import logging

class CustomLogger:
    @staticmethod
    def initialize():
        log_format = "%(asctime)s - %(message)s"
        logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")
        return logging.getLogger(__name__)

# Initialize the logger
logger = CustomLogger.initialize()
