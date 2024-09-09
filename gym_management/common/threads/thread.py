import threading

_local = threading.local()


def set_local(**kwargs):
    for key, value in kwargs.items():
        setattr(_local, key, value)


def get_local(key, default=None):
    return getattr(_local, key, default)


def clear_local():
    _local.__dict__.clear()


def get_request_id():
    return get_local('request_id')
