from common.aws.boto_sessions.session_manager import SessionManager

class SQSService:
    def __init__(self, queue_url):
        self.sqs_client = SessionManager.get_client('sqs')
        self.queue_url = queue_url

    def receive_messages(self, max_number=10, wait_time=20):
        response = self.sqs_client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=max_number,
            WaitTimeSeconds=wait_time
        )
        return response.get('Messages', [])

    def send_message(self, message_body, message_attributes=None):
        self.sqs_client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message_body,
            MessageAttributes=message_attributes or {}
        )

    def delete_message(self, receipt_handle):
        self.sqs_client.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle
        )

    def purge_queue(self):
        self.sqs_client.purge_queue(QueueUrl=self.queue_url)
