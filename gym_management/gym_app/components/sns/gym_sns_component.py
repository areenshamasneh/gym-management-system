from gym_app.components.sns.sns_component import SNSComponent
from gym_management.settings import AWS
from services.aws.sns_service import SNSService


class GymSNSComponent(SNSComponent):
    def __init__(self):
        sns_service = SNSService(topic_arn=AWS['sns']['GYM_NOTIFICATIONS'])
        super().__init__(sns_service)

    def notify_gym_created(self, gym_id, data):
        code = 'entity_added'
        message_body = {'gym_id': gym_id, 'data': data}
        self.publish_event(code, message_body)

    def notify_gym_updated(self, gym_id, data):
        code = 'entity_updated'
        message_body = {'gym_id': gym_id, 'data': data}
        self.publish_event(code, message_body)

    def notify_gym_deleted(self, gym_id):
        code = 'entity_removed'
        message_body = {'gym_id': gym_id}
        self.publish_event(code, message_body)
