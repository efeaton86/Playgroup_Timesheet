from datetime import datetime
import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required

from .timesheet_forms import FormCleaner, FormValidator
from .forms import TimeEntryDetailModelForm
from .models import TimeData

from backend.accounts.models import CustomUser



@login_required
def calendar_app(request):
    """

    :param request:
    :return:
    """
    if request.method == 'GET':
        # serve html and vue app
        return render(request, 'timesheet/time_capture_month.html')

    if request.method == 'POST':
        form = FormCleaner(request)
        validated_form = FormValidator(form.get_cleaned_form())

        # test form data with errors beloe
        # validated_form = FormValidator(
        #     {'dateRangePickerActive': False,
        #      'date': datetime.date(2022, 2, 26),
        #      # 'endDate': datetime.date(2022, 2, 25),
        #      'hours': 0,
        #      'minutes': 0,
        #      'comments': 'multi day',
        #      'payRate': 'overtime',
        #      'user_id': 1}
        # )
        # print(validated_form.errors)


        #write single or multi day entry to db
        if validated_form.is_valid_form:
            for item in validated_form:
                TimeData.objects.create(
                    employee=CustomUser.objects.get(id=item['user_id']),
                    record_date=item['date'],
                    recorded_time=(item['hours'] * 60 + item['minutes']),
                    comments=item['comments'],
                    overtime=item['payRate']
                )
            #  I want to return something else here, not HTTPResponseRedirect
            return HttpResponseRedirect(reverse('admin:index'))

        #if errors found during backend validation
        if not validated_form.is_valid_form:

            payload = {
                'is_valid_form': validated_form.is_valid_form,
                'error_dict': validated_form.get_form_errors()
            }

            return JsonResponse(payload)

def approval_app(request):
    """
    Serves Vue Approval App and handles time entry approvals
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'timesheet/timesheet_approval_app.html')

def approve_user_entries(request):
    pass

def time_entries_view(request):
    if request.method == 'GET':
        # print(request.user.id)
        user_obj = request.user.id

        year = request.GET.get('year', None)
        quarter = request.GET.get('quarter', None)
        month = request.GET.get('month', None)

        current_year = datetime.now().year

        year_filter_options = [current_year - 1, current_year, current_year + 1]

        if not all([year, quarter, month]):
            user_entries = TimeData.objects \
                .filter(employee=request.user) \
                .order_by('-record_date')

        else:

            user_entries = TimeData.objects \
                .filter(employee=request.user) \
                .filter(record_date__year=year)\
                .filter(record_date__month=month)\
                .order_by('-record_date')

        context = {
            'year_filter_options': year_filter_options,
            'user_entries': user_entries,
            'user_obj': user_obj
        }


        return render(request, 'timesheet/time_entries_view.html', context)

def time_entry_detail(request, year=None, month=None, day=None, pk=None):

    if request.method == 'POST':

        return HttpResponseRedirect(reverse('timesheet:time_entries_view'))

    elif request.method == 'GET':
        if pk:
            count_of_entries = 1
            time_entry = TimeData.objects.get(pk=pk)
            form = TimeEntryDetailModelForm(instance=time_entry)
            #print(getattr(time_entry, 'record_date'))
            # to properly format date to set value in js form
            date_str = datetime.strftime(getattr(time_entry, 'record_date'), '%Y-%m-%d')

        # handle returning values based on date
        if pk is None:
            time_entry = TimeData.objects.filter(record_date=f'{year}-{month}-{day}')
            count_of_entries = len(time_entry)

            if count_of_entries == 1:
                form = TimeEntryDetailModelForm(instance=time_entry[0])
                # to properly format date to set value in js form
                date_str = datetime.strftime(time_entry.values()[0].get('record_date'), '%Y-%m-%d')
            elif count_of_entries > 1:
                print(time_entry.values()[0]['comments'])
                multiple_time_entries = time_entry.values()

        context = {
            'form': form if count_of_entries == 1 else None,
            'count_of_entries': count_of_entries,
            'date': date_str if count_of_entries == 1 else None,
            'multiple_time_entries': multiple_time_entries if count_of_entries > 1 else None,
        }
    return render(request, 'timesheet/time_entry_detail.html', context)




#apis

def form_entries(request):
    if request.method == 'GET':
        user = request.user
        month = request.GET.get('month', '')
        year = request.GET.get('year', '')

        time_entries_json = None
        if month and year:
            month = int(month) + 1
            year = int(year)
            time_entries = TimeData.objects \
                .filter(employee=user.id) \
                .filter(
                    record_date__month=month,
                    record_date__year=year
                )

            time_entries_json = json.dumps(
                [entry for entry in time_entries.values()],
                default=str,
                cls=DjangoJSONEncoder
            )

    payload = {
        "time_entries_json": time_entries_json
    }

    return JsonResponse(payload)
