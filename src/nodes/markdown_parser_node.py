import logging
import os
from datetime import timedelta

from markdownify import markdownify as md

from src.nodes.base_node import BaseNode


class MarkdownParserNode(BaseNode):
    FILE_EXTENSION = "md"
    CACHE_DURATION = timedelta(hours=12)

    def __init__(self, project_name):
        super().__init__(project_name)
        self.logger = logging.getLogger(__name__)

    def execute(self, input_folder, **kwargs):
        """Processes HTML files in the given input folder into Markdown files."""
        output_folder, is_cache_valid = self.cache_manager.get_or_create_output_folder(**kwargs)
        if not is_cache_valid:
            html_files_contents = self._load_data(input_folder)
            for file_path, html_content in html_files_contents:
                markdown_content = self._process(html_content)
                # Deduce markdown filename from HTML filename
                markdown_filename = os.path.splitext(os.path.basename(file_path))[0] + ".md"
                self._write_to_file(markdown_content, output_folder, markdown_filename)
        return output_folder

    def _load_data(self, input_folder):
        """Load HTML files from the specified input directory and return as a list of (file_path, HTML contents)."""
        html_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".html")]
        return [(file_path, open(file_path, "r", encoding="utf-8").read()) for file_path in html_files]

    def _process(self, html_content):
        """Convert HTML to Markdown directly."""
        markdown = md(html_content)
        cleaned_markdown = "\n".join(line for line in markdown.splitlines() if line.strip())
        return cleaned_markdown

    def _write_to_file(self, markdown_content, output_folder, filename):
        """Writes the markdown content to a file in the specified output folder using the provided filename."""
        output_path = os.path.join(output_folder, filename)
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(markdown_content)
        self.logger.info(f"Markdown content successfully written to {output_path}")
