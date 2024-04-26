import logging
from datetime import timedelta

from src.nodes.base_node import BaseNode


class BoilerplateNode(BaseNode):
    CACHE_DURATION = timedelta(hours=2)  # Custom cache duration for this node
    FOLDER_NAME = "boilerplate"  # Custom folder name for this node

    def __init__(self, project_name):
        super().__init__(project_name)
        self.logger = logging.getLogger(__name__)

    def process(self, input_data, **kwargs):
        # Specific processing logic for BoilerplateNode
        self.logger.info(f"Processing input data in BoilerplateNode: {input_data}")
        processed_data = f"Processed {input_data} with params {kwargs}"
        return processed_data
