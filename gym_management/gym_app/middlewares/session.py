import threading

from django.utils.deprecation import MiddlewareMixin
from common.database import Session
from gym_app.middlewares.req_id_correlation import RequestIDMiddleware

request_id_middleware = RequestIDMiddleware(None)


class SessionMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        request_id = request_id_middleware.get_request_id()
        setattr(threading.local(), 'request_id', request_id)
        setattr(request, 'request_id', request_id)

    @staticmethod
    def process_response(request, response):
        Session.remove()
        return response
