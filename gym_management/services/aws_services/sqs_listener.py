import pprint
from concurrent.futures import ThreadPoolExecutor
import json
import time
from services.aws_services.handlers import get_handler_for_event
from services.aws_services.sqs_service import SQSService

class SQSListener:
    def __init__(self, queue_url, max_workers=10):
        self.sqs_service = SQSService(queue_url)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def process_message(self, message):
        try:
            print("Received message:")
            pprint.pprint(json.loads(message['Body']), indent=4)
            message_body = json.loads(message['Body'])
            sns_message = json.loads(message_body['Message'])
            event_type = sns_message.get('eventType')
            entity_type = sns_message['data'].get('entityType')

            if not event_type or not entity_type:
                print("No event_type or entity_type found in the message.")
                return False

            handler = get_handler_for_event(event_type)
            if handler:
                handler.handle_message(entity_type, sns_message['data'])
                self.sqs_service.delete_message(message['ReceiptHandle'])
                print(f"Message with event type '{event_type}' for entity '{entity_type}' processed and deleted.")
                return True
            else:
                print(f"No handler found for event type: {event_type}")
                return False

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Failed to process message: {e}")
            return False

    def start_listening(self, max_iterations=1):
        print("Listening to SQS queue...")
        for _ in range(max_iterations):
            messages = self.sqs_service.receive_messages()

            if messages:
                futures = [self.executor.submit(self.process_message, msg) for msg in messages]
                for future in futures:
                    if not future.result():
                        print("Message not processed. Skipping deletion.")
            else:
                print("No messages available. Waiting...")

            time.sleep(5)
