import json
from typing import List, Union

from datatypes.base_type import BaseType


class AmazonProduct(BaseType):
    asin: str = ""
    address: str = ""
    title: str = ""
    image_urls: List[str] = []
    description: str = ""
    bullets: List[str] = []

    def __init__(self, identifier: Union[str, None] = None):
        if identifier:
            if identifier.startswith("http"):
                self.url = identifier
            else:
                self.asin = identifier

    def _save_all(self, file_path: str) -> None:
        data = self.__dict__
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def save_payload(self, file_path: str, content: str) -> None:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

    @classmethod
    def load(cls, data: dict) -> "AmazonProduct":
        instance = cls()
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return instance
