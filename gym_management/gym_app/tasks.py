import json
from celery import shared_task
from services.aws_services.handlers import get_handler_for_event
from services.aws_services.sqs_service import SQSService

@shared_task
def process_sqs_messages(queue_url):
    sqs_service = SQSService(queue_url)
    messages = sqs_service.receive_messages()

    for message in messages:
        message_body = json.loads(message['Body'])
        sns_message = json.loads(message_body.get('Message', '{}'))
        event_code = sns_message.get('code')
        event_data = sns_message.get('data', {})

        handler = get_handler_for_event(event_code)
        if handler:
            handler.handle_message(event_data)
            print(f"Attempting to delete message with ReceiptHandle: {message['ReceiptHandle']}")
            try:
                sqs_service.delete_message(message['ReceiptHandle'])
                print(f"Message with code '{event_code}' processed and deleted.")
            except Exception as e:
                print(f"Failed to delete message: {e}")
        else:
            print(f"No handler found for event code: {event_code}")

