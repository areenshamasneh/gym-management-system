
import time
from gym_app.tasks import process_sqs_messages
class SQSListener:
    def __init__(self, queue_url, max_workers=10):
        self.queue_url = queue_url
        self.max_workers = max_workers

    def start_listening(self):
        print("Listening to SQS queue...")
        while True:
            process_sqs_messages.delay(self.queue_url)
            time.sleep(10)
