import logging
import os
from datetime import timedelta

from markdownify import markdownify as md

from nodes.base_node import BaseNode


class MarkdownParserNode(BaseNode):
    FILE_EXTENSION = "md"
    CACHE_DURATION = timedelta(hours=12)

    def __init__(self, project_name):
        super().__init__(project_name)
        self._logger = logging.getLogger(__name__)

    def _load_data(self, input_path, **kwargs):
        self._logger.debug(f"Loading HTML files from directory: {input_path}")
        html_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".html")]
        self._logger.debug(f"Found HTML files: {html_files}")
        for file_path in html_files:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    html_content = file.read()
                    self._input_data.append((file_path, html_content))
            except Exception as e:
                self._logger.error(f"Failed to read file {file_path}: {e}")

    def _process(self, output_folder):
        self._processing_data = []
        for file_path, html_content in self._input_data:
            markdown_content = self._convert_to_markdown(html_content)
            self._processing_data.append((file_path, markdown_content))

    @staticmethod
    def _convert_to_markdown(html_content):
        markdown = md(html_content)
        cleaned_markdown = "\n".join(line for line in markdown.splitlines() if line.strip())
        return cleaned_markdown

    def _save_data(self, output_folder):
        for file_path, markdown_content in self._processing_data:
            markdown_filename = os.path.splitext(os.path.basename(file_path))[0] + ".md"
            output_file_path = os.path.join(output_folder, markdown_filename)
            with open(output_file_path, "w", encoding="utf-8") as file:
                file.write(markdown_content)
            self._logger.info(f"Markdown content successfully written to {output_file_path}")

    def _get_cache_duration(self):
        return self.CACHE_DURATION
