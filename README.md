# Autonomous Agent Project

This project involves building autonomous agents capable of message processing, behavior management, and ERC-20 token handling on the Ethereum blockchain. The agents are designed to communicate asynchronously and can perform multiple actions concurrently, including message filtering, token transfers, and balance checks.

## Table of Contents

- [Installation and Running the Project](#installation)
- [Description of Key Folders and Files](#Description)
- [Acknowledgments](#acknowledgments)

## Installation & Running the Project

### Prerequisites

**Python 3.9+**


Follow these steps to install the necessary dependencies for the project:

1. Clone the repository:

```bash
git clone https://github.com/TanyaSrivastava-Dipali/autonomous-agent.git
cd autonomous-agent
```
2. Create Virtual Environment and Activate:

```bash
python3 -m venv venv
```
   - If `venv` is not installed, you can install it with and then create the venv with above command:
     ```bash
     sudo apt install python3-venv
     ```
 Activate the Virtual Environment
```
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Copy the keys in .env file from .env.example file provided in the repository:
```bash
cp .env.example .env
```

5. Add Your Keys to the .env File:


  - Open the .env file and replace placeholder values with your actual keys, including RPC_NODE_URL,TOKEN_ADDRESS, FROM_ADDRESS,TO_ADDRESS and PRIVATE_KEY.


6. Run the agent:

```bash
python3 -m src.main
```
7. Run the Test:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Description of Key Folders and Files:

- **`autonomous_agent/`**: The root directory for the project, which contains the core files for the application.
- **`src/`**: Contains the source code for the autonomous agents and their functionalities.
  - **`config/`**: Holds the configuration files (such as `settings.py`) for environment-specific settings.
  - **`utils/`**: Contains ABI for smart contract.
  - **`agent_connector.py`**: Manages the connection and communication logic with the external agents or services.
  - **`agent.py`**: Defines the primary structure autonomous agent, including its state.
  - **`autonomous_agent.py`**: Implements specific algorithms or strategies unique to the autonomous agent.
  - **`handlers.py`**: Contains handlers that process messages received by the agent, triggering specific behaviors.
  - **`logger.py`**: Provides logging utilities to track agent operations, performance, and errors.
  - **`main.py`**: The entry point of the application where the agent is initialized and started.
<!-- - **`tests/`**: Directory for unit tests, including tests for agent behaviors and interactions.
  - **`test_autonomous_agent.py`**: Contains test cases that verify the functionality and behavior of the autonomous agent. -->
  
## Acknowledgments

- **Tenderly**: For offering a platform to easily test and debug Ethereum smart contracts in a controlled environment.
- **web3.py**: For providing an intuitive Python library to interact with Ethereum and simplify blockchain operations.
