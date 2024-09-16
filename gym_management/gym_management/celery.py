from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_management.settings')

app = Celery('gym_management')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'process-sqs-messages-every-minute': {
        'task': 'gym_app.tasks.process_sqs_messages',
        'schedule': crontab(minute='*/1'),
        'args': ('http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/Queue',)
    },
}

