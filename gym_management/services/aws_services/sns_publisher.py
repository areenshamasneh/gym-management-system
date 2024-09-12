import json

import boto3

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
        self.topic_arn = self.load_topic_arn()

    @staticmethod
    def load_topic_arn():
        try:
            with open('config.json') as config_file:
                config = json.load(config_file)
            return config.get('TOPIC_ARN')
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading topic ARN from config file: {e}")
            raise

    def publish_event(self, event_type, event_data):
        message = {
            'eventType': event_type,
            'data': event_data
        }
        response = self.sns_client.publish(
            TopicArn=self.topic_arn,
            Message=json.dumps(message)
        )
        print(f"Published event: {event_type} with data: {event_data}")
        return response
