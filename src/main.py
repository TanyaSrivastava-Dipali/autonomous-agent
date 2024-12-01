import time
import asyncio
from threading import Thread
from .autonomous_agent import AutonomousAgent
from .logger import logger
from .agent_connector import connect_agents 

def init_agents():
    logger.info("Autonomous agents setup")

    # Initialize autonomous agents
    agent1 = AutonomousAgent("AgentA ")
    agent2 = AutonomousAgent("AgentB ")

    Thread(target=agent1.process_messages, daemon=True).start()
    Thread(target=agent2.process_messages, daemon=True).start()

    Thread(target=agent1.start, daemon=True).start()
    Thread(target=agent2.start, daemon=True).start()
    
    connect_agents(agent1,agent2)

if __name__ == "__main__":
    init_agents()
