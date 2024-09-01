from common import Session
import logging

logging.basicConfig()
logger = logging.getLogger('sqlalchemy.engine')


class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.db_session = Session()
        try:
            response = self.get_response(request)
            if request.db_session.is_active:
                logger.info("Committing session")
                request.db_session.commit()
        except Exception:
            if request.db_session.is_active:
                logger.error("Rolling back session due to error")
                request.db_session.rollback()
            raise
        finally:
            logger.info("Removing session")
            Session.remove()
        return response
