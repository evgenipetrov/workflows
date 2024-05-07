from abc import ABC, abstractmethod


class BaseType(ABC):
    data_type: str = ""

    @abstractmethod
    def _save_all(self, file_path: str) -> None:
        pass

    @abstractmethod
    def save_payload(self, file_path: str, content: str) -> None:
        pass

    @classmethod
    @abstractmethod
    def load(cls, data: dict) -> "BaseType":
        pass
