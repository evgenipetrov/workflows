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
        self._logger = logging.getLogger(__name__)

    def _load_data(self, urls):
        """Ensure the URLs are always handled as a list."""
        if isinstance(urls, str):  # Check if urls is a single string
            urls = [urls]  # Convert it to a list
        return urls

    def _process(self, output_folder):
        """Fetch HTML content for each URL and store in self._processing_data."""
        processed_data = []
        for url in self._processing_data:
            try:
                self._logger.info(f"Fetching HTML content from URL: {url}")
                response = requests.get(url)
                response.raise_for_status()

                # Generate a normalized filename from the URL
                filename = f"{UrlOperator.normalize_url(url)}.html"
                processed_data.append((filename, response.text))
                self._logger.info(f"Successfully fetched HTML content from URL: {url}")
            except requests.RequestException as e:
                self._logger.error(f"Failed to fetch HTML content from URL: {url}. Error: {e}")

        self._processing_data = processed_data

    def _save_data(self, output_folder):
        """Save the processed HTML data to files in the specified output folder."""
        for filename, html_content in self._processing_data:
            output_path = os.path.join(output_folder, filename)
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(html_content)
            self._logger.info(f"HTML content successfully written to {output_path}")

    def execute(self, urls, **kwargs):
        # Ensure urls are processed as a list
        urls = self._load_data(urls)  # This adjusts single url to a list if necessary
        self._input_data = urls
        self._processing_data = self._input_data.copy()
        output_folder, is_cache_valid = self._cache_manager.get_or_create_output_folder(**kwargs)
        if not is_cache_valid:
            self._process(output_folder)
            self._save_data(output_folder)
        return output_folder

    def _get_cache_duration(self):
        return self.CACHE_DURATION  # Overrides the base class method
