from gym_management.settings import AWS
from services.aws.sns_service import SNSService

class GymSNSComponent:
    def __init__(self):
        from gym_app.components.sns.sns_component import SNSComponent
        sns_service = SNSService(topic_arn=AWS['sns']['GYM_NOTIFICATIONS'])
        self.sns_component = SNSComponent(sns_service=sns_service)

    def notify_gym_created(self, gym_id, data):
        code = 'entity_added'
        message_body = {'gym_id': gym_id, 'data': data}
        self.sns_component.publish_event(code, message_body)

    def notify_gym_updated(self, gym_id, data):
        code = 'entity_updated'
        message_body = {'gym_id': gym_id, 'data': data}
        self.sns_component.publish_event(code, message_body)

    def notify_gym_deleted(self, gym_id):
        code = 'entity_removed'
        message_body = {'gym_id': gym_id}
        self.sns_component.publish_event(code, message_body)
