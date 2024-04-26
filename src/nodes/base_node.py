import hashlib
from abc import ABC, abstractmethod
from datetime import timedelta

from src.services.cache_service import CacheService


class BaseNode(ABC):
    def __init__(self, project_name):
        self.project_name = project_name
        self.node_folder_name = self.__class__.__name__
        self.cache_manager = CacheService(self.project_name, self.node_folder_name, self.get_cache_duration())

    def execute(self, input_data, **kwargs):
        identifier = self.create_identifier(input_data, **kwargs)
        cache_path = self.cache_manager.cache_exists(identifier, self.FILE_EXTENSION)
        if cache_path:
            return self.cache_manager.load_cached_data(cache_path)

        result = self.process(input_data, **kwargs)

        cache_path = self.cache_manager.get_cache_path(identifier, self.FILE_EXTENSION)
        self.cache_manager.save_data_to_cache(result, cache_path)
        return result

    @abstractmethod
    def process(self, input_data, **kwargs):
        """Process data in a way specific to the node type."""
        pass

    def create_identifier(self, input_data, **kwargs):
        # Simplified example
        base_string = str(input_data) + str(kwargs)
        return hashlib.md5(base_string.encode()).hexdigest()

    def get_cache_duration(self):
        return getattr(self, "CACHE_DURATION", timedelta(hours=1))  # Default to 1 hour if not set
