import base64
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed
from gym_app.authentication import CustomAuthBackend
from common.threads.thread import set_local, clear_local

import logging

logger = logging.getLogger('gym_app.components')

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION')
        if auth:
            logger.info("Authorization header found.")
            try:
                auth_type, credentials = auth.split()
                if auth_type.lower() == 'basic':
                    username, password = base64.b64decode(credentials).decode('utf-8').split(':')
                    logger.info(f"Decoding credentials for user: {username}")

                    auth_backend = CustomAuthBackend()
                    user = auth_backend.authenticate(request, username=username, password=password)

                    if user is None:
                        raise AuthenticationFailed('Unauthorized')

                    set_local(user_id=user.id)
                    logger.info(f"User ID {user.id} saved to thread-local storage.")
            except Exception as e:
                logger.error(f"Authentication failed: {str(e)}")
        else:
            logger.info("No authorization header found; clearing local storage.")
            clear_local()
