from abc import ABC

from gym_app.handlers.base_handler import SQSHandlerABC


class EntityRemovedHandler(SQSHandlerABC, ABC):
    _CODE = 'entity_removed'

    @staticmethod
    def process_sqs_message(message):
        gym_id = message.get('gym_id')
        print(f"Gym removed with ID: {gym_id}")