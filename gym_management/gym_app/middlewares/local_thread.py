import uuid

from django.utils.deprecation import MiddlewareMixin

from common.threads.thread import set_local, clear_local


class LocalThreadMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        request_id = request.META.get('HTTP_X_REQUEST_ID') or str(uuid.uuid4())
        set_local(request_id=request_id)
        setattr(request, 'request_id', request_id)

    @staticmethod
    def process_response(request, response):
        clear_local()
        return response
