import boto3 # type: ignore

from gym_management.settings import LOCALSTACK_URL, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, AWS_REGION


class SQSService:
    def __init__(self, queue_url):
        self.queue_url = queue_url
        self.sqs = boto3.client(
            'sqs',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            endpoint_url=LOCALSTACK_URL
        )

    def receive_messages(self, max_number_of_messages=10):
        response = self.sqs.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=max_number_of_messages,
            WaitTimeSeconds=10
        )
        return response.get('Messages', [])

    def delete_message(self, receipt_handle):
        self.sqs.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle
        )
        print("Message deleted from the queue.")

    def purge_queue(self):
        self.sqs.purge_queue(QueueUrl=self.queue_url)