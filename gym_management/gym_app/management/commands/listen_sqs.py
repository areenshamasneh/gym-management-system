import json

from django.core.management.base import BaseCommand

from services.aws_services.sqs_listener import SQSListener


class Command(BaseCommand):
    help = 'Starts the SQS listener'

    def handle(self, *args, **kwargs):
        queue_url = self.load_queue_url()
        sqs_listener = SQSListener(queue_url)
        self.stdout.write(self.style.SUCCESS('Listening to SQS queue...'))
        sqs_listener.start_listening()

    @staticmethod
    def load_queue_url():
        try:
            with open('config.json') as config_file:
                config = json.load(config_file)
            return config.get('QUEUE_URL')
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading topic ARN from config file: {e}")
            raise