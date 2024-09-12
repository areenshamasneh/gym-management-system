import json
import boto3 # type: ignore
import time
from gym_management.settings import LOCALSTACK_URL, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, AWS_REGION

with open('config.json') as config_file:
    config = json.load(config_file)

QUEUE_URL = config.get('QUEUE_URL')

sqs = boto3.client(
    'sqs',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    endpoint_url=LOCALSTACK_URL
)

def process_message(message_body):
    try:
        message_json = json.loads(message_body)
        print("Processing message:")
        print(json.dumps(message_json, indent=4))
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        print(f"Message body: {message_body}")

def listen_to_queue():
    print("Listening to SQS queue...")
    while True:
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )

        messages = response.get('Messages', [])

        if messages:
            for message in messages:
                process_message(message['Body'])
                sqs.delete_message(
                    QueueUrl=QUEUE_URL,
                    ReceiptHandle=message['ReceiptHandle']
                )
                print("Message processed and deleted from the queue.")
        else:
            print("No messages available. Waiting...")

        time.sleep(5)

if __name__ == "__main__":
    if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, LOCALSTACK_URL, QUEUE_URL]):
        raise ValueError("One or more environment variables are not set.")
    listen_to_queue()
