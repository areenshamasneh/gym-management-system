import json

class BaseMessageHandler:
    def handle_message(self, data):
        print(f"Handling event:")
        print(json.dumps(data, indent=4))

class EntityAddedHandler(BaseMessageHandler):
    def handle_message(self, data):
        print(f"Handling entity added event:")
        print(json.dumps(data, indent=4))

class EntityUpdatedHandler(BaseMessageHandler):
    def handle_message(self, data):
        print(f"Handling entity updated event:")
        print(json.dumps(data, indent=4))

def get_handler_for_event(event_code):
    handlers = {
        'entity_added': EntityAddedHandler(),
        'entity_updated': EntityUpdatedHandler(),
    }
    return handlers.get(event_code)
