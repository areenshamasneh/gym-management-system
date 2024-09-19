from abc import ABC

from gym_app.handlers.base_handler import SQSHandlerABC


class EntityUpdatedHandler(SQSHandlerABC, ABC):
    @staticmethod
    def process_sqs_message(message):
        gym_data = message.get('data', {})
        print(f"Gym updated with data: {gym_data}")
