from src.nodes.browser_node import BrowserNode
from src.nodes.markdown_parser_node import MarkdownParserNode
from src.pipelines.base_pipeline import BasePipeline


class PageToMarkdownPipeline(BasePipeline):
    def __init__(self, project_name):
        super().__init__(project_name)
        # Initialize each node with project name. Assume markdown parser can handle direct data.
        self.browser_node = BrowserNode(project_name)
        self.markdown_parser_node = MarkdownParserNode(project_name)

    def add_arguments(self, parser):
        parser.add_argument("--url", type=str, required=True, help="URL for fetching HTML")

    def execute(self, args):
        html_dir = self.browser_node.execute(args.url)
        markdown_content = self.markdown_parser_node.execute(html_dir)  # Directly pass HTML content
        return markdown_content
