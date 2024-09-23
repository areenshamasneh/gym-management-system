from gym_management.settings import AWS
from services.aws.sns_service import SNSService


class NotificationService:
    def __init__(self):
        self.sns_services = {}

    def publish_event(self, event_code, message_body):
        topic_arn = self.get_topic_arn(event_code)
        if not topic_arn:
            raise ValueError(f"No topic ARN found for event code: {event_code}")

        sns_service = self.get_sns_service(topic_arn)
        sns_service.publish_event(event_code, message_body)

    @staticmethod
    def get_topic_arn(event_code):
        return AWS['sns'].get(event_code)

    def get_sns_service(self, topic_arn):
        if topic_arn not in self.sns_services:
            self.sns_services[topic_arn] = SNSService(topic_arn)
        return self.sns_services[topic_arn]
