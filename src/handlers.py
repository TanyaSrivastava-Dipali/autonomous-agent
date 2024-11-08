from .logger import logger

def hello_filter_handler(agent, message_content):
    logger.info(f"Filtered message (hello): {message_content['content']}")

def crypto_filter_handler(agent, message_content):
    logger.info(f"Filtered message (crypto): {message_content['content']}")
    logger.info("Initiating ERC-20 token transfer...")
    agent.transfer_erc20_token()