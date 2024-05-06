import pandas as pd

from datatypes.base_type import BaseType


class Url(BaseType):
    def __init__(self, url: str):
        self.url = url

    def save(self, file_path: str) -> None:
        with open(file_path, "w") as file:
            file.write(self.url)

    def save_to_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        data = {"url": [self.url]}
        return df.append(pd.DataFrame(data), ignore_index=True)

    @classmethod
    def load(cls, file_path: str) -> "Url":
        with open(file_path, "r") as file:
            url = file.read().strip()
            return cls(url)

    @classmethod
    def load_from_dataframe(cls, row: pd.Series) -> "Url":
        return cls(row["url"])
