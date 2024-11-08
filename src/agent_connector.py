import time

def connect_agents(agent1, agent2):
    while True:
        # Relay message from agent1 to agent2
        message = agent1.get_outbox_message()
        if message:
            agent2.send_inbox_message(message)

        # Relay message from agent2 to agent1
        message = agent2.get_outbox_message()
        if message:
            agent1.send_inbox_message(message)

        time.sleep(1)