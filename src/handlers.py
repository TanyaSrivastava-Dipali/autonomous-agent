from .logger import logger
from .token_operation import transfer_erc20_token

async def hello_filter_handler(agent, message):
    logger.info(f"{agent.name}:: Filtered message (hello)")

async def crypto_filter_handler(agent, message):
    logger.info(f"{agent.name}:: Initiating ERC-20 token transfer...")
    await transfer_erc20_token(agent)
