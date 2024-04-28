from src.pipelines.boilerplate_pipeline import BoilerplatePipeline
from src.pipelines.page_to_markdown_pipeline import PageToMarkdownPipeline


class PipelineOperator:
    # factory class to create pipelines
    pipelines = {
        "boilerplate": BoilerplatePipeline,
        "page_to_markdown": PageToMarkdownPipeline,
    }

    @staticmethod
    def create(pipeline_name, project_name):
        pipeline_class = PipelineOperator.pipelines.get(pipeline_name)
        if pipeline_class:
            return pipeline_class(project_name)
        return None
