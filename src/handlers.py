from .logger import logger
from .token_operation import transfer_erc20_token

def hello_filter_handler(agent,message):
    logger.info(f"{agent.name}:: Filtered message (hello):")

def crypto_filter_handler(agent,message):
    logger.info(f"{agent.name}:: Initiating ERC-20 token transfer...")
    transfer_erc20_token(agent)
    