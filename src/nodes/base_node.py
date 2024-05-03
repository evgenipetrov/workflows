from abc import ABC, abstractmethod
from datetime import timedelta
from typing import List, Any

from operators.cache_operator import CacheOperator


class BaseNode(ABC):
    def __init__(self, project_name: str):
        # Initialize the node with the project name
        self._project_name = project_name

        # Create a cache manager instance for the node
        self._cache_manager = CacheOperator(project_name, self.__class__.__name__, self._get_cache_duration())

        # Initialize input and processing data containers
        self._input_data: List[Any] = []
        self._output_data: List[Any] = []

        # Initialize input and output folder variables
        self._input_folder: str = ""
        self._output_folder: str = ""

        # Initialize kwargs variable
        self._kwargs: dict = {}

    def execute(self, input_folder: str, **kwargs) -> str:
        # Store the input folder and kwargs internally
        self._input_folder = input_folder
        self._kwargs = kwargs

        # Load the input data
        self._load_data()

        # Check if input data is available
        if not self._input_data:
            self._logger.error("No input data loaded.")
            return ""

        # Get or create the output folder based on cache validity
        self._output_folder, is_cache_valid = self._cache_manager.get_or_create_output_folder(input_folder=input_folder, **kwargs)

        # If cache is not valid, process the data and save it
        if not is_cache_valid:
            self._process()
            self._save_data()

        # Return the output folder path
        return self._output_folder

    @abstractmethod
    def _load_data(self) -> None:
        # Abstract method to load input data
        # Implement this method in the child class to load data specific to the node
        pass

    @abstractmethod
    def _process(self) -> None:
        # Abstract method to process the input data
        # Implement this method in the child class to perform node-specific data processing
        pass

    @abstractmethod
    def _save_data(self) -> None:
        # Abstract method to save the processed data
        # Implement this method in the child class to save the processed data in the desired format
        pass

    @abstractmethod
    def _get_cache_duration(self) -> timedelta:
        # Abstract method to get the cache duration for the node
        # Implement this method in the child class to specify the cache duration
        pass
