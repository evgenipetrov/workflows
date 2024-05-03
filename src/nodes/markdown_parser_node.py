import logging
import os
from datetime import timedelta

from markdownify import markdownify as md

from nodes.base_node import BaseNode
from operators.file_operator import FileOperator


class MarkdownParserNode(BaseNode):
    FILE_EXTENSION = "md"
    CACHE_DURATION = timedelta(hours=12)

    def __init__(self, project_name: str):
        super().__init__(project_name)
        self._logger = logging.getLogger(__name__)
        self._file_operator = FileOperator()

    def _load_data(self) -> None:
        self._logger.debug(f"Loading HTML files from directory: {self._input_folder}")
        html_files = self._file_operator.read_all_txts_in_folder(self._input_folder)
        self._logger.debug(f"Found HTML files: {len(html_files)}")
        for html_content in html_files:
            self._input_data.append(html_content)

    def _process(self) -> None:
        for file_path, html_content in self._input_data:
            markdown_content = self._convert_to_markdown(html_content)
            self._output_data.append((file_path, markdown_content))

    def _save_data(self) -> None:
        for file_path, markdown_content in self._output_data:
            markdown_filename = os.path.splitext(os.path.basename(file_path))[0] + ".md"
            output_file_path = os.path.join(self._output_folder, markdown_filename)
            with open(output_file_path, "w", encoding="utf-8") as file:
                file.write(markdown_content)
            self._logger.info(f"Markdown content successfully written to {output_file_path}")

    @staticmethod
    def _convert_to_markdown(html_content: str) -> str:
        markdown = md(html_content)
        cleaned_markdown = "\n".join(line for line in markdown.splitlines() if line.strip())
        return cleaned_markdown

    def _get_cache_duration(self) -> timedelta:
        return self.CACHE_DURATION
