import os

from dotenv import load_dotenv

load_dotenv()

WORDS_TO_FIND = ["hello", "crypto"]
# Define the MESSAGE_WORDS for message generation
MESSAGE_WORDS = [
    "hello",
    "sun",
    "world",
    "space",
    "moon",
    "crypto",
    "sky",
    "ocean",
    "universe",
    "human",
]

# Ethereum settings
ETH_SETTINGS = {
    "RPC_NODE_URL": os.getenv("RPC_NODE_URL"),
    "FROM_ADDRESS": os.getenv("FROM_ADDRESS"),
    "TO_ADDRESS": os.getenv("TO_ADDRESS"),
    "PRIVATE_KEY": os.getenv("PRIVATE_KEY"),
    "TOKEN_ADDRESS": os.getenv("TOKEN_ADDRESS"),
}
