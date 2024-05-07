import argparse
import logging

from nodes.amazon_product_parser_node import AmazonProductParserNode
from nodes.browser_node import BrowserNode
from nodes.markdown_node import MarkdownNode
from nodes.openai_node import OpenAINode
from pipelines.base_pipeline import BasePipeline


class TestPipeline(BasePipeline):
    """Pipeline for testing purposes."""

    def __init__(self, project_name: str):
        """Initialize the TestPipeline.

        Args:
            project_name: The name of the project.
        """
        super().__init__(project_name)
        self.browser_node = BrowserNode(project_name)
        self.markdown_node = MarkdownNode(project_name)
        self.amazon_product_parser_node = AmazonProductParserNode(project_name)
        self.openai_node = OpenAINode(project_name)

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add pipeline-specific arguments to the parser.

        Args:
            parser: The argument parser to add arguments to.
        """
        parser.add_argument("--input_data_dir", type=str, help="CSV file with URLs to fetch HTML from")
        parser.add_argument("--url", type=str, help="URL for fetching HTML")

    def execute(self, args: argparse.Namespace) -> None:
        """Execute the pipeline.

        Args:
            args: The parsed command-line arguments.

        Raises:
            ValueError: If neither --input_data_dir nor --url is provided.
        """
        try:
            if args.input_data_dir:
                html_dir = self.browser_node.get_path(
                    input_path=args.input_data_dir, execute_js=True, node_name="get_html"
                )
            elif args.url:
                html_dir = self.browser_node.get_path(input_data=[args.url], execute_js=True, node_name="get_html")
            else:
                raise ValueError("Either --input_data_dir or --url must be provided.")

            markdown_dir = self.markdown_node.get_path(input_path=html_dir, node_name="get_markdown")
            amazon_dir = self.amazon_product_parser_node.get_path(input_path=html_dir, node_name="parse_amazon")

            system_prompt = "You are a blog writer who needs to write a blog post about the product."
            user_prompt = "Write a blog post about the product."
            openai_blog_dir = self.openai_node.get_path(
                input_path=markdown_dir,
                node_name="openai_blog",
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                openai_parameters={
                    "model": "gpt-3.5-turbo",
                    "temperature": 0.5,
                    "max_tokens": 2000,
                    "top_p": 1.0,
                    "frequency_penalty": 0.0,
                    "presence_penalty": 0.0,
                },
            )
        except Exception as e:
            logging.error(f"An error occurred during pipeline execution: {str(e)}")
            raise
