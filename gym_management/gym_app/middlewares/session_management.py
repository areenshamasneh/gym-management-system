from django.utils.deprecation import MiddlewareMixin
from common.db.database import Session


class SessionManagementMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        request.db_session = Session()

    @staticmethod
    def process_response(request, response):
        try:
            if 200 <= response.status_code < 400:
                request.db_session.commit()
        except Exception:
            request.db_session.rollback()
            raise
        finally:
            Session.remove()
        return response

    @staticmethod
    def process_exception(request, exception):
        request.db_session.rollback()
        Session.remove()
