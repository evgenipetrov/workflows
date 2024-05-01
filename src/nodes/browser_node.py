import logging
import os
import time
from datetime import timedelta

import requests
import undetected_chromedriver as uc

from nodes.base_node import BaseNode
from operators.csv_operator import CsvOperator
from operators.url_operator import UrlOperator


class BrowserNode(BaseNode):
    FILE_EXTENSION = "html"
    CACHE_DURATION = timedelta(hours=24)  # Cache duration of 24 hours

    def __init__(self, project_name):
        super().__init__(project_name)
        self._logger = logging.getLogger(__name__)
        self.csv_operator = CsvOperator()  # Initialize CsvOperator

    def _load_data(self, input_path, **kwargs):
        df = self.csv_operator.read_all_csvs_in_folder(input_path)
        execute_js = kwargs.get("execute_js", False)
        # Initialize _input_data to an empty list to ensure it's never None
        self._input_data = []

        if not df.empty and "url" in df.columns:
            self._input_data = df["url"].tolist()
        else:
            self._logger.warning("No URLs found or 'url' column is missing in the CSV files.")

        self._extra_args = {"execute_js": execute_js}

    @staticmethod
    def _use_requests(url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    @staticmethod
    def _use_selenium(url):
        browser_executable_path = os.getenv("CHROME_EXECUTABLE_PATH")
        user_data_dir = os.getenv("USER_DATA_ROOT_PATH")
        driver = uc.Chrome(browser_executable_path=browser_executable_path, user_data_dir=user_data_dir, use_subprocess=True)
        try:
            driver.get("about:blank")
            time.sleep(1)
            driver.get(url)
            html_content = driver.page_source
        finally:
            driver.quit()
        return html_content

    def _process(self, output_folder):
        execute_js = self._extra_args["execute_js"]
        for url in self._input_data:
            try:
                html_content = self._use_selenium(url) if execute_js else self._use_requests(url)
                filename = f"{UrlOperator.normalize_url(url)}.html"
                # Ensure only two items are in the tuple
                self._processing_data.append((filename, html_content))
                self._logger.info(f"Successfully fetched HTML content from URL: {url}")
            except Exception as e:
                self._logger.error(f"Failed to fetch HTML content from URL: {url}. Error: {e}")

    def _save_data(self, output_folder):
        self._logger.debug(f"Saving data to folder {output_folder}. Data to save: {self._processing_data}")
        for item in self._processing_data:
            try:
                filename, html_content = item  # Unpacking the tuple
                output_file_path = os.path.join(output_folder, filename)
                with open(output_file_path, "w", encoding="utf-8", errors="replace") as file:
                    file.write(html_content)
                self._logger.info(f"HTML content successfully written to {output_file_path}")
            except ValueError as e:
                self._logger.error(f"Error unpacking item in _save_data: {item}, Error: {e}")

    def _get_cache_duration(self):
        return self.CACHE_DURATION
