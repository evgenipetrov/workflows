import logging
from src.pipelines.base_pipeline import BasePipeline
from src.nodes.boilerplate_node import BoilerplateNode


class BoilerplatePipeline(BasePipeline):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.boilerplate_node = BoilerplateNode()

    def add_arguments(self, parser):
        parser.add_argument("--url", type=str, required=True, help="URL")

    def execute(self, args):
        self.logger.info("Starting pipeline execution.")
        content = self.boilerplate_node.execute(args.url)
        self.logger.info(f"Pipeline execution completed. Content: {content}")
