# Autonomous Agent Project

This project involves building autonomous agents capable of message processing, behavior management, and ERC-20 token handling on the Ethereum blockchain. The agents are designed to communicate asynchronously and can perform multiple actions concurrently, including message filtering, token transfers, and balance checks.

## Table of Contents

- [Installation and Running the Project](#installation)
- [Description of Key Folders and Files](#Description)
- [Acknowledgments](#acknowledgments)

## Installation & Running the Project

Follow these steps to install the necessary dependencies for the project:

1. Clone the repository:

```bash
git clone https://github.com/your-username/autonomous-agent.git
cd autonomous-agent
```
2. Create Virtual Environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```
4. Run the agent:

```bash
python -m src.main
```
5. Run the Test:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Description of Key Folders and Files:

- **`autonomous_agent/`**: The root directory for the project, which contains the core files for the application.
- **`src/`**: Contains the source code for the autonomous agents and their functionalities.
  - **`config/`**: Holds the configuration files (such as `settings.py`) for environment-specific settings.
  - **`utils/`**: Contains ABI for smart contract.
  - **`agent_connector.py`**: Manages the connection and communication logic with external agents or services.
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
- Please refer to the **`example.env`** file for the required environment variables to configure the project correctly.