import unittest
from unittest.mock import MagicMock, patch
from src.autonomous_agent import AutonomousAgent
from src.agent import Agent

class TestAutonomousAgent(unittest.TestCase):

    @patch("web3.Web3")
    def setUp(self, MockWeb3):
        # Mock the Web3 connection
        self.mock_w3 = MockWeb3.return_value
        self.mock_w3.is_connected.return_value = True
        self.mock_w3.eth.contract.return_value = MagicMock()
        
        self.agent_name = "TestAgent"
        self.agent = AutonomousAgent(self.agent_name)

    def test_initialization(self):
        self.assertEqual(self.agent.get_name(), self.agent_name)
        self.assertTrue(self.agent.w3.is_connected())
        self.assertIsNotNone(self.agent.token_contract)
        
    def test_message_handling(self):
        # Mock handlers
        mock_hello_handler = MagicMock()
        mock_crypto_handler = MagicMock()

        self.agent.register_handler("hello", mock_hello_handler)
        self.agent.register_handler("crypto", mock_crypto_handler)

        # Send a "hello" message
        message = {"type": "hello", "content": "Hello, World!"}
        self.agent.inbox.put(message)
        self.agent.process_messages()

        # Assert handler was called
        mock_hello_handler.assert_called_once_with(message)

        # Send a "crypto" message
        message = {"type": "crypto", "content": "Crypto is cool!"}
        self.agent.inbox.put(message)
        self.agent.process_messages()

        # Assert handler was called
        mock_crypto_handler.assert_called_once_with(message)

    @patch("asyncio.sleep", return_value=None)  # To speed up tests
    def test_random_word_gen_behaviour(self, _):
        with patch.object(self.agent, "send_outbox_message") as mock_send_message:
            asyncio.run(self.agent.random_word_gen_behaviour())
            mock_send_message.assert_called_once()
            call_args = mock_send_message.call_args[0][0]
            self.assertIn(call_args["type"], ["message"] + self.agent.WORDS_TO_FIND)

    @patch("asyncio.sleep", return_value=None)
    def test_start(self, _):
        # Mock behaviors to avoid running real async tasks
        mock_behaviour = MagicMock(return_value=None)
        self.agent.register_behaviour(mock_behaviour)

        # Mock the event loop
        with patch("asyncio.new_event_loop") as mock_loop:
            loop = MagicMock()
            mock_loop.return_value = loop

            self.agent.start()
            self.assertTrue(loop.create_task.called)

    @patch("web3.Web3.HTTPProvider")
    def test_web3_connection_failure(self, MockHTTPProvider):
        MockHTTPProvider.return_value = MagicMock()
        MockHTTPProvider.return_value.is_connected.return_value = False
        with self.assertRaises(SystemExit):
            AutonomousAgent("FailAgent")

if __name__ == "__main__":
    unittest.main()