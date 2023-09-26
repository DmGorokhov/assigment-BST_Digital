from django.urls import path
from .views import RobotStubView

urlpatterns = [
    path('', RobotStubView.as_view()),
]
