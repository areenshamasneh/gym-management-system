import unittest
from unittest.mock import patch

from gym_app.management.scripts.sqs_listener import lambda_handler, listen_to_queue


class TestSqsListener(unittest.TestCase):

    @patch('gym_app.management.scripts.sqs_listener.sqs')
    def test_lambda_handler(self, mock_sqs):
        mock_message = {
            'Body': '{"key": "value"}'
        }
        event = {'Records': [mock_message]}

        with patch('gym_app.management.scripts.sqs_listener.process_message') as mock_process_message:
            lambda_handler(event, None)
            mock_process_message.assert_called_once_with('{"key": "value"}')

    @patch('gym_app.management.scripts.sqs_listener.sqs')
    def test_listen_to_queue(self, mock_sqs):
        mock_sqs.receive_message.return_value = {
            'Messages': [{'Body': '{"key": "value"}', 'ReceiptHandle': 'dummy_receipt_handle'}]
        }

        actual_queue_url = 'http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/TestQueue'

        with patch('gym_app.management.scripts.sqs_listener.process_message') as mock_process_message:
            with patch('gym_app.management.scripts.sqs_listener.sqs.delete_message') as mock_delete_message:
                listen_to_queue(max_iterations=1)

                mock_process_message.assert_called_once_with('{"key": "value"}')

                mock_delete_message.assert_called_once_with(
                    QueueUrl=actual_queue_url,
                    ReceiptHandle='dummy_receipt_handle'
                )


if __name__ == '__main__':
    unittest.main()
