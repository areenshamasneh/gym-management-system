import json
import threading
from django.apps import AppConfig
from services.aws_services.sqs_listener import SQSListener

class GymAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gym_app"

    def ready(self):
        queue_url = self.load_queue_url()
        if queue_url:
            listener = SQSListener(queue_url)
            thread = threading.Thread(target=listener.start_listening)
            thread.daemon = True
            thread.start()
        else:
            print("Queue URL not found, SQS Listener not started.")

    @staticmethod
    def load_queue_url():
        try:
            with open('config.json') as config_file:
                config = json.load(config_file)
            return config.get('QUEUE_URL')
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading queue URL from config file: {e}")
            return None
