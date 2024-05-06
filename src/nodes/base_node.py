import hashlib
import json
import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Any, Optional, Type, TypeVar

T = TypeVar("T")


class BaseNode(ABC):
    def __init__(self, project_name: str):
        self._project_name = project_name
        self._root_path = os.getenv("PROJECT_DATA_ROOT_PATH", "data")
        self._logger = logging.getLogger(__name__)
        self._input_data: List[Any] = []
        self._output_data: List[Any] = []
        self._input_path: Optional[str] = None
        self._output_path: str = ""
        self._kwargs: dict = {}

    def _load_data(self, data_class: Type[T]) -> None:
        if self._input_path:
            all_json_file = os.path.join(self._input_path, "all.json")
            if os.path.exists(all_json_file):
                with open(all_json_file, "r") as file:
                    data = json.load(file)
                    self._input_data = []
                    for item in data:
                        input_value = item.get(next(iter(item)), "")
                        obj = data_class(input_value)
                        for key, value in item.items():
                            if key != next(iter(item)):
                                setattr(obj, key, value)
                        self._input_data.append(obj)
            else:
                self._logger.warning("all.json file not found in the input path.")
        elif self._input_data:
            self._input_data = [data_class(input_value) for input_value in self._input_data]

    @abstractmethod
    def _process_item(self, item: Any) -> Any:
        pass

    @abstractmethod
    def _save_data(self) -> None:
        pass

    @abstractmethod
    def _get_cache_duration(self) -> timedelta:
        pass

    @abstractmethod
    def _get_input_type(self) -> Type[T]:
        pass

    def _get_output_folder(self, base_path: str, **kwargs: Any) -> str:
        hash_input = json.dumps(kwargs, sort_keys=True).encode("utf-8")
        hash_output = hashlib.md5(hash_input).hexdigest()
        output_folder = os.path.join(base_path, hash_output)

        if os.path.exists(output_folder) and self._is_cache_valid(output_folder):
            self._logger.info(f"Using valid cache at {output_folder}")
            self._is_cache_valid = True
        else:
            self._logger.info(f"Cache not found or invalid at {output_folder}")
            self._is_cache_valid = False

        return output_folder

    def _create_output_folder(self, output_folder: str) -> None:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self._logger.info(f"Creating new output folder at {output_folder}")

    def _is_cache_valid(self, folder_path: str) -> bool:
        file_paths = [os.path.join(root, file) for root, _, files in os.walk(folder_path) for file in files]
        if file_paths:
            latest_mod_time = max(os.path.getmtime(file_path) for file_path in file_paths)
            return datetime.now() - datetime.fromtimestamp(latest_mod_time) <= self._get_cache_duration()
        return False

    def _execute(
            self,
            input_path: Optional[str] = None,
            input_data: Optional[List[Any]] = None,
            node_name: Optional[str] = None,
            **kwargs: Any,
    ) -> None:
        if input_path is not None:
            self._input_path = input_path
            self._load_data(self._get_input_type())
        elif input_data is not None:
            self._input_data = input_data
        else:
            self._logger.error("No input path or input data provided.")
            return

        if not self._input_data:
            self._logger.error("No input data loaded.")
            return

        # Use the provided node_name or default to the class name
        if node_name is None:
            node_name = self.__class__.__name__

        # Create the base path using the provided node_name
        base_path = os.path.join(self._root_path, self._project_name, node_name)
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        # Merge input_path and input_data with kwargs (exclude node_name)
        self._kwargs = {
            "input_path": input_path,
            "input_data": input_data,
            "node_name": node_name,
            **kwargs,
        }

        self._output_path = self._get_output_folder(base_path, **self._kwargs)

        if not self._is_cache_valid:
            self._create_output_folder(self._output_path)
            self._output_data = [self._process_item(item) for item in self._input_data]
            self._save_data()

    def get_path(
            self,
            input_path: Optional[str] = None,
            input_data: Optional[List[Any]] = None,
            node_name: Optional[str] = None,
            **kwargs: Any,
    ) -> str:
        self._execute(input_path, input_data, node_name, **kwargs)
        return self._output_path

    def get_data(
            self,
            input_path: Optional[str] = None,
            input_data: Optional[List[Any]] = None,
            node_name: Optional[str] = None,
            **kwargs: Any,
    ) -> List[Any]:
        self._execute(input_path, input_data, node_name, **kwargs)
        return self._output_data
