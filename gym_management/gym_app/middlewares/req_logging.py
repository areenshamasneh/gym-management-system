import logging
from django.utils.deprecation import MiddlewareMixin
import socket
import time
import json

request_logger = logging.getLogger("custom.request")


class RequestLogMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith("/api/"):
            log_data = self.extract_log_info(request=request, response=response)
            request_logger.info(json.dumps(log_data, indent=4))
        return response

    def process_request(self, request):
        if request.method in ["POST", "PUT", "PATCH"]:
            request.req_body = request.body
        if request.path.startswith("/api/"):
            request.start_time = time.time()

    def extract_log_info(self, request, response=None, exception=None):
        log_data = {
            "remote_address": request.META.get("REMOTE_ADDR"),
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
            "run_time": (
                time.time() - request.start_time
                if hasattr(request, "start_time")
                else None
            ),
        }
        if request.method in ["PUT", "POST", "PATCH"] and hasattr(request, "req_body"):
            try:
                log_data["request_body"] = json.loads(request.req_body.decode("utf-8"))
            except json.JSONDecodeError:
                log_data["request_body"] = request.req_body.decode("utf-8")
        if response:
            log_data["response_status"] = response.status_code
            if response.get("content-type") == "application/json":
                try:
                    log_data["response_body"] = json.loads(
                        response.content.decode("utf-8")
                    )
                except json.JSONDecodeError:
                    log_data["response_body"] = response.content.decode("utf-8")
        if exception:
            log_data["exception"] = str(exception)
        return log_data

    def process_response(self, request, response):
        if request.path.startswith("/api/"):
            log_data = self.extract_log_info(request=request, response=response)
            request_logger.info(json.dumps(log_data, indent=4))
        return response

    def process_exception(self, request, exception):
        if request.path.startswith("/api/"):
            log_data = self.extract_log_info(request=request, exception=exception)
            request_logger.error(json.dumps(log_data, indent=4))
        return exception
