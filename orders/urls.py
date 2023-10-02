from django.urls import path
from .views import add_new_order

app_name = 'orders'

urlpatterns = [
    path('new/', add_new_order, name='new_order'),
]
