import random
import asyncio
from web3 import Web3
from functools import partial
from .logger import logger
from .utils.abi import ERC20_ABI
from .config.settings import MESSAGE_WORDS, ETH_SETTINGS,WORDS_TO_FIND
from .token_operation import get_erc20_balance_behaviour
from .handlers import hello_filter_handler
from .agent import Agent



class AutonomousAgent(Agent):

    def __init__(self,agent_name):
        super().__init__(agent_name)
        self.w3 =Web3(Web3.HTTPProvider(ETH_SETTINGS["RPC_NODE_URL"]))
        if not self.w3.is_connected():
            print("Web3 connection failed. Exiting...")
            exit(1)
        self.token_contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(ETH_SETTINGS["TOKEN_ADDRESS"]),
            abi=ERC20_ABI,
        )
        self.register_handler("hello", hello_filter_handler)
        self.register_handler("crypto",self.crypto_filter_handler)
      
        # self.register_handler("crypto",lambda message:crypto_filter_handler(self))

        
    async def random_word_gen_behaviour(self):
        while True:
            words = random.sample(MESSAGE_WORDS, 2)
            logger.info(f"Words selected: {words}")
            message = " ".join(words)
            type = "message"
            for i in range(len(WORDS_TO_FIND)):
                if WORDS_TO_FIND[i] in message:
                    type = WORDS_TO_FIND[i]
                    break 
            self.send_outbox_message({"type": type, "content": message})
            await asyncio.sleep(2)

    def crypto_filter_handler(self,message):
        logger.info(f"{self.name}::Initiating ERC-20 token transfer...")
        self.transfer_erc20_token()

    def transfer_erc20_token(self):
        try:
            w3 = Web3(Web3.HTTPProvider(ETH_SETTINGS["RPC_NODE_URL"]))
            if not w3.is_connected():
                logger.error("Web3 is not connected.")
                return None
            balance = self.token_contract.functions.balanceOf(
            w3.to_checksum_address(ETH_SETTINGS["FROM_ADDRESS"])
            ).call()
            token_to_transfer = 1 * 10 ** (self.token_contract.functions.decimals().call())
            if balance >= token_to_transfer:
                nonce = w3.eth.get_transaction_count(ETH_SETTINGS["FROM_ADDRESS"])

                txn = self.token_contract.functions.transfer(
                    ETH_SETTINGS["TO_ADDRESS"], token_to_transfer
                ).build_transaction(
                    {
                        "chainId": w3.eth.chain_id,
                        "gas": 2000000,
                        "gasPrice": self.w3.eth.gas_price,
                        "nonce": nonce,
                    }
                )

                signed_txn = w3.eth.account.sign_transaction(
                    txn, private_key=ETH_SETTINGS["PRIVATE_KEY"]
                )
                tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
                logger.info(f"{self.name}::Transaction sent with hash: {tx_hash.hex()}")
                return tx_hash.hex()
            else:
                logger.info("Insufficient tokens to transfer.")
        except Exception as e:
            logger.error(f"Error transferring token: {e}")
            return None

    
    def start(self):
        # Set up a new event loop for asynchronous tasks
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Register behaviors
        self.register_behaviour(self.random_word_gen_behaviour,"random_word_gen")
        self.register_behaviour(lambda:get_erc20_balance_behaviour(self),"get_erc20_balance")

        # Schedule registered behaviors to run concurrently
        tasks = [loop.create_task(behaviour()) for behaviour in self.behaviours]
  
        # Keep the event loop running until all tasks are complete (or indefinitely)
        loop.run_until_complete(asyncio.gather(*tasks))
