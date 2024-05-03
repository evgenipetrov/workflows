import logging
import os
import time
from datetime import timedelta

import requests
import undetected_chromedriver as uc

from nodes.base_node import BaseNode
from operators.file_operator import FileOperator
from operators.url_operator import UrlOperator


class BrowserNode(BaseNode):
    FILE_EXTENSION = "html"
    CACHE_DURATION = timedelta(hours=24)

    def __init__(self, project_name: str):
        super().__init__(project_name)
        self._logger = logging.getLogger(__name__)
        self.file_operator = FileOperator()

    def _load_data(self) -> None:
        df = self.file_operator.read_all_csvs_in_folder(self._input_folder)

        if not df.empty and "url" in df.columns:
            self._input_data = df["url"].tolist()
        else:
            self._logger.warning("No URLs found or 'url' column is missing in the CSV files.")

    def _process(self) -> None:
        execute_js = self._kwargs.get("execute_js", False)
        for url in self._input_data:
            try:
                html_content = self._use_selenium(url) if execute_js else self._use_requests(url)
                filename = f"{UrlOperator.normalize_url(url)}.html"
                self._output_data.append((filename, html_content))
                self._logger.info(f"Successfully fetched HTML content from URL: {url}")
            except Exception as e:
                self._logger.error(f"Failed to fetch HTML content from URL: {url}. Error: {e}")

    def _save_data(self) -> None:
        self._logger.debug(f"Saving data to folder {self._output_folder}. Data to save: {self._output_data}")
        for filename, html_content in self._output_data:
            output_file_path = os.path.join(self._output_folder, filename)
            with open(output_file_path, "w", encoding="utf-8", errors="replace") as file:
                file.write(html_content)
            self._logger.info(f"HTML content successfully written to {output_file_path}")

    @staticmethod
    def _use_requests(url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    @staticmethod
    def _use_selenium(url: str) -> str:
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

    def _get_cache_duration(self) -> timedelta:
        return self.CACHE_DURATION
