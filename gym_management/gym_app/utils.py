from rest_framework.views import exception_handler # type: ignore
from rest_framework.response import Response # type: ignore

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'error': {
                'status_code': response.status_code,
                'message': response.data.get('detail', 'An error occurred.'),
            }
        }
    else:
        response = Response(
            data={
                'error': {
                    'status_code': 500,
                    'message': 'An unexpected error occurred.',
                }
            },
            status=500
        )

    return response