import asyncio
from .logger import logger
from .config.settings import ETH_SETTINGS

async def get_erc20_balance_behaviour(agent):
    while True:
        try:
            add = ETH_SETTINGS["FROM_ADDRESS"]
            # Call balanceOf in a separate thread
            balance = await asyncio.to_thread(
                agent.token_contract.functions.balanceOf(ETH_SETTINGS["FROM_ADDRESS"]).call
            )
            # Compute balance in tokens
            balance_in_tokens = balance / (10 ** agent.token_decimals)
            logger.info(f"{agent.name}:: ERC-20 Token Balance for address {add}: {balance_in_tokens}")
        except Exception as e:
            logger.error(f"{agent.name}:: Error fetching balance: {e}")
        await asyncio.sleep(10)

async def transfer_erc20_token(agent):
    try:
        if not await asyncio.to_thread(agent.w3.is_connected):
            logger.error("Web3 is not connected.")
            return None

        decimals = agent.token_decimals

        balance = await asyncio.to_thread(
            agent.token_contract.functions.balanceOf(ETH_SETTINGS["FROM_ADDRESS"]).call)

        token_to_transfer = 1 * (10 ** decimals)

        if balance >= token_to_transfer:
            nonce = await asyncio.to_thread(
                agent.w3.eth.get_transaction_count,
                ETH_SETTINGS["FROM_ADDRESS"],
            )

            txn = await asyncio.to_thread(
                agent.token_contract.functions.transfer(
                    ETH_SETTINGS["TO_ADDRESS"], token_to_transfer
                ).build_transaction,
                {
                    "chainId": agent.w3.eth.chain_id,
                    "gas": 2000000,
                    "gasPrice": agent.w3.eth.gas_price,
                    "nonce": nonce,
                }
            )
            signed_txn = await asyncio.to_thread(
                agent.w3.eth.account.sign_transaction,
                txn,
                private_key=ETH_SETTINGS["PRIVATE_KEY"],
            )
            tx_hash = await asyncio.to_thread(
                agent.w3.eth.send_raw_transaction, signed_txn.raw_transaction
            )
            logger.info(f"{agent.name}:: Transaction sent with hash: {tx_hash.hex()}")
            return tx_hash.hex()
        else:
            logger.info(f"{agent.name}:: Insufficient tokens to transfer. Balance: {balance}")
    except Exception as e:
        logger.error(f"{agent.name}:: Error transferring token: {e}")
        return None