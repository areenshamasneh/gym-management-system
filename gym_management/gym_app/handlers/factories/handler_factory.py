from gym_app.handlers import EntityAddedHandler, EntityUpdatedHandler, EntityRemovedHandler

class HandlerFactory:
    _handlers = {
        'entity_added': EntityAddedHandler,
        'entity_updated': EntityUpdatedHandler,
        'entity_removed': EntityRemovedHandler,
    }

    @classmethod
    def get_handler(cls, event_code, sqs_message, message_code, message_data):
        handler_class = cls._handlers.get(event_code)
        if handler_class:
            return handler_class(sqs_message, message_code, message_data)
        else:
            raise ValueError(f"No handler found for event code: {event_code}")
