import json
from common.aws.boto_sessions.session_manager import SessionManager
from gym_management.settings import AWS

class SNSService:
    def __init__(self):
        self.sns_client = SessionManager.get_client('sns')

    def publish_event(self, event_code, message_body, message_attributes=None):
        if not message_attributes:
            message_attributes = self.build_attributes(event_code)
        else:
            message_attributes = {}
        message = self.build_message(event_code, message_body)
        topic_arn = self.get_topic_arn(event_code)
        self.sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(message),
            MessageAttributes=message_attributes
        )

    @staticmethod
    def build_message(event_code, message_body):
        message = {
            'code': event_code,
            'data': message_body,
        }
        return message

    @staticmethod
    def get_topic_arn(event_code):
        return AWS['sns'].get(event_code)

    @staticmethod
    def build_attributes(event_code):
        return {
            'EventCode': {
                'DataType': 'String',
                'StringValue': event_code
            }
        }
