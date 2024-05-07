import json

from datatypes.base_type import BaseType


class Page(BaseType):
    address: str = ""
    html: str = ""

    def __init__(self, address: str = ""):
        self.address = address

    def _save_all(self, file_path: str) -> None:
        data = self.__dict__
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def save_payload(self, file_path: str, content: str) -> None:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

    @classmethod
    def load(cls, data: dict) -> "Page":
        instance = cls()
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return instance
