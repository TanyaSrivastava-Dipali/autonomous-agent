import asyncio
from .logger import logger
from .config.settings import MESSAGE_WORDS, ETH_SETTINGS

async def get_erc20_balance_behaviour(agent):
    while True:
        add=ETH_SETTINGS["FROM_ADDRESS"]
        balance = agent.token_contract.functions.balanceOf(ETH_SETTINGS["FROM_ADDRESS"]).call()
        dec = agent.token_contract.functions.decimals().call()
        balance_in_tokens = balance / (10**dec)
        logger.info(f"{agent.name}::ERC-20 Token Balance for address {add}: {balance_in_tokens}")
        await asyncio.sleep(10)  # Add a 10-second delay before checking balance again
    
async def transfer_erc20_token(agent):
    try:
        w3 = Web3(Web3.HTTPProvider(ETH_SETTINGS["RPC_NODE_URL"]))
        balance = agent.token_contract.functions.balanceOf(
        agent.w3.to_checksum_address(ETH_SETTINGS["FROM_ADDRESS"])
        ).call()
        one_unit = 1 * 10 ** (agent.token_contract.functions.decimals().call())
        if balance >= one_unit:
            nonce = agent.w3.eth.getTransactionCount(ETH_SETTINGS["FROM_ADDRESS"])

            txn = contract.functions.transfer(
                ETH_SETTINGS["TO_ADDRESS"], w3.toWei(1, "ether")
            ).buildTransaction(
                {
                    "chainId": agent.w3.eth.chain_id,
                    "gas": 2000000,
                    "gasPrice": w3.toWei("50", "gwei"),
                    "nonce": nonce,
                }
            )

            signed_txn = agent.w3.eth.account.sign_transaction(
                txn, private_key=ETH_SETTINGS["PRIVATE_KEY"]
            )
            tx_hash = agent.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            logger.info(f"Transaction sent with hash: {tx_hash.hex()}")
            return tx_hash.hex()
        else:
            logger.info("Insufficient tokens to transfer.")
    except Exception as e:
        logger.error(f"Error transferring token: {e}")
        return None

    
