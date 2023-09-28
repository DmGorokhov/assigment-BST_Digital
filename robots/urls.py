from django.urls import path
from .views import get_week_report

app_name = 'robots'

urlpatterns = [
    path('week_report/', get_week_report, name='week_report'),
]
