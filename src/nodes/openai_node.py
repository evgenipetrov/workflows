import json
import logging
import os
from datetime import timedelta
from typing import Any, Union

from dotenv import load_dotenv
from openai import OpenAI

from datatypes.amazon_product_type import AmazonProduct
from datatypes.markdown_type import Markdown
from datatypes.openai_chat_type import OpenAIChat
from datatypes.page_type import Page
from datatypes.url_type import Url
from nodes.base_node import BaseNode

load_dotenv()


class OpenAINode(BaseNode):
    CACHE_DURATION = timedelta(hours=24)

    def __init__(self, project_name: str):
        super().__init__(project_name)
        self._logger = logging.getLogger(__name__)
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def _load_data_item(self, file_path: str) -> Union[Page, AmazonProduct]:
        if "page" in file_path:
            return Page.load(file_path)
        elif "amazon_product" in file_path:
            return AmazonProduct.load(file_path)
        else:
            raise ValueError(f"Unsupported input type for file: {file_path}")

    def _process_item(self, item: Any) -> Any:
        """Process a single item by constructing the appropriate prompt.

        Args:
            item: The item to process (Url, Page, Markdown, or AmazonProduct object).

        Returns:
            The processed item with the generated response.
        """
        system_prompt = self._kwargs.get("system_prompt", "")
        user_prompt = self._kwargs.get("user_prompt", "")

        if isinstance(item, Url):
            return self._process_url(item, system_prompt, user_prompt)
        elif isinstance(item, Page):
            return self._process_page(item, system_prompt, user_prompt)
        elif isinstance(item, Markdown):
            return self._process_markdown(item, system_prompt, user_prompt)
        elif isinstance(item, AmazonProduct):
            return self._process_amazon_product(item, system_prompt, user_prompt)
        else:
            raise ValueError(f"Unsupported item type: {type(item)}")

    def _process_url(self, url: Url, system_prompt: str, user_prompt: str) -> OpenAIChat:
        """Process a Url object by constructing the prompt.

        Args:
            url: The Url object to process.
            system_prompt: The system prompt for the OpenAI API.
            user_prompt: The user prompt for the OpenAI API.

        Returns:
            An instance of OpenAIChat with the generated response.
        """
        try:
            user_prompt = f"{user_prompt}\n\nURL: {url.address}"
            response = self._generate_response(system_prompt=system_prompt, user_prompt=user_prompt)
            return OpenAIChat(system_prompt=system_prompt, user_prompt=user_prompt, response=response)
        except Exception as e:
            self._logger.error(f"Failed to process URL: {url.address}. Error: {e}")
            return None

    def _process_page(self, page: Page, system_prompt: str, user_prompt: str) -> OpenAIChat:
        """Process a Page object by constructing the prompt.

        Args:
            page: The Page object to process.
            system_prompt: The system prompt for the OpenAI API.
            user_prompt: The user prompt for the OpenAI API.

        Returns:
            An instance of OpenAIChat with the generated response.
        """
        try:
            user_prompt = f"{user_prompt}\n\nWebpage content:\n{page.html}"
            response = self._generate_response(system_prompt=system_prompt, user_prompt=user_prompt)
            return OpenAIChat(system_prompt=system_prompt, user_prompt=user_prompt, response=response)
        except Exception as e:
            self._logger.error(f"Failed to process Page: {page.url}. Error: {e}")
            return None

    def _process_markdown(self, markdown: Markdown, system_prompt: str, user_prompt: str) -> OpenAIChat:
        """Process a Markdown object by constructing the prompt.

        Args:
            markdown: The Markdown object to process.
            system_prompt: The system prompt for the OpenAI API.
            user_prompt: The user prompt for the OpenAI API.

        Returns:
            An instance of OpenAIChat with the generated response.
        """
        try:
            user_prompt = f"{user_prompt}\n\nMarkdown content:\n{markdown.body}"
            response = self._generate_response(system_prompt=system_prompt, user_prompt=user_prompt)
            return OpenAIChat(system_prompt=system_prompt, user_prompt=user_prompt, response=response)
        except Exception as e:
            self._logger.error(f"Failed to process Markdown: {markdown.address}. Error: {e}")
            return None

    def _process_amazon_product(self, product: AmazonProduct, system_prompt: str, user_prompt: str) -> OpenAIChat:
        """Process an AmazonProduct object by constructing the prompt.

        Args:
            product: The AmazonProduct object to process.
            system_prompt: The system prompt for the OpenAI API.
            user_prompt: The user prompt for the OpenAI API.

        Returns:
            An instance of OpenAIChat with the generated response.
        """
        try:
            user_prompt = f"{user_prompt}\n\nAmazon product details:\n{product.to_dict()}"
            response = self._generate_response(system_prompt=system_prompt, user_prompt=user_prompt)
            return OpenAIChat(system_prompt=system_prompt, user_prompt=user_prompt, response=response)
        except Exception as e:
            self._logger.error(f"Failed to process AmazonProduct: {product.url}. Error: {e}")
            return None

    def _generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a response using the OpenAI API.

        Args:
            system_prompt: The system prompt for the OpenAI API.
            user_prompt: The user prompt for the OpenAI API.
            **kwargs: Additional keyword arguments for the OpenAI API.

        Returns:
            The generated response from the OpenAI API.
        """
        try:
            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            openai_parameters = self._kwargs.get("openai_parameters", {})
            # Truncate the user prompt if it exceeds the maximum context length
            max_context_length = openai_parameters.get(
                "max_context_length", 16000
            )  # Adjust this value based on the model's limit
            if len(user_prompt) > max_context_length:
                user_prompt = user_prompt[:max_context_length]

            messages = [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ]

            openai_parameters = self._kwargs.get("openai_parameters", {})
            chat_completion = client.chat.completions.create(
                model=openai_parameters.get("model", "gpt-3.5-turbo"),
                messages=messages,
                temperature=openai_parameters.get("temperature", 0.7),
                max_tokens=openai_parameters.get("max_tokens", 100),
                top_p=openai_parameters.get("top_p", 1.0),
                frequency_penalty=openai_parameters.get("frequency_penalty", 0.0),
                presence_penalty=openai_parameters.get("presence_penalty", 0.0),
            )

            message = chat_completion.choices[0].message.content.strip()
            return message

        except Exception as e:
            self._logger.error(f"Failed to generate response from OpenAI API. Error: {e}")
            return None

    def _save_data(self) -> None:
        """Save the processed data to files."""
        json_file_path = os.path.join(self._output_path, "all.json")
        data = []
        for index, item in enumerate(self._output_data):
            if item is not None and item.response is not None:
                file_name = f"payload_{index}.txt"
                file_path = os.path.join(self._output_path, file_name)
                item.save_payload(file_path, item.response)
                entry = {
                    "data_type": item.__class__.__name__,
                    "system_prompt": item.system_prompt,
                    "user_prompt": item.user_prompt,
                    "response": item.response,
                    "file_name": file_name,
                }
                data.append(entry)
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

    def _get_cache_duration(self) -> timedelta:
        return self.CACHE_DURATION

    def _get_input_type(self) -> Any:
        return Any
