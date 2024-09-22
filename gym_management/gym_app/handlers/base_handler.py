from abc import ABC, abstractmethod

from gym_management.settings import AWS
from services.aws.sqs_service import SQSService


class SQSHandlerABC(ABC):
    _CODE = None
    _DELETE_AFTER = True  # Control whether to delete message after processing

    def __init__(self, sqs_message, message_code, message_data):
        self.sqs_message = sqs_message
        self.message_code = message_code
        self.message_data = message_data
        self.sqs_service = None

    @classmethod
    def get_code(cls):
        return cls._CODE

    def handle(self, receipt_handle, queue_name):
        self._process_sqs_message()
        self.sqs_service = SQSService(AWS['sqs'][queue_name])

        if self._DELETE_AFTER:
            print(f"Deleting message with ReceiptHandle: {receipt_handle}")
            self.sqs_service.delete_message(receipt_handle)

    @abstractmethod
    def _process_sqs_message(self):
        raise NotImplementedError("Subclasses must implement `_process_sqs_message`.")
