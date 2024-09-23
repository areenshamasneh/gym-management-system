from gym_app.handlers.base_handler import SQSHandlerABC


class EntityAddedHandler(SQSHandlerABC):
    _CODE = 'entity_added'

    def _process_sqs_message(self):
        data = self.message_data
        print(f"Entity updated with data: {data}")
