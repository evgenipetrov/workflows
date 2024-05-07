import json

from datatypes.base_type import BaseType


class Markdown(BaseType):
    address: str = ""
    body: str = ""

    def __init__(self, address: str = "", body: str = ""):
        self.address = address
        self.body = body

    def _save_all(self, file_path: str) -> None:
        data = self.__dict__
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def save_payload(self, file_path: str, content: str) -> None:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

    @classmethod
    def load(cls, data: dict) -> "Markdown":
        instance = cls()
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return instance
