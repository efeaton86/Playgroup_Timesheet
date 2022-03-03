from django.db import models
from django.conf import settings

from django.core.validators import MinValueValidator, MaxValueValidator

from .timesheet_config import PAY_CYCLE_END_DATE

# Create your models here.

PAYRATE_CHOICES = [
    ('base', 'Base'),
    ('overtime', 'Overtime')
]


class PayPeriodManager(models.Manager):
    """
    Custom Manager that returns a list of entries that fall inside
    of a pay period
    """
    def get_current_pay_period_entries(self, pay_period):
        if isinstance(pay_period, str):
            pay_period = (int(pay_period.split('-')[0]), int(pay_period.split('-')[1]))

        entries = TimeData.objects.all()
        entry_values = entries.values()
        entry_pay_periods = [entry.pay_period_status() for entry in entries]
        filtered_pay_period_entries = []
        for values, entry_pay_period in zip(entry_values, entry_pay_periods):
            if pay_period == entry_pay_period:
                values['pay_period'] = entry_pay_period
                filtered_pay_period_entries.append(values)
        return filtered_pay_period_entries


class TimeData(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT
    )
    created = models.DateTimeField(auto_now_add=True)
    record_date = models.DateField()
    recorded_time = models.DecimalField(max_digits=6, decimal_places=2)
    comments = models.TextField()
    #overtime = models.BooleanField(default=False)
    overtime = models.CharField(max_length=8, choices=PAYRATE_CHOICES)
    entry_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Time Data'

    def pay_period_status(self):

        """
        Returns the pay period a time entry should be assigned to.
        For use in dashboard vue where approving time entries
        """

        from datetime import datetime
        from dateutil.relativedelta import relativedelta

        record_date_minus_month = self.record_date + relativedelta(months=-1)
        year = self.record_date.year
        month = self.record_date.month
        start_of_pay_cycle = datetime.strptime(f'{record_date_minus_month.year}-{record_date_minus_month.month}-{PAY_CYCLE_END_DATE + 1}', '%Y-%m-%d').date()
        end_of_pay_cycle = datetime.strptime(f'{year}-{month}-{PAY_CYCLE_END_DATE}', '%Y-%m-%d').date()

        if start_of_pay_cycle < self.record_date <= end_of_pay_cycle:
            return (year, month)
        elif self.record_date > end_of_pay_cycle:
            return (year, month + 1)
        elif self.record_date < start_of_pay_cycle:
            return (year, month - 1)

    objects = models.Manager()
    pay_period_entries = PayPeriodManager()


class PayPeriod(models.Model):
    set_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    updated_on = models.DateField()
    pay_period_closure_date = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(31)
        ]
    )





