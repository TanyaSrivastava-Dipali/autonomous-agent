import asyncio
from .logger import logger

async def connect_agents(agent1, agent2):

    async def relay_messages(from_agent, to_agent):
        while True:
            message = await from_agent.get_outbox_message()
            if message:
                await to_agent.send_inbox_message(message)
            await asyncio.sleep(1)  # Prevent busy-waiting

    # Start two relay loops: one for each direction
    await asyncio.gather(
        relay_messages(agent1, agent2),
        relay_messages(agent2, agent1)
    )