import asyncio
from .logger import logger

class Agent:
    def __init__(self, agent_name):
        self.inbox = asyncio.Queue()
        self.outbox = asyncio.Queue()
        self.behaviours = []
        self.handlers = {}
        self.name = agent_name

    def register_handler(self, message_type, handler):
        logger.info(f"Registering Handler : {self.name} :: {message_type}_filter")
        self.handlers[message_type] = handler

    def register_behaviour(self, behaviour, name):
        logger.info(f"Registering behaviour : {self.name} :: {name}")
        self.behaviours.append(behaviour)

    async def process_messages(self):
        while True:
            logger.info(f"{self.name}:: Checking inbox for messages...")
            message = await self.inbox.get()
            if message:
                logger.info(f"{self.name}:: Message found: {message}")
                message_type = message.get('type')
                if message_type in self.handlers:
                    await self.handlers[message_type](message)
                self.inbox.task_done()
            else:
                logger.info(f"{self.name}:: Message not found!!")

    async def send_inbox_message(self, message_type):
        logger.info(f"{self.name}:: Sending inbox message: {message_type}")
        await self.inbox.put(message_type)

    async def send_outbox_message(self, message_type):
        await self.outbox.put(message_type)

    async def get_outbox_message(self):
        try:
            message = self.outbox.get_nowait()
            logger.info(f"{self.name}:: Getting outbox message: {message}")
            return message
        except asyncio.QueueEmpty:
            return None

    def get_name(self):
        return self.name
