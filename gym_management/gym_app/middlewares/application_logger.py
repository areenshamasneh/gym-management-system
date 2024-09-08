import json
import logging
import socket
import time
from django.utils.deprecation import MiddlewareMixin

request_logger = logging.getLogger("custom.request")


class ApplicationLogMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, request):
        response = self.get_response(request)
        log_data = self.extract_log_info(request=request, response=response)
        request_logger.info(json.dumps(log_data, indent=4))
        return response

    def process_request(self, request):
        request.start_time = time.time()

    def extract_log_info(self, request, response=None, exception=None):
        log_data = {
            "remote_address": request.META.get("REMOTE_ADDR"),
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
            "run_time": (
                time.time() - request.start_time if hasattr(request, "start_time") else None
            ),
        }

        if request.method in ["PUT", "POST", "PATCH"]:
            try:
                log_data["request_body"] = json.loads(request.body.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                log_data["request_body"] = request.body.decode("utf-8", errors='ignore')

        if response:
            log_data["response_status"] = response.status_code
            if response.get("content-type") == "application/json":
                try:
                    log_data["response_body"] = json.loads(response.content.decode("utf-8"))
                except json.JSONDecodeError:
                    log_data["response_body"] = response.content.decode("utf-8")

        if exception:
            log_data["exception"] = str(exception)

        return log_data

    def process_response(self, request, response):
        log_data = self.extract_log_info(request=request, response=response)
        request_logger.info(json.dumps(log_data, indent=4))
        return response

    def process_exception(self, request, exception):
        log_data = self.extract_log_info(request=request, exception=exception)
        request_logger.error(json.dumps(log_data, indent=4))
        return exception
