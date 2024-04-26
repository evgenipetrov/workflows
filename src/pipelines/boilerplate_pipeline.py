from src.nodes.boilerplate_node import BoilerplateNode
from src.pipelines.base_pipeline import BasePipeline


class BoilerplatePipeline(BasePipeline):
    def __init__(self):
        self.boilerplate_node = BoilerplateNode()

    def add_arguments(self, parser):
        parser.add_argument("--url", type=str, required=True, help="URL")

    def execute(self, args):
        content = self.boilerplate_node.execute(args.url)
        print(content)
