from django.views import View
from django.http import HttpResponse


# Create your views here.
class RobotStubView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('In development')
