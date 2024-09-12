import json
from gym_management.settings import LOCALSTACK_URL, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, AWS_REGION
import boto3 # type: ignore

with open('config.json') as config_file:
    config = json.load(config_file)

TOPIC_ARN = config.get('TOPIC_ARN')

sns = boto3.client(
    'sns',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    endpoint_url=LOCALSTACK_URL
)

def publish_message_to_sns(message):
    sns.publish(
        TopicArn=TOPIC_ARN,
        Message=message
    )
    print(f"Message sent to SNS: {message}")

if __name__ == "__main__":
    if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, LOCALSTACK_URL, TOPIC_ARN]):
        raise ValueError("One or more environment variables are not set.")
    publish_message_to_sns("Hello, this is a message from SNS!")
