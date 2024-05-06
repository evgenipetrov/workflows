from abc import ABC, abstractmethod


class BaseType(ABC):
    @abstractmethod
    def _save_all(self, file_path: str) -> None:
        pass

    @abstractmethod
    def _save_payload(self, file_path: str, content: str) -> None:
        pass

    @classmethod
    @abstractmethod
    def load(cls, file_path: str) -> "BaseType":
        pass
