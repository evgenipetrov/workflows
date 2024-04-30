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

    def _load_data(self, input_folder):
        """Load HTML files from the specified input directory and return as a list of (file_path, HTML contents)."""
        html_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".html")]
        return [(file_path, open(file_path, "r", encoding="utf-8").read()) for file_path in html_files]

    def _process(self, output_folder):
        """Convert HTML to Markdown and store in self._processing_data."""
        self._processing_data = []
        for file_path, html_content in self._input_data:
            markdown_content = self._convert_to_markdown(html_content)
            data_item = file_path, markdown_content
            self._processing_data.append(data_item)

    @staticmethod
    def _convert_to_markdown(html_content):
        """Convert HTML to Markdown."""
        markdown = md(html_content)
        cleaned_markdown = "\n".join(line for line in markdown.splitlines() if line.strip())
        return cleaned_markdown

    def _save_data(self, output_folder):
        """Save the processed Markdown data to files in the specified output folder."""
        for file_path, markdown_content in self._processing_data:
            markdown_filename = os.path.splitext(os.path.basename(file_path))[0] + ".md"
            output_path = os.path.join(output_folder, markdown_filename)
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(markdown_content)
            self._logger.info(f"Markdown content successfully written to {output_path}")

    def execute(self, input_folder, **kwargs):
        # Integrate input_folder into kwargs to pass to cache manager
        kwargs["input_folder"] = input_folder
        """Processes HTML files in the given input folder into Markdown files."""
        self._input_data = self._load_data(input_folder)
        self._processing_data = self._input_data.copy()
        output_folder, is_cache_valid = self._cache_manager.get_or_create_output_folder(**kwargs)
        if not is_cache_valid:
            self._process(output_folder)
            self._save_data(output_folder)
        return output_folder

    def _get_cache_duration(self):
        return self.CACHE_DURATION  # Overrides the base class method
