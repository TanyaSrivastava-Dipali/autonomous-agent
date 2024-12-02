import unittest
from threading import Thread
from queue import Queue
from unittest.mock import patch,call
from src.autonomous_agent import AutonomousAgent


class TestAutonomousAgent(unittest.TestCase):
    def setUp(self):
        # Create inbox and outbox for testing
        self.inbox = Queue()
        self.outbox = Queue()

        # Initialize the agent
        self.agent = AutonomousAgent("TestAgent")
        self.agent.inbox = self.inbox
        self.agent.outbox = self.outbox

        # Start the agent's inbox processing in a separate thread
        Thread(target=self.agent.process_messages, daemon=True).start()

    @patch("src.handlers.logger.info")
    def test_hello_handler(self, mock_logger_info):
        # Send a message to trigger the "hello" handler
        message = {"type": "hello", "content": "hello world"}
        self.inbox.put(message)

        # Allow some time for the message to be processed
        self.inbox.join()

        # Assert that the logger.info was called correctly
        mock_logger_info.assert_any_call("Filtered message (hello):")

    @patch("src.handlers.logger.info")
    @patch("src.token_operation.transfer_erc20_token")
    def test_crypto_handler(self, mock_transfer_erc20_token, mock_logger_info):
        # Mock the transfer_erc20_token function
        mock_transaction_hash = "0x9af63e625bd695c922cba4fdf1cd3475974ed0b636d4d518096701b9f90f012a"
        mock_transfer_erc20_token.return_value = mock_transaction_hash

        # Send a message to trigger the "crypto" handler
        message = {"type": "crypto", "content": "crypto transfer"}
        self.inbox.put(message)

        # Allow some time for the message to be processed
        self.inbox.join()

        # Assert that the logger.info was called with the correct message
        mock_logger_info.assert_has_calls([call("TestAgent:: Message found: {'type': 'crypto', 'content': 'crypto transfer'}"),
        call('TestAgent::Initiating ERC-20 token transfer...'),
        call(f'TestAgent::Transaction sent with hash: {mock_transaction_hash}'),
        call('TestAgent:: Checking inbox for messages...')])

        # Assert that the transfer_erc20_token function was called once
        mock_transfer_erc20_token.assert_called_once_with(self.agent)

# This block ensures the test can be run standalone
if __name__ == "__main__":
    unittest.main()