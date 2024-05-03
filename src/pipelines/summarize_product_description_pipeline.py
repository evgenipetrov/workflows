from nodes.open_ai_node import OpenAINode
from pipelines.base_pipeline import BasePipeline


class SummarizeProductDescriptionPipeline(BasePipeline):
    def __init__(self, project_name):
        super().__init__(project_name)
        # Initialize each node with project name. Assume Markdown parser can handle direct data.
        self.openai_node = OpenAINode(project_name)

    def add_arguments(self, parser):
        parser.add_argument("--input_data_dir", type=str, required=True, help="URL for fetching HTML")

    def execute(self, args):
        product_markdown_dir = r"D:\Projects\workflows\project_data\test\MarkdownParserNode\015867a9f942e59b5d1e160a7606ed45"

        user_prompt = "Summarize the product description"
        summary_dir = self.openai_node.execute(args.input_data_dir, user_prompt=user_prompt)
        return summary_dir
