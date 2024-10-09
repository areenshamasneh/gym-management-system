import binascii
from base64 import b64decode

from rest_framework import permissions, exceptions
from rest_framework.authentication import get_authorization_header
from gym_app.models.models_sqlalchemy import User
from common.db.database import Session
from common.threads.thread import set_local


class BasicAuthPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        auth_header = get_authorization_header(request).decode('utf-8')
        if not auth_header or not auth_header.startswith('Basic '):
            return False

        try:
            auth_decoded = b64decode(auth_header.split()[1]).decode('utf-8')
            username, password = auth_decoded.split(':')

            user = Session.query(User).filter(User.username == username).first()
            if not user:
                raise exceptions.AuthenticationFailed('Invalid credentials')

            if not user.check_password(password):
                raise exceptions.AuthenticationFailed('Invalid credentials')

            request.user = user
            set_local(user_id=user.id)

            return True
        except (ValueError, binascii.Error):
            print("Error decoding credentials")
            raise exceptions.AuthenticationFailed('Invalid credentials')
        except Exception as e:
            print(f"Authentication error: {e}")
            raise exceptions.AuthenticationFailed('An unexpected error occurred.')
