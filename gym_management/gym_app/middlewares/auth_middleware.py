import base64

from django.contrib.auth import authenticate
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION')
        if auth:
            try:
                auth_type, credentials = auth.split()
                if auth_type.lower() == 'basic':
                    username, password = base64.b64decode(credentials).decode('utf-8').split(':')
                    user = authenticate(username=username, password=password)
                    if user is None:
                        raise AuthenticationFailed('Unauthorized')
                    request.user = user
            except Exception as e:
                raise AuthenticationFailed('Unauthorized')
