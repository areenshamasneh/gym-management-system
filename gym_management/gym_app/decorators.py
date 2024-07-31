import json
from django.http import JsonResponse, Http404
from functools import wraps
from django.core.exceptions import ValidationError, PermissionDenied


def handle_exceptions(view_func):
    @wraps(view_func)
    def _wrapped_view(view, request, *args, **kwargs):
        try:
            return view_func(view, request, *args, **kwargs)
        except json.JSONDecodeError:
            response_data = {
                "error": {"code": "INVALID_JSON", "details": "Invalid JSON"}
            }
            return JsonResponse(response_data, status=400)
        except Http404 as e:
            response_data = {"error": {"code": "NOT_FOUND", "details": str(e)}}
            return JsonResponse(response_data, status=404)
        except ValidationError as ve:
            response_data = {
                "error": {"code": "VALIDATION_ERROR", "details": ve.message_dict}
            }
            return JsonResponse(response_data, status=400)
        except PermissionDenied:
            response_data = {
                "error": {"code": "PERMISSION_DENIED", "details": "Permission denied"}
            }
            return JsonResponse(response_data, status=403)
        except NotImplementedError:
            response_data = {
                "error": {
                    "code": "NOT_IMPLEMENTED",
                    "details": "Feature not implemented",
                }
            }
            return JsonResponse(response_data, status=501)
        except KeyError as ke:
            response_data = {
                "error": {"code": "KEY_ERROR", "details": f"Missing key: {str(ke)}"}
            }
            return JsonResponse(response_data, status=400)
        except Exception as e:
            response_data = {
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "details": "Internal server error",
                }
            }
            return JsonResponse(response_data, status=500)

    return _wrapped_view
