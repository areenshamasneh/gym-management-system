from common.threads.thread import get_request_id

class SNSComponent:
    def __init__(self, sns_service):
        self.sns_service = sns_service

    def _build_message_attributes(self, code):
        return {
            'EventCode': {
                'DataType': 'String',
                'StringValue': code
            },
            'RequestId': {
                'DataType': 'String',
                'StringValue': get_request_id()
            }
        }

    def _build_message(self, code, message_body):
        return {
            'code': code,
            'data': message_body,
        }

    def _publish_message(self, code, message_body):
        message = self._build_message(code, message_body)
        message_attributes = self._build_message_attributes(code)
        self.sns_service.publish_event(
            event_code=code,
            message=message,
            message_attributes=message_attributes
        )

    def publish_event(self, code, data):
        self._publish_message(code, data)
