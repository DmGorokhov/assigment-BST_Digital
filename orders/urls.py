from django.urls import path
from .views import OrderStubView

urlpatterns = [
    path('', OrderStubView.as_view()),
]
