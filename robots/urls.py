from django.urls import path
from .views import get_week_report
from .views import add_new_robot

app_name = 'robots'

urlpatterns = [
    path('week_report/', get_week_report, name='week_report'),
    path('new/', add_new_robot, name='new_robot'),
]
