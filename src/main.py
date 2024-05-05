import argparse
import logging
import sys

from dotenv import load_dotenv

from operators.logging_operator import LoggingOperator
from operators.pipeline_operator import PipelineOperator

load_dotenv()


def main():
    LoggingOperator.setup_logging()

    parser = argparse.ArgumentParser(description="Run a specified pipeline on a project with dynamic parameters.")
    parser.add_argument("--project_name", type=str, required=True, help="Name of the project")
    parser.add_argument("--workflow_name", type=str, required=True, help="Name of the workflow")

    # Parse arguments early to get the pipeline name
    args, remaining_argv = parser.parse_known_args()

    # Create pipeline using the factory
    pipeline = PipelineOperator.create(args.workflow_name, args.project_name)
    if not pipeline:
        logging.error(f"Invalid workflow name provided: {args.workflow_name}")
        sys.exit(1)

    # Allow the pipeline to add its specific arguments
    pipeline.add_arguments(parser)

    # Reparse args with new context
    args = parser.parse_args()

    # Execute the pipeline
    pipeline.execute(args)


if __name__ == "__main__":
    main()
