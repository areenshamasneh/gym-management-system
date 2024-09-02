import threading
import uuid


class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.local = threading.local()

    def __call__(self, request):
        request_id = request.META.get('HTTP_X_REQUEST_ID') or str(uuid.uuid4())
        self.local.request_id = request_id
        setattr(request, 'request_id', request_id)

        response = self.get_response(request)
        response['X-Request-ID'] = request_id

        return response

    @staticmethod
    def get_request_id():
        return getattr(threading.local(), 'request_id', None)
