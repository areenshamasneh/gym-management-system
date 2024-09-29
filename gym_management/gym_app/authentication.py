from sqlalchemy import select

from common.db.database import Session
from gym_app.models.models_sqlalchemy import User

import logging

logger = logging.getLogger('gym_app.components')

class CustomAuthBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        logger.info(f"Attempting to authenticate user: {username}")
        try:
            query = select(User).filter(User.username == username)
            result = Session.execute(query)
            user = result.scalar_one_or_none()

            if user and user.check_password(password):
                logger.info(f"User {username} authenticated successfully.")
                return user
            logger.warning(f"User {username} not found or password mismatch.")
        except Exception as e:
            logger.error(f"Error during authentication: {str(e)}")
        return None

