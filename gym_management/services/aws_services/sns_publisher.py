import json

import boto3  # type: ignore

from services.aws_services.aws_config import AWSConfig


class SNSPublisher:
    def __init__(self):
        self.sns_client = AWSConfig.get_sns_client()

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
