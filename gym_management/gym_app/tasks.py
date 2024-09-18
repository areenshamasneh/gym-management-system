from celery import shared_task

from gym_management.settings import QUEUE_URL
from services.aws_services.handlers import get_handler_for_event
from services.aws_services.service import ServiceFactory


@shared_task
def poll_sqs_queue():
    sqs = ServiceFactory.get_sqs_service(QUEUE_URL)
    messages = sqs.receive_messages()

    if messages:
        print(f"Messages received: {messages}")
        for message in messages:
            process_sqs_message(message)
    else:
        print("No messages in the queue.")

@shared_task
def process_sqs_message(message):
    import json
    sqs = ServiceFactory.get_sqs_service(QUEUE_URL)
    try:
        sns_message = json.loads(message.get('Body', '{}'))
        sns_inner_message = json.loads(sns_message.get('Message', '{}'))

        event_code = sns_inner_message.get('code')
        event_data = sns_inner_message.get('data', {})

        handler = get_handler_for_event(event_code)
        if handler:
            handler.handle_message(event_data)
            sqs.delete_message(message['ReceiptHandle'])
        else:
            print(f"No handler found for event code: {event_code}")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Failed to process message: {e}")
