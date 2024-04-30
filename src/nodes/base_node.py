import os
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, List

from operators.cache_operator import CacheOperator


class BaseNode(ABC):
    def __init__(self, project_name, input_folder=None):
        self._project_name = project_name
        self._input_folder = None if input_folder is None else os.path.join(project_name, input_folder)
        self._cache_manager = CacheOperator(project_name, self.__class__.__name__, self._get_cache_duration())
        self._input_data: List[Any] = []
        self._processing_data: List[Any] = []

    def execute(self, **kwargs):
        output_folder, is_cache_valid = self._cache_manager.get_or_create_output_folder(**kwargs)
        if not is_cache_valid:
            self._input_data = self._load_data()
            self._processing_data = self._input_data.copy()  # Create a copy of the input data for processing
            self._process(output_folder)
            self._save_data(output_folder)
        return output_folder

    @abstractmethod
    def _load_data(self, **kwargs):
        """Load data; must return a list."""
        pass

    @abstractmethod
    def _process(self, output_folder):
        """Process data and store intermediate results in self._processing_data."""
        pass

    @abstractmethod
    def _save_data(self, output_folder):
        """Save the processed data in the specified output folder."""
        pass

    def _get_cache_duration(self):
        """Override this method in subclasses to define specific cache durations."""
        return timedelta(hours=1)  # Default cache duration
