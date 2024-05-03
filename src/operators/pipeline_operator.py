from pipelines.page_to_markdown_pipeline import PageToMarkdownPipeline
from pipelines.summarize_product_description_pipeline import SummarizeProductDescriptionPipeline


class PipelineOperator:
    # factory class to create pipelines
    pipelines = {
        "test": SummarizeProductDescriptionPipeline,
        "page_to_markdown": PageToMarkdownPipeline,
    }

    @staticmethod
    def create(pipeline_name, project_name):
        pipeline_class = PipelineOperator.pipelines.get(pipeline_name)
        if pipeline_class:
            return pipeline_class(project_name)
        return None
