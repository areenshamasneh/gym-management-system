import json

from celery import shared_task

from gym_app.handlers.factories import HandlerFactory
from gym_management.settings import AWS
from services.aws.sqs_service import SQSService


@shared_task
def poll_sqs_queues():
    for queue_name, queue_url in AWS['sqs'].items():
        sqs_service = SQSService(queue_url)
        messages = sqs_service.receive_messages()

        if messages:
            for message in messages:
                process_sqs_message.apply_async(
                    args=(queue_name, message)
                )


@shared_task(bind=True, max_retries=3)
def process_sqs_message(self, queue_name, sqs_message):
    try:
        print(f"Original SQS Message: {sqs_message}")
        if isinstance(sqs_message, str):
            sqs_message = json.loads(sqs_message)

        sns_message = sqs_message.get('Body', '{}')
        print(f"Parsed SNS message (from Body): {sns_message}")

        sns_message = json.loads(sns_message)

        sns_inner_message = sns_message.get('Message')

        if sns_inner_message and isinstance(sns_inner_message, str):
            sns_inner_message = json.loads(sns_inner_message)

        print(f"Parsed SNS Inner Message: {sns_inner_message}")

        event_code = sns_inner_message.get('code')
        event_data = sns_inner_message.get('data', {})

        if not event_code:
            raise ValueError("Missing 'code' in the SNS message")

        handler = HandlerFactory.get_handler(event_code, sqs_message, event_code, event_data)
        handler.handle(sqs_message['ReceiptHandle'], queue_name)

    except json.JSONDecodeError as e:
        self.retry(exc=e, countdown=60)
        print(f"JSON parsing error: {e}, message body: {sqs_message}")
    except KeyError as e:
        self.retry(exc=e, countdown=60)
        print(f"KeyError: {e}, queue_name: {queue_name}")
    except TypeError as e:
        self.retry(exc=e, countdown=60)
        print(f"TypeError: {e}, message body: {sqs_message}")
    except Exception as exc:
        self.retry(exc=exc, countdown=60)
        print(f"General error: {exc}, message body: {sqs_message}")
