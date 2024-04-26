import argparse
import sys
import logging

from pipelines.boilerplate_pipeline import BoilerplatePipeline


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="Run a specified pipeline on a project with dynamic parameters.")
    parser.add_argument("--project_name", type=str, required=True, help="Name of the project")
    parser.add_argument("--pipeline_name", type=str, required=True, help="Name of the pipeline")

    # Temporary parse to get pipeline name
    known_args, remaining_argv = parser.parse_known_args(sys.argv[1:3])

    # Instantiate the appropriate pipeline
    pipelines = {
        "boilerplate": BoilerplatePipeline(),
    }

    pipeline = pipelines.get(known_args.pipeline_name)
    if not pipeline:
        logging.error(f"Invalid pipeline name provided: {known_args.pipeline_name}")
        sys.exit(1)

    # Let the pipeline define its specific arguments
    pipeline.add_arguments(parser)

    # Parse all arguments again with new context
    args = parser.parse_args()

    # Execute the pipeline
    pipeline.execute(args)


if __name__ == "__main__":
    main()
