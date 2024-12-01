from .logger import logger
from .token_operation import transfer_erc20_token

def hello_filter_handler(agent):
    logger.info(f"Filtered message (hello):")

async def crypto_filter_handler(agent):
    logger.info("Initiating ERC-20 token transfer...")
    await agent.transfer_erc20_token()
    