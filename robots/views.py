from django.http import FileResponse
from django.views.decorators.http import require_http_methods
from .services import make_week_report
from datetime import datetime


@require_http_methods(['GET'])
def get_week_report(request):
    report_data = make_week_report()
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")
    report_filename = f'week_report {current_datetime}.xlsx'
    response = FileResponse(report_data,
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # noqa: E501
                            filename=report_filename, as_attachment=True)
    return response
