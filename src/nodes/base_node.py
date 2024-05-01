from abc import ABC, abstractmethod

from operators.cache_operator import CacheOperator


class BaseNode(ABC):
    def __init__(self, project_name):
        self._project_name = project_name
        self._cache_manager = CacheOperator(project_name, self.__class__.__name__, self._get_cache_duration())
        self._input_data = []
        self._processing_data = []

    def execute(self, input_folder, **kwargs):
        self._load_data(input_folder, **kwargs)
        if self._input_data is None or not self._input_data:
            self._logger.error("No input data loaded.")
            return None  # Or handle this case appropriately

        output_folder, is_cache_valid = self._cache_manager.get_or_create_output_folder(**kwargs)
        if not is_cache_valid:
            # self._processing_data = self._input_data.copy()
            self._process(output_folder)
            self._save_data(output_folder)

        return output_folder

    @abstractmethod
    def _load_data(self, input_path, **kwargs):
        pass

    @abstractmethod
    def _process(self, output_folder):
        pass

    @abstractmethod
    def _save_data(self, output_folder):
        pass

    @abstractmethod
    def _get_cache_duration(self):
        pass
