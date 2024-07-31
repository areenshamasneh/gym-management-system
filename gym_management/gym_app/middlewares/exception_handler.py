import json
import logging
from django.http import JsonResponse, Http404
from django.core.exceptions import ValidationError, PermissionDenied
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('custom.request')

class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, json.JSONDecodeError):
            response_data = {
                "error": {
                    "code": "INVALID_JSON",
                    "details": "Invalid JSON"
                }
            }
            logger.error(response_data)
            return JsonResponse(response_data, status=400)
        elif isinstance(exception, Http404):
            response_data = {
                "error": {
                    "code": "NOT_FOUND",
                    "details": str(exception)
                }
            }
            logger.error({
                "remote_address": request.META.get('REMOTE_ADDR'),
                "request_method": request.method,
                "request_path": request.path,
                "exception": str(exception)
            })
            return JsonResponse(response_data, status=404)
        elif isinstance(exception, ValidationError):
            response_data = {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "details": exception.message_dict
                }
            }
            logger.error(response_data)
            return JsonResponse(response_data, status=400)
        elif isinstance(exception, PermissionDenied):
            response_data = {
                "error": {
                    "code": "PERMISSION_DENIED",
                    "details": "Permission denied"
                }
            }
            logger.error(response_data)
            return JsonResponse(response_data, status=403)
        elif isinstance(exception, NotImplementedError):
            response_data = {
                "error": {
                    "code": "NOT_IMPLEMENTED",
                    "details": "Feature not implemented"
                }
            }
            logger.error(response_data)
            return JsonResponse(response_data, status=501)
        elif isinstance(exception, KeyError):
            response_data = {
                "error": {
                    "code": "KEY_ERROR",
                    "details": f"Missing key: {str(exception)}"
                }
            }
            logger.error(response_data)
            return JsonResponse(response_data, status=400)
        else:
            response_data = {
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "details": "Internal server error"
                }
            }
            logger.error({
                "remote_address": request.META.get('REMOTE_ADDR'),
                "request_method": request.method,
                "request_path": request.path,
                "exception": str(exception)
            })
            return JsonResponse(response_data, status=500)
