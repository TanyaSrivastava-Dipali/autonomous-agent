import asyncio
from .logger import logger
from .config.settings import  ETH_SETTINGS

async def get_erc20_balance_behaviour(agent):
    while True:
        add=ETH_SETTINGS["FROM_ADDRESS"]
        balance = agent.token_contract.functions.balanceOf(ETH_SETTINGS["FROM_ADDRESS"]).call()
        dec = agent.token_contract.functions.decimals().call()
        balance_in_tokens = balance / (10**dec)
        logger.info(f"{agent.name}:: ERC-20 Token Balance for address {add}: {balance_in_tokens}")
        await asyncio.sleep(10)  # Add a 10-second delay before checking balance again

def transfer_erc20_token(self):
    try:
        if not self.w3.is_connected():
            logger.error("Web3 is not connected.")
            return None
        balance = self.token_contract.functions.balanceOf(
        self.w3.to_checksum_address(ETH_SETTINGS["FROM_ADDRESS"])
        ).call()
        token_to_transfer = 1 * 10 ** (self.token_contract.functions.decimals().call())
        if balance >= token_to_transfer:
            nonce = self.w3.eth.get_transaction_count(ETH_SETTINGS["FROM_ADDRESS"])

            txn = self.token_contract.functions.transfer(
                ETH_SETTINGS["TO_ADDRESS"], token_to_transfer
            ).build_transaction(
                {
                    "chainId": self.w3.eth.chain_id,
                    "gas": 2000000,
                    "gasPrice": self.w3.eth.gas_price,
                    "nonce": nonce,
                }
            )

            signed_txn = self.w3.eth.account.sign_transaction(
                txn, private_key=ETH_SETTINGS["PRIVATE_KEY"]
            )
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            logger.info(f"{self.name}:: Transaction sent with hash: {tx_hash.hex()}")
            return tx_hash.hex()
        else:
            logger.info("Insufficient tokens to transfer.")
    except Exception as e:
        logger.error(f"Error transferring token: {e}")
        return None
