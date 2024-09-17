import json
import time
from concurrent.futures import ThreadPoolExecutor
from services.aws_services.handlers import get_handler_for_event
from services.aws_services.sqs_service import SQSService

class SQSListener:
    def __init__(self, queue_url, max_workers=10):
        self.queue_url = queue_url
        self.sqs_service = SQSService(queue_url)
        self.max_workers = max_workers

    def process_message(self, message):
        try:
            message_body = json.loads(message['Body'])
            sns_message = json.loads(message_body.get('Message', '{}'))
            event_code = sns_message.get('code')
            event_data = sns_message.get('data', {})

            handler = get_handler_for_event(event_code)
            if handler:
                handler.handle_message(event_data)
                print(f"Attempting to delete message with ReceiptHandle: {message['ReceiptHandle']}")
                try:
                    self.sqs_service.delete_message(message['ReceiptHandle'])
                    print(f"Message with code '{event_code}' processed and deleted.")
                except Exception as e:
                    print(f"Failed to delete message: {e}")
            else:
                print(f"No handler found for event code: {event_code}")

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Failed to process message: {e}")

    def start_listening(self):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while True:
                messages = self.sqs_service.receive_messages()
                if messages:
                    print(f"Received messages: {len(messages)}")
                    for message in messages:
                        executor.submit(self.process_message, message)
                else:
                    print("No messages available. Waiting...")
                time.sleep(5)
