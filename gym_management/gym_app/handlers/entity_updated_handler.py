from gym_app.handlers.base_handler import SQSHandlerABC


class EntityUpdatedHandler(SQSHandlerABC):
    _CODE = 'entity_updated'

    def _process_sqs_message(self):
        gym_data = self.message_data
        print(f"Gym updated with data: {gym_data}")
