import logging
import os
from datetime import datetime


class CacheService:
    def __init__(self, project_name, node_folder_name, cache_duration):
        root_path = os.getenv("DATA_ROOT_PATH", "data")
        self.base_path = os.path.join(root_path, project_name, node_folder_name)
        self.cache_duration = cache_duration

        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        self.logger = logging.getLogger(__name__)

    def get_cache_path(self, identifier, extension="txt"):
        now = datetime.now()
        date_folder = now.strftime("%Y-%m-%d")
        # Format: timestamp.identifier.extension
        file_name = f"{now.strftime('%H-%M-%S')}.{identifier}.{extension}"
        full_path = os.path.join(self.base_path, date_folder, file_name)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        return full_path

    def cache_exists(self, identifier, extension="txt"):
        self.logger.info(f"Checking cache for identifier: {identifier} and extension: {extension}")
        now = datetime.now()
        for date_folder in os.listdir(self.base_path):
            date_path = os.path.join(self.base_path, date_folder)
            if not os.path.isdir(date_path):
                continue
            for file_name in os.listdir(date_path):
                # Check if the file starts with the timestamp and contains the identifier
                parts = file_name.split(".")
                if len(parts) > 2 and parts[1] == identifier and parts[2] == extension:
                    full_path = os.path.join(date_path, file_name)
                    file_time = datetime.fromtimestamp(os.path.getmtime(full_path))
                    if now - file_time <= self.cache_duration:
                        self.logger.info(f"Cache found for identifier: {identifier} at path: {full_path}")
                        return full_path
        self.logger.info(f"No cache found for identifier: {identifier}")
        return None

    def load_cached_data(self, cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            self.logger.error(f"Failed to load cached data: {e}")
            return None

    def save_data_to_cache(self, data, cache_path):
        try:
            with open(cache_path, "w", encoding="utf-8") as file:  # Specify UTF-8 encoding
                if data:
                    file.write(data)
                    self.logger.info(f"Data successfully written to {cache_path}.")
                else:
                    self.logger.warning(f"Attempted to write empty data to {cache_path}.")
        except Exception as e:
            self.logger.error(f"Failed to save data to cache: {e}")
