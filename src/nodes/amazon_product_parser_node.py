import json
import logging
import os
from datetime import timedelta
from typing import Any

from bs4 import BeautifulSoup

from datatypes.amazon_product_type import AmazonProduct
from nodes.base_node import BaseNode


class AmazonProductParserNode(BaseNode):
    CACHE_DURATION = timedelta(hours=24)

    def __init__(self, project_name: str):
        super().__init__(project_name)
        self._logger = logging.getLogger(__name__)

    def _load_data_item(self, file_path: str) -> AmazonProduct:
        return AmazonProduct.load(file_path)

    def _process_item(self, item: Any) -> AmazonProduct:
        try:
            if isinstance(item, AmazonProduct):
                html_content = item.html
            else:
                raise ValueError("Invalid input type. Expected AmazonProduct object.")

            soup = BeautifulSoup(html_content, "html.parser")
            item.asin = self._extract_asin(item.url)
            item.title = self._extract_title(soup)
            item.image_urls = self._extract_image_urls(soup)
            item.description = self._extract_description(soup)
            item.bullets = self._extract_bullets(soup)
            self._logger.info(f"Successfully parsed Amazon product data for ASIN: {item.asin}")
        except Exception as e:
            self._logger.error(f"Failed to parse Amazon product data for URL: {item.url}. Error: {e}")
        return item

    def _save_data(self) -> None:
        json_file_path = os.path.join(self._output_path, "all.json")
        data = []
        for index, item in enumerate(self._output_data):
            file_name = f"payload_{index}.json"
            file_path = os.path.join(self._output_path, file_name)
            item._save_payload(file_path, json.dumps(item.__dict__, indent=4))
            entry = {
                "asin": item.asin,
                "url": item.url,
                "title": item.title,
                "image_urls": item.image_urls,
                "description": item.description,
                "bullets": item.bullets,
                "file_name": file_name,
            }
            data.append(entry)
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

    @staticmethod
    def _extract_asin(url: str) -> str:
        asin = url.split("/")[-2]
        return asin

    @staticmethod
    def _extract_title(soup: BeautifulSoup) -> str:
        title_element = soup.select_one("#productTitle")
        return title_element.get_text(strip=True) if title_element else ""

    @staticmethod
    def _extract_image_urls(soup: BeautifulSoup) -> list:
        image_elements = soup.select("#altImages img")
        image_urls = [img["src"] for img in image_elements] if image_elements else []

        largest_image_urls = []
        for url in image_urls:
            if "play-button-overlay" not in url and "360_icon" not in url:
                largest_image_url = url.split("._")[0] + ".jpg"
                largest_image_urls.append(largest_image_url)

        return largest_image_urls

    @staticmethod
    def _extract_description(soup: BeautifulSoup) -> str:
        description_element = soup.select_one("#productDescription")
        return description_element.get_text(strip=True) if description_element else ""

    @staticmethod
    def _extract_bullets(soup: BeautifulSoup) -> list:
        bullet_elements = soup.select("div#productFactsDesktopExpander ul.a-unordered-list li")
        bullets = [bullet.get_text(strip=True) for bullet in bullet_elements] if bullet_elements else []
        return bullets

    def _get_cache_duration(self) -> timedelta:
        return self.CACHE_DURATION

    def _get_input_type(self) -> Any:
        return AmazonProduct
