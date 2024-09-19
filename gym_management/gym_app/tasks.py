import json
from celery import shared_task
from gym_app.handlers import HandlerFactory
from gym_management.settings import AWS
from services.aws.sqs_service import SQSService

@shared_task
def poll_sqs_queues():
    for queue_name, queue_url in AWS['sqs'].items():
        sqs_service = SQSService(queue_url)
        messages = sqs_service.receive_messages()

        if messages:
            for message in messages:
                process_sqs_message.apply_async(args=(queue_name, message['Body'], message['ReceiptHandle']))

@shared_task(bind=True, max_retries=3)
def process_sqs_message(self, queue_name, message_body, receipt_handle):
    sqs_service = SQSService(AWS['sqs'][queue_name])
    try:
        sns_message = json.loads(message_body)
        event_code = sns_message.get('code')
        handler = HandlerFactory.get_handler(event_code)
        handler.handle(sns_message.get('data', {}))
        sqs_service.delete_message(receipt_handle)
    except Exception as exc:
        self.retry(exc=exc, countdown=60)
