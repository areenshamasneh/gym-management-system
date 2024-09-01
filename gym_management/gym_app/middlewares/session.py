from common import Session


class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.db_session = Session()

        try:
            response = self.get_response(request)
            if request.db_session.is_active:
                request.db_session.commit()
        except Exception:
            if request.db_session.is_active:
                request.db_session.rollback()
            raise
        finally:
            Session.remove()

        return response
