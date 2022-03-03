import json
from collections import defaultdict


from django.contrib.auth import get_user_model
from .models import TimeData
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

from .timesheet_utils import get_current_pay_period, calculate_days_remaining_in_pay_period

from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_user_time_entry_data(request):
    payload = {}
    if request.method == 'PUT':
        data = json.loads(request.body)

        users = get_user_model().objects.values('id', 'username', 'first_name', 'last_name', 'email')
        current_pay_period_entries = TimeData.pay_period_entries.get_current_pay_period_entries(data['payPeriod'])

        users_json = json.dumps([user for user in users], cls=DjangoJSONEncoder)

        payload = {
            "users": users_json,
            "pay_period_entries": current_pay_period_entries,
        }

    if request.method == 'GET':
        pass

    return JsonResponse({'payload': payload})

def get_all_users(request):
    """API that passes data initially required for Vue dashboard page load"""

    # Get list of users
    users = get_user_model().objects.values('id', 'username', 'first_name', 'last_name', 'email')
    users_json = json.dumps([user for user in users], cls=DjangoJSONEncoder)

    # Get entries for the current pay period which will be dependent on datetime.now()
    active_pay_period = get_current_pay_period()  # active pay period - based on where 'today' of user
    current_pay_period_entries = TimeData.pay_period_entries.get_current_pay_period_entries(active_pay_period)


    #math on entries
    employee_total_hours_per_period = defaultdict(int)
    for entry in current_pay_period_entries:
        user = entry['employee_id']
        time = entry['recorded_time']
        employee_total_hours_per_period[user] += time

    completed_days, total_days = calculate_days_remaining_in_pay_period()

    # Payload
    payload = {
        "users": users_json,
        "pay_period_entries": current_pay_period_entries,
        "completed_day": completed_days,
        "total_days": total_days,
    }

    return JsonResponse(payload)

def get_all_user_time_entries(request):

    return JsonResponse({'message': 'success'})

def get_user_time_entries(request):
    user_id = request.GET.get('userID')

    user_entries = TimeData.objects.filter(employee_id=user_id)
    for item in user_entries:
        pass
        # print(item.pay_period_status())
    user_entries_json = json.dumps(
        [entry for entry in user_entries.values()],
        default=str,
        cls=DjangoJSONEncoder
    )
    # print(user_entries_json)
    payload = {
        'user_entries': user_entries_json
    }

    return JsonResponse(payload)

def get_users_entries_for_pay_period(request):
    pass
