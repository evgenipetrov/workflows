import logging
from datetime import timedelta

import requests

from src.nodes.base_node import BaseNode


class BrowserNode(BaseNode):
    FILE_EXTENSION = "html"
    CACHE_DURATION = timedelta(hours=24)  # Cache duration of 24 hours

    def __init__(self, project_name):
        super().__init__(project_name)
        self.logger = logging.getLogger(__name__)

    def process(self, input_data, **kwargs):
        self.logger.info(f"Fetching HTML content from URL: {input_data}")
        response = requests.get(input_data)
        response.raise_for_status()
        self.logger.info(f"Successfully fetched HTML content from URL: {input_data}")
        return response.text
