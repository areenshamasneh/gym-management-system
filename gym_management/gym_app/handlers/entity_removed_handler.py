from gym_app.handlers.base_handler import SQSHandlerABC


class EntityRemovedHandler(SQSHandlerABC):
    _CODE = 'entity_removed'

    def _process_sqs_message(self):
        print(f"Entity removed")
