import json

import pandas as pd

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
        with open(file_path, "w") as file:
            file.write(content)

    def save_to_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        data = {key: [value] for key, value in self.__dict__.items()}
        return pd.concat([df, pd.DataFrame(data)], ignore_index=True)

    @classmethod
    def load(cls, file_path: str) -> "Page":
        with open(file_path, "r") as file:
            data = json.load(file)
            return cls(**data)

    @classmethod
    def load_from_dataframe(cls, row: pd.Series) -> "Page":
        return cls(**row.to_dict())
