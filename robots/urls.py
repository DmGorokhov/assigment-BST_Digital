from django.urls import path
from .views import add_new_robot

app_name = 'robots'

urlpatterns = [
    path('new/', add_new_robot, name='new_robot'),
]
