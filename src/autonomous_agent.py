import random
import asyncio
from web3 import Web3
from .logger import logger
from .utils.abi import ERC20_ABI
from .config.settings import MESSAGE_WORDS, ETH_SETTINGS, WORDS_TO_FIND
from .token_operation import get_erc20_balance_behaviour
from .handlers import hello_filter_handler, crypto_filter_handler
from .agent import Agent

class AutonomousAgent(Agent):
    def __init__(self, agent_name):
        super().__init__(agent_name)
        self.w3 = Web3(Web3.HTTPProvider(ETH_SETTINGS["RPC_NODE_URL"]))
        if not self.w3.is_connected():
            print("Web3 connection failed. Exiting...")
            exit(1)
        self.token_contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(ETH_SETTINGS["TOKEN_ADDRESS"]),
            abi=ERC20_ABI,
        )
        self.token_decimals = self.token_contract.functions.decimals().call()
        self.register_handler("hello", lambda message: hello_filter_handler(self, message))
        self.register_handler("crypto", lambda message: crypto_filter_handler(self, message))

    async def random_word_gen_behaviour(self):
        while True:
            words = random.sample(MESSAGE_WORDS, 2)
            logger.info(f"{self.name}:: Words selected: {words}")
            message = " ".join(words)
            type = "message"
            for word in WORDS_TO_FIND:
                if word in message:
                    type = word
                    break
            await self.send_outbox_message({"type": type, "content": message})
            await asyncio.sleep(2)

    async def start(self):
        # Register behaviors
        self.register_behaviour(self.random_word_gen_behaviour, "random_word_gen")
        self.register_behaviour(lambda: get_erc20_balance_behaviour(self), "get_erc20_balance")

        # Start all behaviors as asyncio tasks
        tasks = [asyncio.create_task(behaviour()) for behaviour in self.behaviours]
        await asyncio.gather(*tasks)
