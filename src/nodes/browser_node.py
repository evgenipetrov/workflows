import logging
import os
from datetime import timedelta

import requests

from src.nodes.base_node import BaseNode
from src.operators.url_operator import UrlOperator


class BrowserNode(BaseNode):
    FILE_EXTENSION = "html"
    CACHE_DURATION = timedelta(hours=24)  # Cache duration of 24 hours

    def __init__(self, project_name):
        super().__init__(project_name)
        self.logger = logging.getLogger(__name__)

    def _load_data(self, urls):
        """Ensure the URLs are always handled as a list."""
        if isinstance(urls, str):  # Check if urls is a single string
            urls = [urls]  # Convert it to a list
        return urls

    def _process(self, data_list, output_folder):
        """Fetch HTML content for each URL and store in the output folder."""
        for url in data_list:
            try:
                self.logger.info(f"Fetching HTML content from URL: {url}")
                response = requests.get(url)
                response.raise_for_status()

                # Generate a normalized filename from the URL
                filename = f"{UrlOperator.normalize_url(url)}.html"
                output_path = os.path.join(output_folder, filename)

                with open(output_path, "w", encoding="utf-8") as file:
                    file.write(response.text)
                self.logger.info(f"Successfully fetched and stored HTML content from URL: {url} in {filename}")
            except requests.RequestException as e:
                self.logger.error(f"Failed to fetch HTML content from URL: {url}. Error: {e}")

    def execute(self, urls, **kwargs):
        # Ensure urls are processed as a list
        urls = self._load_data(urls)  # This adjusts single url to a list if necessary
        output_folder, is_cache_valid = self.cache_manager.get_or_create_output_folder(**kwargs)
        if not is_cache_valid:
            self._process(urls, output_folder)
        return output_folder

    def _get_cache_duration(self):
        return self.CACHE_DURATION  # Overrides the base class method
