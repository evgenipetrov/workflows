from pipelines.get_html_pipeline import GetHtmlPipeline


class PipelineOperator:
    # factory class to create pipelines
    pipelines = {
        # "test": GetHtmlPipeline,
        # "summarize": SummarizeProductDescriptionPipeline,
        "get_html": GetHtmlPipeline,
    }

    @staticmethod
    def create(pipeline_name, project_name):
        pipeline_class = PipelineOperator.pipelines.get(pipeline_name)
        if pipeline_class:
            return pipeline_class(project_name)
        return None
