import calendar
from datetime import datetime
from .timesheet_config import PAY_CYCLE_END_DATE

def get_current_pay_period():
    """Function that will calculate a given pay period range"""
    from dateutil.relativedelta import relativedelta
    today = datetime.now().date()
    end_of_pay_cycle = datetime.strptime(f'{today.year}-{today.month}-{PAY_CYCLE_END_DATE}', '%Y-%m-%d').date()
    start_of_pay_cycle = end_of_pay_cycle + relativedelta(months=-1)

    if start_of_pay_cycle < today <= end_of_pay_cycle:
        return (today.year, today.month)
    elif today > end_of_pay_cycle:
        return (today.year, today.month + 1)
    elif today < start_of_pay_cycle:
        return (today.year, today.month - 1)


def calculate_days_remaining_in_pay_period():
    """
    Calculates the total days in a time period and the days completed.
    Returns: 2 integer tuple - (completed days and total days in pay period)
    """
    from dateutil.relativedelta import relativedelta

    now = datetime.now().date()
    payperiod_end = datetime.strptime(f'{now.year}-{now.month}-{PAY_CYCLE_END_DATE}', '%Y-%m-%d').date()
    payperiod_start = payperiod_end + relativedelta(months=-1)

    completed_days = (now - payperiod_start).days
    total_days = (payperiod_end - payperiod_start).days

    return completed_days, total_days