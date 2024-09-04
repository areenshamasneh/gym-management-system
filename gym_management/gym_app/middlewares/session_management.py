from django.utils.deprecation import MiddlewareMixin

from common.db.database import Session


class SessionManagementMiddleware(MiddlewareMixin):

    @staticmethod
    def process_response(request, response):
        Session.remove()
        return response
