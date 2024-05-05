import logging
import os
from datetime import timedelta
from typing import List

import openai

from nodes.base_node import BaseNode
from operators.file_operator import FileOperator


class OpenAINode(BaseNode):
    FILE_EXTENSION = "txt"
    CACHE_DURATION = timedelta(hours=24)

    def __init__(self, project_name: str):
        super().__init__(project_name)
        self._logger = logging.getLogger(__name__)
        self._file_operator = FileOperator()

        # Load the API key from the .env file
        # load_dotenv()
        self._api_key = os.getenv("OPENAI_API_KEY")

        # Set default values for parameters
        self._default_model = "gpt-4-turbo"
        self._default_temperature = 0.7
        self._default_system_prompt = "You are a helpful assistant."
        self._default_max_tokens = 100

    def _load_data(self) -> None:
        # Check if the input folder is provided
        if self._input_folder:
            # Load data from the input folder
            self._logger.debug(f"Loading text files from directory: {self._input_folder}")
            text_files = self._file_operator.read_all_txts_in_folder(self._input_folder)
            self._logger.debug(f"Found text files: {len(text_files)}")
            self._input_data = text_files
        else:
            # No input folder provided, use an empty list for input data
            self._input_data = [""]

    def _process(self) -> None:
        # Get the model from kwargs or use the default
        model = self._kwargs.get("model", self._default_model)

        # Get the system prompt from kwargs or use the default
        system_prompt = self._kwargs.get("system_prompt", self._default_system_prompt)

        # Get the user prompt from kwargs
        user_prompt = self._kwargs.get("user_prompt", "")

        # Get the temperature from kwargs or use the default
        temperature = self._kwargs.get("temperature", self._default_temperature)

        # Get the max_tokens from kwargs or use the default
        max_tokens = self._kwargs.get("max_tokens", self._default_max_tokens)

        # Create an OpenAI client instance
        client = openai.OpenAI()

        # Process each input text file or the direct prompt
        for input_text in self._input_data:
            # Initialize conversation history for each input text
            conversation_history: List[dict] = []

            # Append the system prompt to the conversation history
            conversation_history.append({"role": "system", "content": system_prompt})

            # Concatenate the input text with the user prompt
            full_prompt = f"{input_text}\n{user_prompt}"

            # Append the full prompt to the conversation history
            conversation_history.append({"role": "user", "content": full_prompt})

            # Make the API request to OpenAI
            response = client.chat.completions.create(
                model=model, messages=conversation_history, temperature=temperature, max_tokens=max_tokens
            )

            # Extract the assistant's response from the API response
            assistant_response = response.choices[0].message.content

            # Append the assistant's response to the output data
            self._output_data.append(assistant_response)

    def _save_data(self) -> None:
        # Save the conversation history to a file in the output folder
        output_file = os.path.join(self._output_path, "conversation_history.txt")
        with open(output_file, "w") as file:
            for response in self._output_data:
                file.write(f"Assistant: {response}\n")

    def _get_cache_duration(self) -> timedelta:
        # Set the cache duration to 1 hour
        return timedelta(hours=1)
