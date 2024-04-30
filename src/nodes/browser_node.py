import logging
import os
import time
from datetime import timedelta

import requests
import undetected_chromedriver as uc

from nodes.base_node import BaseNode
from operators.url_operator import UrlOperator


class BrowserNode(BaseNode):
    FILE_EXTENSION = "html"
    CACHE_DURATION = timedelta(hours=24)  # Cache duration of 24 hours

    def __init__(self, project_name):
        super().__init__(project_name)
        self._logger = logging.getLogger(__name__)

    def _load_data(self, urls):
        """Ensure the URLs are always handled as a list."""
        self._input_data = [urls] if isinstance(urls, str) else urls

    @staticmethod
    def _use_requests(url):
        """Fetch HTML content using requests."""
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    @staticmethod
    def _use_selenium(url):
        """Fetch HTML content using Selenium WebDriver."""
        browser_executable_path = os.getenv("CHROME_EXECUTABLE_PATH")
        user_data_dir = os.getenv("USER_DATA_ROOT_PATH")
        driver = uc.Chrome(
            browser_executable_path=browser_executable_path,
            user_data_dir=user_data_dir,
            use_subprocess=True,
        )
        try:
            driver.get("about:blank")  # Open a blank page to ensure the browser is open
            time.sleep(1)
            driver.get(url)
            # input("Press Enter to continue once the page has loaded")  # Wait for user input before proceeding
            html_content = driver.page_source
        finally:
            driver.close()  # Ensure driver is quit no matter what
        return html_content

    def _process(self, output_folder, execute_js=False):
        """Fetch HTML content for each URL and store in self._processing_data."""
        for url in self._input_data:
            try:
                self._logger.info(f"Fetching HTML content from URL: {url}")
                html_content = self._use_selenium(url) if execute_js else self._use_requests(url)

                filename = f"{UrlOperator.normalize_url(url)}.html"
                self._processing_data.append((filename, html_content))
                self._logger.info(f"Successfully fetched HTML content from URL: {url}")
            except Exception as e:
                self._logger.error(f"Failed to fetch HTML content from URL: {url}. Error: {e}")

    def _save_data(self, output_folder):
        """Save the processed HTML data to files in the specified output folder."""
        for filename, html_content in self._processing_data:
            output_path = os.path.join(output_folder, filename)
            with open(output_path, "w", encoding="utf-8", errors="replace") as file:
                file.write(html_content)
            self._logger.info(f"HTML content successfully written to {output_path}")

    def execute(self, urls, execute_js=False, **kwargs):
        self._load_data(urls)
        output_folder, is_cache_valid = self._cache_manager.get_or_create_output_folder(**kwargs)
        if not is_cache_valid:
            self._process(output_folder, execute_js)
            self._save_data(output_folder)
        return output_folder

    def _get_cache_duration(self):
        return self.CACHE_DURATION
