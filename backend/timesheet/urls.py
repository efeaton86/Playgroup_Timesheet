from django.views.decorators.csrf import csrf_exempt

# from graphene_django.views import GraphQLView

from django.urls import path
from .views import calendar_app, approval_app, time_entries_view, time_entry_detail, form_entries, approve_user_entries
from .apis import get_all_users, get_user_time_entries, get_all_user_time_entries, get_user_time_entry_data
app_name = 'timesheet'

urlpatterns = [
    # views
    path('', calendar_app, name='calendar_app'),
    path('approval/', approval_app, name='approval_app'),
    path('approval/<int:pk>/', approve_user_entries, name=''),
    path('user_entries/', time_entries_view, name='time_entries_view'),
    path('user_entries/<int:pk>/', time_entry_detail, name='time_entry_detail'),
    path('user_entries/<int:year>/<int:month>/<int:day>/', time_entry_detail, name='time_entry_detail'),

    # api
    path('api/form_entries/', form_entries),
    path('api/get_users/', get_all_users, name='get_all_users'),
    path('api/get_all_user_time_entries/', get_all_user_time_entries, name='get_all_user_time_entries'),
    path('api/get_user_time_entries/', get_user_time_entries, name='get_all_users'),
    path('api/get_user_time_entry_data/', get_user_time_entry_data, name='get_user_time_entry_data')
]
