import logging
from src.nodes.base_node import BaseNode


class BoilerplateNode(BaseNode):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def execute(self, input_data):
        self.logger.info(f"BoilerplateNode processing: {input_data}")
        return input_data
