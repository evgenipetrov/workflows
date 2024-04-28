# logging_operator.py
import logging


class LoggingOperator:
    @staticmethod
    def setup_logging():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
