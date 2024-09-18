from gym_management.settings import TOPIC_ENTITY_ADDED_ARN, TOPIC_ENTITY_UPDATED_ARN
from services.aws_services.sns_publisher import SNSPublisher


class MessageService:
    def __init__(self):
        self.publisher = SNSPublisher()

    def publish_event(self, event_code, event_data):
        if self.publisher:
            topic_map = {
                'entity_added': TOPIC_ENTITY_ADDED_ARN,
                'entity_updated': TOPIC_ENTITY_UPDATED_ARN
            }
            topic_arn = topic_map.get(event_code)

            if topic_arn:
                self.publisher.publish_event(topic_arn, event_code, event_data)
