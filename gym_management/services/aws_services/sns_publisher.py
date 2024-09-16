import json
import boto3 # type: ignore
from gym_management.settings import LOCALSTACK_URL, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, AWS_REGION

class SNSPublisher:
    def __init__(self):
        self.sns_client = boto3.client(
            'sns',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            endpoint_url=LOCALSTACK_URL
        )

    def publish_event(self, topic_arn, event_code, event_data):
        message = {
            'code': event_code,
            'data': event_data
        }
        response = self.sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(message)
        )
        print(f"Published event: {event_code} with data: {event_data}")
        return response
