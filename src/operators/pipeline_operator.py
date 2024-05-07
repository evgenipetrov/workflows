from typing import Optional, Dict, Type

from pipelines.base_pipeline import BasePipeline
from pipelines.test_pipeline import TestPipeline


class PipelineOperator:
    """Factory class to create pipelines."""

    pipelines: Dict[str, Type[BasePipeline]] = {
        "test": TestPipeline,
    }

    @staticmethod
    def create(pipeline_name: str, project_name: str) -> Optional[BasePipeline]:
        """Create a pipeline instance based on the provided pipeline name and project name.

        Args:
            pipeline_name: The name of the pipeline to create.
            project_name: The name of the project.

        Returns:
            An instance of the corresponding pipeline class if it exists, or None otherwise.
        """
        pipeline_class = PipelineOperator.pipelines.get(pipeline_name)
        if pipeline_class:
            return pipeline_class(project_name)
        return None
