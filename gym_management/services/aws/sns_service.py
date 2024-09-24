import json

from common.aws.boto_sessions.session_manager import get_boto_client


class SNSService:
    def __init__(self, topic_arn):
        self.sns_client = get_boto_client('sns')
        self.topic_arn = topic_arn

    def publish_event(self, event_code, message, message_attributes=None):
        message_attributes = message_attributes or {}
        self.sns_client.publish(
            TopicArn=self.topic_arn,
            Message=json.dumps(message),
            MessageAttributes=message_attributes
        )
