from rest_framework.views import exception_handler # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.exceptions import APIException # type: ignore
from django.http import Http404
from gym_app.exceptions import ValidationException

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    status_code = 500
    message = "An unexpected error occurred."

    if isinstance(exc, APIException):
        status_code = exc.status_code
        message = exc.detail
    elif isinstance(exc, Http404):
        status_code = 404
        message = str(exc)
    elif isinstance(exc, NotImplementedError):
        status_code = 501
        message = "Feature not implemented."
    elif isinstance(exc, KeyError):
        status_code = 400
        message = f"Missing key: {str(exc)}"

    if isinstance(exc, ValidationException) and response is not None:
        message = exc.message_dict

    error_message = {
        "error": {
            "status_code": status_code,
            "message": message,
        }
    }

    if response is not None:
        response.data = error_message
        response.status_code = status_code
    else:
        response = Response(data=error_message, status=status_code)

    return response
