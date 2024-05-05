from nodes.browser_node import BrowserNode
from pipelines.base_pipeline import BasePipeline


class GetHtmlPipeline(BasePipeline):
    def __init__(self, project_name):
        super().__init__(project_name)
        self.browser_node = BrowserNode(project_name)

    def add_arguments(self, parser):
        parser.add_argument("--input_data_dir", type=str, help="CSV file with URLs to fetch HTML from")
        parser.add_argument("--url", type=str, help="URL for fetching HTML")

    def execute(self, args):
        if args.input_data_dir:
            html_dir = self.browser_node.get_path(input_path=args.input_data_dir, execute_js=True, node_name="get_html")
        elif args.url:
            html_dir = self.browser_node.get_path(input_data=[args.url], execute_js=True, node_name="get_html")
        else:
            raise ValueError("Either --input_data_dir or --url must be provided.")
        return html_dir
