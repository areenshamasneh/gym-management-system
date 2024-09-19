from abc import ABC, abstractmethod

class SQSHandlerABC(ABC):
    _CODE = None
    _DELETE_AFTER = True  # Control whether to delete message after processing

    def __init__(self, sqs_message, message_code, message_data):
        self.sqs_message = sqs_message
        self.message_code = message_code
        self.message_data = message_data

    @classmethod
    def get_code(cls):
        return cls._CODE

    def handle(self):
        self._process_sqs_message()

        if self._DELETE_AFTER:
            self.sqs_message.delete()

    @abstractmethod
    def _process_sqs_message(self):
        raise NotImplementedError("Subclasses must implement `_process_sqs_message`.")
