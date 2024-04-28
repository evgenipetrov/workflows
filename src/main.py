import argparse
import logging
import sys

from dotenv import load_dotenv

from src.operators.logging_operator import LoggingOperator
from src.operators.pipeline_operator import PipelineOperator

load_dotenv()


def main():
    LoggingOperator.setup_logging()

    parser = argparse.ArgumentParser(description="Run a specified pipeline on a project with dynamic parameters.")
    parser.add_argument("--project_name", type=str, required=True, help="Name of the project")
    parser.add_argument("--pipeline_name", type=str, required=True, help="Name of the pipeline")

    # Parse arguments early to get the pipeline name
    args, remaining_argv = parser.parse_known_args()

    # Create pipeline using the factory
    pipeline = PipelineOperator.create(args.pipeline_name, args.project_name)
    if not pipeline:
        logging.error(f"Invalid pipeline name provided: {args.pipeline_name}")
        sys.exit(1)

    # Allow the pipeline to add its specific arguments
    pipeline.add_arguments(parser)

    # Re-parse args with new context
    args = parser.parse_args()

    # Execute the pipeline
    pipeline.execute(args)


if __name__ == "__main__":
    main()
