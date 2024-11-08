import time
import asyncio
from threading import Thread
from .autonomous_agent import AutonomousAgent
from .logger import logger
from .agent_connector import connect_agents 

def init_agents():
    logger.info("Setting up autonomous agents")

    # Initialize autonomous agents
    agent1 = AutonomousAgent("Agent1")
    agent2 = AutonomousAgent("Agent2")

    Thread(target=agent1.process_messages, daemon=True).start()
    Thread(target=agent2.process_messages, daemon=True).start()

    Thread(target=agent1.start, daemon=True).start()
    Thread(target=agent2.start, daemon=True).start()
    
    connect_agents()

if __name__ == "__main__":
    init_agents()
