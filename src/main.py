import asyncio
from .autonomous_agent import AutonomousAgent
from .logger import logger
from .agent_connector import connect_agents

async def init_agents():
    logger.info("Autonomous agents setup")

    # Initialize autonomous agents
    agent1 = AutonomousAgent("AgentA")
    agent2 = AutonomousAgent("AgentB")

    # Start agent behaviors and message processing
    agent_tasks = [
        asyncio.create_task(agent1.start()),
        asyncio.create_task(agent2.start()),
        asyncio.create_task(agent1.process_messages()),
        asyncio.create_task(agent2.process_messages())
    ]

    # Start the connector to relay messages
    connector_task = asyncio.create_task(connect_agents(agent1, agent2))

    # Wait for all tasks
    await asyncio.gather(*agent_tasks, connector_task)

if __name__ == "__main__":
    asyncio.run(init_agents())