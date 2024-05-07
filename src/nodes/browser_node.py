import json
import logging
import os
import time
from datetime import timedelta
from typing import Any

import requests
import undetected_chromedriver as uc
from dotenv import load_dotenv

from datatypes.page_type import Page
from datatypes.url_type import Url
from nodes.base_node import BaseNode
from operators.file_operator import FileOperator

load_dotenv()


class BrowserNode(BaseNode):
    """Node for fetching HTML content from URLs using requests or Selenium."""

    CACHE_DURATION = timedelta(hours=24)

    def __init__(self, project_name: str):
        """Initialize the BrowserNode.

        Args:
            project_name: The name of the project.
        """
        super().__init__(project_name)
        self._logger = logging.getLogger(__name__)
        self.file_operator = FileOperator()

    def _load_data_item(self, file_path: str) -> Page:
        """Load a single data item from a file.

        Args:
            file_path: The path to the file containing the data item.

        Returns:
            The loaded Page object.
        """
        return Page.load(file_path)

    def _process_item(self, item: Any) -> Any:
        """Process a single item by fetching its HTML content.

        Args:
            item: The item to process (Page object or Url object).

        Returns:
            The processed Page object with the fetched HTML content.
        """
        if isinstance(item, Page):
            return self._process_page(item)
        elif isinstance(item, Url):
            return self._process_url(item)
        else:
            raise ValueError(f"Unsupported item type: {type(item)}")

    def _process_url(self, url: Url) -> Page:
        """Process a Url object by fetching its HTML content.

        Args:
            url: The Url object to process.

        Returns:
            The processed Page object with the fetched HTML content.
        """
        execute_js = self._kwargs.get("execute_js", False)
        try:
            page = Page(address=url.address)
            html_content = self._fetch_html(url.address, execute_js)
            page.html = html_content
            self._logger.info(f"Successfully fetched HTML content from URL: {url.address}")
            return page
        except Exception as e:
            self._logger.error(f"Failed to fetch HTML content from URL: {url.address}. Error: {e}")
            return None

    def _process_page(self, page: Page) -> Page:
        """Process a Page object by fetching its HTML content.

        Args:
            page: The Page object to process.

        Returns:
            The processed Page object with the fetched HTML content.
        """
        execute_js = self._kwargs.get("execute_js", False)
        try:
            html_content = self._fetch_html(page.address, execute_js)
            page.html = html_content
            self._logger.info(f"Successfully fetched HTML content from URL: {page.address}")
            return page
        except Exception as e:
            self._logger.error(f"Failed to fetch HTML content from URL: {page.address}. Error: {e}")
            return None

    def _fetch_html(self, url: str, execute_js: bool) -> str:
        """Fetch the HTML content from the given URL.

        Args:
            url: The URL to fetch the HTML content from.
            execute_js: Whether to execute JavaScript when fetching the HTML content.

        Returns:
            The fetched HTML content.
        """
        if execute_js:
            return self._use_selenium(url)
        else:
            return self._use_requests(url)

    def _save_data(self) -> None:
        """Save the processed data to files."""
        json_file_path = os.path.join(self._output_path, "all.json")
        data = []
        for index, item in enumerate(self._output_data):
            file_name = f"payload_{index}.html"
            file_path = os.path.join(self._output_path, file_name)
            item.save_payload(file_path, item.html)
            entry = {
                "data_type": item.__class__.__name__,
                "address": item.address,
                "html": item.html,
                "file_name": file_name,
            }
            data.append(entry)
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

    @staticmethod
    def _use_requests(url: str) -> str:
        """Fetch the HTML content from the given URL using the requests library.

        Args:
            url: The URL to fetch the HTML content from.

        Returns:
            The fetched HTML content.
        """
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    @staticmethod
    def _use_selenium(url: str) -> str:
        """Fetch the HTML content from the given URL using Selenium with undetected_chromedriver.

        Args:
            url: The URL to fetch the HTML content from.

        Returns:
            The fetched HTML content.
        """
        browser_executable_path = os.getenv("CHROME_EXECUTABLE_PATH")
        user_data_dir = os.getenv("USER_DATA_ROOT_PATH")
        driver = uc.Chrome(
            browser_executable_path=browser_executable_path, user_data_dir=user_data_dir, use_subprocess=True
        )
        try:
            driver.get("about:blank")
            time.sleep(1)
            driver.get(url)
            html_content = driver.page_source
        finally:
            driver.quit()
        return html_content

    def _get_cache_duration(self) -> timedelta:
        """Get the cache duration for the node.

        Returns:
            The cache duration as a timedelta object.
        """
        return self.CACHE_DURATION

    def _get_input_type(self) -> Any:
        """Get the input type for the node.

        Returns:
            The input type (Page).
        """
        return Page
