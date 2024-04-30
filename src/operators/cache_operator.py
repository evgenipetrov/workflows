import hashlib
import logging
import os
from datetime import datetime


class CacheOperator:
    def __init__(self, project_name, node_folder_name, cache_duration):
        self.root_path = os.getenv("PROJECT_DATA_ROOT_PATH", "data")
        self.base_path = os.path.join(self.root_path, project_name, node_folder_name)
        self.cache_duration = cache_duration
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        self.logger = logging.getLogger(__name__)

    def get_or_create_output_folder(self, **kwargs):
        # Create a hash of the kwargs to form a unique directory name
        hash_input = str(kwargs).encode("utf-8")
        hash_output = hashlib.md5(hash_input).hexdigest()
        output_folder = os.path.join(self.base_path, hash_output)

        if os.path.exists(output_folder) and self._is_cache_valid(output_folder):
            self.logger.info("Using valid cache at {}".format(output_folder))
            return output_folder, True
        else:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            self.logger.info("Creating new output folder at {}".format(output_folder))
            return output_folder, False

    def _is_cache_valid(self, folder_path):
        """Check if the cache is still valid by comparing the modification time."""
        latest_mod_time = None
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                mod_time = os.path.getmtime(file_path)
                if latest_mod_time is None or mod_time > latest_mod_time:
                    latest_mod_time = mod_time

        if latest_mod_time:
            latest_mod_time = datetime.fromtimestamp(latest_mod_time)
            if datetime.now() - latest_mod_time <= self.cache_duration:
                return True
        return False
