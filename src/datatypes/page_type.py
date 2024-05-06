import json

from datatypes.base_type import BaseType


class Page(BaseType):
    url: str = ""
    html: str = ""
    markdown: str = ""

    def __init__(self, url: str):
        self.url = url

    def _save_all(self, file_path: str) -> None:
        data = self.__dict__
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def _save_payload(self, file_path: str, content: str) -> None:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

    @classmethod
    def load(cls, file_path: str) -> "Page":
        with open(file_path, "r") as file:
            data = json.load(file)
            return cls(**data)
