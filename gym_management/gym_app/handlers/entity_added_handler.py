from abc import ABC

from gym_app.handlers.base_handler import SQSHandlerABC


class EntityAddedHandler(SQSHandlerABC, ABC):
    _CODE = 'entity_added'

    @staticmethod
    def process_sqs_message(message):
        gym_data = message.get('data', {})
        print(f"Gym added with data: {gym_data}")
