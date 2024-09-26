from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_management.settings')

app = Celery('gym_management')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['gym_app.tasks'])

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from gym_app.tasks import poll_sqs_queues
    sender.add_periodic_task(5.0, poll_sqs_queues.s(), name='poll SQS queue every 5 seconds')
