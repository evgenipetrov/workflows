import json
import logging
import os
from datetime import timedelta
from typing import Any

from bs4 import BeautifulSoup
from markdownify import markdownify

from datatypes.page_type import Page
from nodes.base_node import BaseNode


class MarkdownNode(BaseNode):
    CACHE_DURATION = timedelta(hours=24)

    def __init__(self, project_name: str):
        super().__init__(project_name)
        self._logger = logging.getLogger(__name__)

    def _load_data_item(self, file_path: str) -> Page:
        return Page.load(file_path)

    def _process_item(self, item: Any) -> Page:
        try:
            if isinstance(item, Page):
                html_content = item.html
            else:
                raise ValueError("Invalid input type. Expected Page object.")

            markdown_content = self._convert_html_to_markdown(html_content)
            item.markdown = markdown_content
            self._logger.info(f"Successfully converted HTML to Markdown for URL: {item.url}")
        except Exception as e:
            self._logger.error(f"Failed to convert HTML to Markdown for URL: {item.url}. Error: {e}")
        return item

    def _load_data(self) -> None:
        if self._input_path:
            all_json_file = os.path.join(self._input_path, "all.json")
            if os.path.exists(all_json_file):
                with open(all_json_file, "r") as file:
                    data = json.load(file)
                    self._input_data = []
                    for item in data:
                        url = item.get("url", "")
                        page = Page(url)
                        for key, value in item.items():
                            if key != "url":
                                setattr(page, key, value)
                        self._input_data.append(page)
            else:
                self._logger.warning("all.json file not found in the input path.")
        elif self._input_data:
            self._input_data = [page for page in self._input_data if isinstance(page, Page)]

    # In MarkdownNode._save_data method
    def _save_data(self) -> None:
        json_file_path = os.path.join(self._output_path, "all.json")
        data = []
        for index, item in enumerate(self._output_data):
            file_name = f"payload_{index}.md"
            file_path = os.path.join(self._output_path, file_name)
            item._save_payload(file_path, item.markdown)
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
    def _convert_html_to_markdown(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        body = soup.body
        if body:
            html_content = str(body)
        else:
            html_content = str(soup)
        markdown_content = markdownify(html_content)
        return markdown_content

    def _get_cache_duration(self) -> timedelta:
        return self.CACHE_DURATION
