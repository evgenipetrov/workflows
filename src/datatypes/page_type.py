import json

import pandas as pd

from datatypes.base_type import BaseType


class Page(BaseType):
    def __init__(self, url: str, html: str = "", markdown: str = ""):
        self.url = url
        self.html = html
        self.markdown = markdown

    def _save_all(self, file_path: str) -> None:
        data = {"url": self.url, "html": self.html, "markdown": self.markdown}
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def _save_payload(self, file_path: str, content: str) -> None:
        with open(file_path, "w") as file:
            file.write(content)

    def save_to_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        data = {"url": [self.url], "html": [self.html], "markdown": [self.markdown]}
        return pd.concat([df, pd.DataFrame(data)], ignore_index=True)

    @classmethod
    def load(cls, file_path: str) -> "Page":
        with open(file_path, "r") as file:
            data = json.load(file)
            url = data.get("url", "")
            html = data.get("html", "")
            markdown = data.get("markdown", "")
            return cls(url, html, markdown)

    @classmethod
    def load_from_dataframe(cls, row: pd.Series) -> "Page":
        return cls(row["url"], row["html"], row["markdown"])
