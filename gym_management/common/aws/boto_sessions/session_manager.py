import threading
import boto3
from gym_management.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    ENDPOINT_URL
)

class SessionManager:
    _thread_local = threading.local()

    @classmethod
    def get_session(cls):
        if not hasattr(cls._thread_local, 'session'):
            cls._thread_local.session = boto3.Session(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION
            )
        return cls._thread_local.session

    @classmethod
    def get_client(cls, service_name):
        session = cls.get_session()
        return session.client(
            service_name,
            endpoint_url=ENDPOINT_URL
        )
