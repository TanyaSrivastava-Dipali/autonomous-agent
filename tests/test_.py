import unittest
from threading import Thread
from queue import Queue
from unittest.mock import patch,call,MagicMock
from unittest import IsolatedAsyncioTestCase
import asyncio
from src.token_operation import get_erc20_balance_behaviour
from src.handlers import crypto_filter_handler
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
        print("Executing test_hello_handler...")
        # Send a message to trigger the "hello" handler
        message = {"type": "hello", "content": "hello world"}
        self.inbox.put(message)

        # Allow some time for the message to be processed
        self.inbox.join()

        # Assert that the logger.info was called correctly
        mock_logger_info.assert_any_call("TestAgent:: Filtered message (hello):")

    @patch("src.handlers.logger.info")  # Mock the logger
    @patch("src.token_operation.transfer_erc20_token")  # Mock the transfer function
    def test_crypto_handler(self, mock_transfer_erc20_token, mock_logger_info):
        print("Executing test_crypto_handler...")
        # Set up mock return value for the transfer function
        mock_transaction_hash = "0x9af63e625bd695c922cba4fdf1cd3475974ed0b636d4d518096701b9f90f012a"
        mock_transfer_erc20_token.return_value = mock_transaction_hash

        # Create a mock agent with required attributes
        mock_agent = MagicMock()
        mock_agent.name = "TestAgent"
        mock_agent.w3 = MagicMock()  # Mock the Web3 connection
        mock_agent.w3.eth.get_balance.return_value = 2000000000000000000  # Return 2 ETH
        mock_agent.w3.eth.send_raw_transaction.return_value = MagicMock(
            hex=MagicMock(return_value=mock_transaction_hash)
        )  # Mock transaction hash

        # Mock the token contract behavior
        mock_agent.token_contract = MagicMock()
        mock_agent.token_contract.functions.decimals.return_value.call.return_value = 18  # Token has 18 decimals
        mock_agent.token_contract.functions.balanceOf.return_value.call.return_value = 1000000000000000000  # 1 Token

        # Define a message to process
        message = {"type": "crypto", "content": "crypto transfer"}

        # Call the handler
        crypto_filter_handler(mock_agent, message)

        # Verify logger calls
        mock_logger_info.assert_has_calls([
            call("TestAgent:: Initiating ERC-20 token transfer..."),
            call(f"TestAgent:: Transaction sent with hash: {mock_transaction_hash}"),
        ])
        
class TestERC20BalanceBehaviour(IsolatedAsyncioTestCase):
    @patch("src.autonomous_agent.Web3")  # Mock Web3
    @patch("src.token_operation.logger.info")  # Mock logger
    async def test_get_erc20_balance_behaviour(self, mock_logger_info, mock_web3):
        print("Executing test_erc_20_balance_behaviour...")
        # Mock ETH_SETTINGS using patch.dict
        with patch.dict(
            "src.config.settings.ETH_SETTINGS",
            {"FROM_ADDRESS": "0xMockedAddress", "TOKEN_ADDRESS": "0xMockedTokenAddress", "RPC_NODE_URL": "https://mocked.node.url"},
        ):
            # Mock the Web3 connection
            mock_web3.return_value.is_connected.return_value = True

            # Mock the token contract
            mock_token_contract = MagicMock()
            mock_token_contract.functions.balanceOf.return_value.call.return_value = 1000000000000000000
            mock_token_contract.functions.decimals.return_value.call.return_value = 18
            mock_web3.return_value.eth.contract.return_value = mock_token_contract

            # Mock the agent
            mock_agent = MagicMock(spec=AutonomousAgent)
            mock_agent.name = "TestAgent"
            mock_agent.token_contract = mock_token_contract

            # Simulate the behavior's execution for one loop
            with patch("asyncio.sleep", side_effect=asyncio.CancelledError):
                try:
                    await get_erc20_balance_behaviour(mock_agent)
                except asyncio.CancelledError:
                    pass  # Exit after one iteration

            # Verify balanceOf was called with the mocked address
            mock_token_contract.functions.balanceOf.assert_called_once_with("0xMockedAddress")

            # Verify decimals was called
            mock_token_contract.functions.decimals.assert_called_once()

            # Verify logger was called with the correct balance
            mock_logger_info.assert_called_once_with(
                "TestAgent:: ERC-20 Token Balance for address 0xMockedAddress: 1.0"
            )

# class TestERC20BalanceBehaviour(IsolatedAsyncioTestCase):
#     @patch("src.token_operation.logger.info")
#     async def test_get_erc20_balance_behaviour(self, mock_logger_info):

#         # Mock agent setup
#         mock_agent = MagicMock(spec=AutonomousAgent)
#         mock_agent.name = "TestAgent"

#         # Mock token contract behaviour
#         mock_agent.token_contract = MagicMock()
#         mock_agent.token_contract.functions.balanceOf.return_value.call.return_value = 1000000000000000000
#         mock_agent.token_contract.functions.decimals.return_value.call.return_value = 18

#         # Simulate the behavior's execution for one loop
#         with patch("asyncio.sleep", side_effect=asyncio.CancelledError):
#             try:
#                 await get_erc20_balance_behaviour(mock_agent)
#             except asyncio.CancelledError:
#                 pass  # Exit after one iteration

#         # Verify balanceOf was called with the correct address
#         mock_agent.token_contract.functions.balanceOf.assert_called_once_with("0x5B38Da6a701c568545dCfcB03FcB875f56beddC4")

#         # Verify decimals was called
#         mock_agent.token_contract.functions.decimals.assert_called_once()

#         # Verify logger was called with the correct balance
#         mock_logger_info.assert_called_once_with(
#             "TestAgent::ERC-20 Token Balance for address 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4: 1.0"
#         )

# This block ensures the test can be run standalone
if __name__ == "__main__":
    unittest.main()