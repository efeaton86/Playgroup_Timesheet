import json

from datetime import datetime, timedelta

from .timesheet_config import field_to_function_parser

##### Data Descriptors#####

class DateDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        #if value is a string, try to coerce to datetime
        if not isinstance(value, str) and not isinstance(value, datetime):
            raise ValueError(f'{self.name} must be either string or datetime object')
        if isinstance(value, str):
            try:
                dt_obj = datetime.strptime(value, '%Y-%m-%d')
            except ValueError as ex:
                print(ex)
            else:
                instance.__dict__[self.name] = dt_obj
        if isinstance(value, datetime):
            dt_obj = value.date()
            instance.__dict__[self.name] = dt_obj


class IntDescriptor:
    def __init__(self, min_val=None, max_val=None):
        self.min_val = min_val
        self.max_val = max_val

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        if not isinstance(value, int) and not isinstance(value, str):   # if not int or str raise
            raise TypeError(f'{self.name} must be an integer or string type.')
        if isinstance(value, str):  # if string
            if not value:
                value = 0
            try:
                value = int(value)
            except ValueError:
                raise Exception(f'{self.name} must be an integer')
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f'{self.name} cannot be less than the minimum value of {self.min_val}.')
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f'{self.name} cannot be greater than the maximum value of {self.max_val}.')
        instance.__dict__[self.name] = value


class StrDescriptor:
    def __init__(self, min_val=None, max_val=None):
        self.min_val = min_val
        self.max_val = max_val

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError(f'{self.name} must be a string.')
        if self.min_val is not None and len(value) < self.min_val:
            raise ValueError(f'{self.name} must be greater than the minimum value of {self.min_val}')
        if self.max_val is not None and len(value) > self.max_val:
            raise ValueError(f'{self.name} must be less than the maximum value of {self.max_val}')
        instance.__dict__[self.name] = value


class BooleanDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if not instance:
            return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        if isinstance(value, str):
            instance.__dict__[self.name] = value == 'True'
            #if value.casefold in {'1', 't', 'true}
            #return True
        if isinstance(value, int) and value not in {0, 1}:
            raise ValueError('Integer value must be either "1" or "0" to represent a boolean.')
        instance.__dict__[self.name] = bool(value)


class FormCleaner:
    """
    Cleans and preps submitted form so that it can be validated in the Form validator class
    """
    def __init__(self, django_request):
        self._request = django_request
        self.form = django_request
        self._clean_form()

    @property
    def form(self):
        return self._form

    @form.setter
    def form(self, django_request):
        data = json.loads(django_request.body)
        data['user_id'] = django_request.user.id
        self._form = data

    def _clean_form(self):
        cleaned_form_fields = {}
        for field_name, field_value in self.form.items():
            value = field_to_function_parser[field_name](field_value)
            cleaned_form_fields[field_name] = value
        self.cleaned_form = cleaned_form_fields

    def get_cleaned_form(self):
        return self.cleaned_form

class FormValidator:

    def __init__(self, form):
        #data members
        self.form = form
        self.errors = {
            'userID': None,
            'date': None,
            'hours': None,
            'minutes': None,
            'comments': None,
            'pay_rate': None
        }
        self.is_day_range_entry = form['dateRangePickerActive']

        # flag
        self.is_valid_form = True

        # method calls during initialization
        self.validate_form_fields()

    def __iter__(self):
        """
        If form is single day entry -> return self.form
        If form is multi day entry -> Yield single day
        :return: dictionary
        """
        if self.is_valid_form and not self.is_day_range_entry:
            yield self.form

        elif self.is_valid_form and self.is_day_range_entry:
            date_array = self.build_time_delta_array(start_date=self.form['date'], end_date=self.form['endDate'])
            single_day_form = {k: v for k, v in self.form.items()}
            for i in range(len(date_array)):
                single_day_form['date'] = date_array[i]
                yield single_day_form

    def add_error(self, field, error):
        self.errors[field] = error

    def get_form_errors(self):
        return self.errors

    def validate_form_fields(self):
        """
        Validation logic for the form
        :return:
        """
        # user not authenticated
        if not self.form['user_id']:
            self.errors['userID'] = 'You must be signed in to capture working hours.'
            self.is_valid_form = False

        # hour and minutes empty
        if not self.form['hours'] and not self.form['minutes']:
            self.errors['hours'] = 'Hours or minutes must contain a value.'
            self.errors['minutes'] = 'Hours or minutes must contain a value.'
            self.is_valid_form = False

        # hour and minutes both 0
        if self.form['hours'] <= 0 and self.form['minutes'] <= 0:
            self.errors['hours'] = 'Hours or minutes must be greater than 0.'
            self.errors['minutes'] = 'Hours or minutes must be greater than 0.'
            self.is_valid_form = False

        # if its a date range flag is active, an end date is less than start date, raise error
        if self.is_day_range_entry and (self.form['date'] > self.form['endDate']):
            self.errors['date'] = 'Start date must come before end date.'
            self.is_valid_form = False

        if self.form['hours'] is None: # if above validation passes, it means hour left empty on purpose
            self.form['hours'] = 0
        if self.form['minutes'] is None:
            self.form['minutes'] = 0

    @staticmethod
    def build_time_delta_array(start_date, end_date, weekend_flag=None):
        delta = end_date - start_date
        date_array = [(start_date + timedelta(days=i)) for i in range(delta.days + 1)]
        return date_array




