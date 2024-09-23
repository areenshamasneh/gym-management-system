import os
from pathlib import Path

from decouple import config  # type: ignore

DATABASE_URL = config('DATABASE_URL')
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_REGION = config('AWS_REGION')
ENDPOINT_URL = config('ENDPOINT_URL')
QUEUE_URL = config('QUEUE_URL')
CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Gaza'

AWS = {
    'sns': {
        'entity_added': 'arn:aws:sns:us-east-1:000000000000:Topic1',
        'entity_updated': 'arn:aws:sns:us-east-1:000000000000:Topic1',
        'entity_removed': 'arn:aws:sns:us-east-1:000000000000:Topic2'
    },
    'sqs': {
        'queue1': 'http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/Queue1',
        'queue2': 'http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/Queue2',
    }
}

BASE_DIR = Path(__file__).resolve().parent.parent

log_dir = os.path.join(BASE_DIR, "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Use the SECRET_KEY from the .env file
SECRET_KEY = config("DJANGO_SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'kubernetes.docker.internal',
]
INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS = [
    "gym_app",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "gym_app.middlewares.application_logger.ApplicationLogMiddleware",
    "gym_app.middlewares.local_thread.LocalThreadMiddleware",
    "gym_app.middlewares.session_management.SessionManagementMiddleware",
]
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "file_logging": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "components_logging.log"),
            "formatter": "default",
        },
        "console_logging": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "request_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "requests_responses.log"),
            "formatter": "default",
        },
        "sql_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "sql_queries.log"),
            "formatter": "default",
        },
    },
    "loggers": {
        "custom.request": {
            "handlers": ["request_file", "console_logging"],
            "level": "INFO",
            "propagate": False,
        },
        "gym_app.components": {
            "handlers": ["file_logging", "console_logging"],
            "level": "INFO",
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "handlers": ["sql_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',

    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'EXCEPTION_HANDLER': 'common.handlers.exception_handler.handle_exception',
}

ROOT_URLCONF = "gym_management.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "gym_management.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "HOST": config("DATABASE_HOST"),
        "PORT": config("DATABASE_PORT", default=3306, cast=int),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Gaza"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
