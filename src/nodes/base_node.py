import os
from abc import ABC, abstractmethod
from datetime import timedelta

from src.operators.cache_operator import CacheOperator


class BaseNode(ABC):
    def __init__(self, project_name, input_folder=None):
        self.project_name = project_name
        self.input_folder = None if input_folder is None else os.path.join(project_name, input_folder)
        self.cache_manager = CacheOperator(project_name, self.__class__.__name__, self._get_cache_duration())

    def execute(self, **kwargs):
        output_folder, is_cache_valid = self.cache_manager.get_or_create_output_folder(**kwargs)
        if not is_cache_valid:
            data_list = self._load_data()
            self._process(data_list, output_folder)
        return output_folder

    @abstractmethod
    def _load_data(self):
        """Load data from the input folder; must return a list."""
        pass

    @abstractmethod
    def _process(self, data_list, output_folder):
        """Process data and store results in the specified output folder."""
        pass

    def _get_cache_duration(self):
        """Override this method in subclasses to define specific cache durations."""
        return timedelta(hours=1)  # Default cache duration
