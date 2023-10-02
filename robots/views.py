from django.http import FileResponse
from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from robots.services.services_main import (save_new_robot,
                                           get_parsed_and_validate_robot)
from robots.services.services_reports import make_week_report


@require_http_methods(['GET'])
def get_week_report(request):
    report_data = make_week_report()
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")
    report_filename = f'week_report {current_datetime}.xlsx'
    response = FileResponse(report_data,
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', # noqa E501
                            # noqa: E501
                            filename=report_filename, as_attachment=True)
    return response


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
