import logging
from datetime import timedelta

from markdownify import markdownify as md

from src.nodes.base_node import BaseNode


class MarkdownParserNode(BaseNode):
    FILE_EXTENSION = "md"
    CACHE_DURATION = timedelta(hours=12)  # Cache duration of 12 hours

    def __init__(self, project_name):
        super().__init__(project_name)
        self.logger = logging.getLogger(__name__)

    def process(self, input_data, **kwargs):
        self.logger.info(f"Starting conversion of HTML to Markdown")
        # Convert HTML to Markdown
        markdown = md(input_data)

        # Remove empty lines
        cleaned_markdown = "\n".join(line for line in markdown.splitlines() if line.strip())
        self.logger.info(f"Successfully converted HTML to Markdown")
        return cleaned_markdown
