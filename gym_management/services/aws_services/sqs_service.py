import json
import boto3 # type: ignore
from gym_management.settings import LOCALSTACK_URL, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, AWS_REGION

class SQSService:
    def __init__(self, queue_url=None):
        self.sqs = boto3.client(
            'sqs',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            endpoint_url=LOCALSTACK_URL
        )
        self.queue_url = queue_url

    def get_queue_url(self, queue_name):
        try:
            response = self.sqs.get_queue_url(QueueName=queue_name)
            self.queue_url = response['QueueUrl']
            print(f"Queue URL retrieved: {self.queue_url}")
            return self.queue_url
        except Exception as e:
            print(f"Failed to retrieve queue URL: {e}")
            raise

    def receive_messages(self, max_number_of_messages=10):
        if not self.queue_url:
            raise ValueError("Queue URL not set. Please set it before receiving messages.")

        response = self.sqs.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=max_number_of_messages,
            WaitTimeSeconds=20
        )
        return response.get('Messages', [])

    def delete_message(self, receipt_handle):
        if not self.queue_url:
            raise ValueError("Queue URL not set. Please set it before deleting messages.")
        self.sqs.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle
        )
        print("Message deleted from the queue.")
