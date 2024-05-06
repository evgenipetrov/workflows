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
from nodes.base_node import BaseNode
from operators.file_operator import FileOperator

load_dotenv()


class BrowserNode(BaseNode):
    CACHE_DURATION = timedelta(hours=24)

    def __init__(self, project_name: str):
        super().__init__(project_name)
        self._logger = logging.getLogger(__name__)
        self.file_operator = FileOperator()

    def _load_data_item(self, file_path: str) -> Page:
        return Page.load(file_path)

    def _process_item(self, item: Any) -> Page:
        execute_js = self._kwargs.get("execute_js", False)
        try:
            if isinstance(item, Page):
                url = item.url
            else:
                url = item
                item = Page(url)
            html_content = self._use_selenium(url) if execute_js else self._use_requests(url)
            item.html = html_content
            self._logger.info(f"Successfully fetched HTML content from URL: {url}")
        except Exception as e:
            if isinstance(item, Page):
                url = item.url
            else:
                url = item
            self._logger.error(f"Failed to fetch HTML content from URL: {url}. Error: {e}")
        return item

    def _save_data(self) -> None:
        json_file_path = os.path.join(self._output_path, "all.json")
        data = []
        for index, item in enumerate(self._output_data):
            file_name = f"payload_{index}.html"
            file_path = os.path.join(self._output_path, file_name)
            item._save_payload(file_path, item.html)
            entry = {
                "url": item.url,
                "html": item.html,
                "markdown": item.markdown,
                "file_name": file_name,
            }
            data.append(entry)
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

    @staticmethod
    def _use_requests(url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    @staticmethod
    def _use_selenium(url: str) -> str:
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
        return self.CACHE_DURATION

    def _get_input_type(self) -> Any:
        return Page
