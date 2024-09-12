import json


class BaseMessageHandler:
    def handle_message(self, entity_type, data):
        print(f"Handling event for entity: {entity_type}")
        print(json.dumps(data, indent=4))


class EntityAddedHandler(BaseMessageHandler):
    def handle_message(self, entity_type, data):
        print(f"Handling {entity_type} added event:")
        print(json.dumps(data, indent=4))


class EntityUpdatedHandler(BaseMessageHandler):
    def handle_message(self, entity_type, data):
        print(f"Handling {entity_type} updated event:")
        print(json.dumps(data, indent=4))


def get_handler_for_event(event_type):
    handlers = {
        'entity_added': EntityAddedHandler(),
        'entity_updated': EntityUpdatedHandler(),
    }
    return handlers.get(event_type)
