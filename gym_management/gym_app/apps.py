import threading
from django.apps import AppConfig
from services.aws_services.sqs_listener import SQSListener
from gym_management.settings import QUEUE_URL

class GymAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gym_app"

    def ready(self):
        queue_url = QUEUE_URL
        if queue_url:
            listener = SQSListener(queue_url)
            thread = threading.Thread(target=listener.start_listening)
            thread.daemon = True
            thread.start()
        else:
            print("Queue URL not found, SQS Listener not started.")
