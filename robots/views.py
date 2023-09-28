from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .services import create_new_robot, save_new_robot


@csrf_exempt
@require_http_methods(['POST'])
def add_new_robot(request):
    new_robot = create_new_robot(request.body)
    if new_robot.error:
        response = JsonResponse(data={"error": new_robot.error},
                                status=HttpResponseBadRequest.status_code)
    else:
        robot = save_new_robot(new_robot.data)
        response = JsonResponse({'success': {'Robot added':
                                                 {"model": robot.model,
                                                  "version": robot.version
                                                  }
                                             }
                                 }, status=200)
    return response
