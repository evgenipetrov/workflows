import pandas as pd

from datatypes.base_type import BaseType


class Html(BaseType):
    def __init__(self, content: str):
        self.content = content

    def save(self, file_path: str) -> None:
        with open(file_path, "w") as file:
            file.write(self.content)

    def save_to_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        data = {"html": [self.content]}
        return df.append(pd.DataFrame(data), ignore_index=True)

    @classmethod
    def load(cls, file_path: str) -> "Html":
        with open(file_path, "r") as file:
            content = file.read()
            return cls(content)

    @classmethod
    def load_from_dataframe(cls, row: pd.Series) -> "Html":
        return cls(row["html"])
