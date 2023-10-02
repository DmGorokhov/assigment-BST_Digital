from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .services import save_new_robot, get_parsed_and_validate_robot


@csrf_exempt
@require_http_methods(['POST'])
def add_new_robot(request):
    robot_data = get_parsed_and_validate_robot(request.body)
    if robot_data.error:
        response = JsonResponse(data={"error": robot_data.error},
                                status=HttpResponseBadRequest.status_code)
        return response
    new_robot = save_new_robot(robot_data.clean_data)
    return JsonResponse(data=new_robot.response_message,
                        status=new_robot.response_status)
