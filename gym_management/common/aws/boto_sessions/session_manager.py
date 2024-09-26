import boto3

from common.threads.thread import get_local, set_local
from gym_management.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    ENDPOINT_URL
)


def initialize_boto_session():
    boto_session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    set_local(boto_session=boto_session)


def fetch_boto_session():
    boto_session = get_local('boto_session')
    if boto_session is None:
        initialize_boto_session()
        boto_session = get_local('boto_session')
    return boto_session


def get_boto_client(service_name):
    session = fetch_boto_session()
    return session.client(
        service_name,
        endpoint_url=ENDPOINT_URL
    )
