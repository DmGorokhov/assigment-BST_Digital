from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .services import create_new_order, get_parsed_and_validate_order
from .tasks import make_post_order_tasks


@csrf_exempt
@require_http_methods(['POST'])
def add_new_order(request):
    order_data = get_parsed_and_validate_order(request.body)
    if order_data.error:
        response = JsonResponse(data={"error": order_data.error},
                                status=HttpResponseBadRequest.status_code)
        return response

    new_order = create_new_order(order_data.clean_data)
    make_post_order_tasks.delay(new_order.to_json())
    return JsonResponse(data=new_order.response_data,
                        status=new_order.response_status)
