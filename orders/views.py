from django.views import View
from django.http import HttpResponse

class OrderStubView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('In development')
