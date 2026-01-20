"""
Your Model Provider Implementation

TODO: Replace this docstring with a detailed description of your model provider.

This module implements a model provider for [service/platform name], allowing
Strands Agents to use [model description] for AI inference.

Key Features:
1. Streaming responses with real-time token generation
2. Tool/function calling support
3. Configurable model parameters
4. [Your specific features]

Usage with Strands Agent:
```python
from strands import Agent
from strands_model_yourname import YourModel

model = YourModel(
    api_key="your-api-key",
    model_id="your-model-id",
    temperature=0.7,
)

agent = Agent(model=model)
result = agent("Help me with a task")
```

Direct Usage:
```python
from strands_model_yourname import YourModel

model = YourModel(api_key="your-api-key", model_id="your-model-id")

# Stream responses
async for event in model.stream(messages=[{"role": "user", "content": [{"text": "Hello"}]}]):
    print(event)
```
"""

import logging
from collections.abc import AsyncGenerator
from typing import Any, TypeVar

from pydantic import BaseModel
from typing_extensions import TypedDict, Unpack, override

from strands.models.model import Model
from strands.types.content import ContentBlock, Messages, SystemContentBlock
from strands.types.streaming import StopReason, StreamEvent
from strands.types.tools import ToolChoice, ToolSpec

# TODO: Import your model's SDK/client library
# import your_model_sdk

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class YourModel(Model):
    """Your model provider implementation.

    TODO: Replace this docstring with a detailed description of your model provider.

    This implementation handles [model/service name]-specific features such as:

    - [Feature 1: e.g., API authentication]
    - [Feature 2: e.g., Streaming responses]
    - [Feature 3: e.g., Tool/function calling]

    Attributes:
        config: Configuration dictionary for the model.
        client: The underlying API client instance.

    Example:
        ```python
        model = YourModel(
            api_key="your-api-key",
            model_id="your-model-id",
            temperature=0.7,
        )
        agent = Agent(model=model)
        ```
    """

    class YourModelConfig(TypedDict, total=False):
        """Configuration parameters for your model.

        TODO: Define all configuration parameters your model supports.

        Attributes:
            api_key: API key for authentication with the service.
            model_id: The model identifier (e.g., "gpt-4", "claude-3").
            max_tokens: Maximum number of tokens to generate in the response.
            temperature: Controls randomness in generation (0.0-1.0, higher = more random).
            top_p: Controls diversity via nucleus sampling (alternative to temperature).
            stop_sequences: List of sequences that will stop generation when encountered.
            additional_args: Any additional arguments to include in the request.
        """

        api_key: str
        model_id: str
        max_tokens: int | None
        temperature: float | None
        top_p: float | None
        stop_sequences: list[str] | None
        additional_args: dict[str, Any] | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        # TODO: Add any client initialization parameters
        client_args: dict[str, Any] | None = None,
        **model_config: Unpack[YourModelConfig],
    ) -> None:
        """Initialize the model provider instance.

        Args:
            api_key: API key for authentication. Can also be set via environment variable.
            client_args: Additional arguments for the underlying API client.
            **model_config: Configuration options for the model.

        Raises:
            ValueError: If required configuration is missing.

        Example:
            ```python
            model = YourModel(
                api_key="your-api-key",
                model_id="your-model-id",
                temperature=0.7,
                max_tokens=1000,
            )
            ```
        """
        # TODO: Validate required configuration
        if api_key:
            model_config["api_key"] = api_key

        self.config = YourModel.YourModelConfig(**model_config)
        self.client_args = client_args or {}

        # TODO: Initialize your API client
        # self.client = your_model_sdk.Client(api_key=api_key, **self.client_args)

        logger.debug("config=<%s> | initializing", self.config)

    @override
    def update_config(self, **model_config: Unpack[YourModelConfig]) -> None:  # type: ignore[override]
        """Update the model configuration with the provided arguments.

        Args:
            **model_config: Configuration overrides.

        Example:
            ```python
            model.update_config(temperature=0.9, max_tokens=2000)
            ```
        """
        self.config.update(model_config)

    @override
    def get_config(self) -> YourModelConfig:
        """Get the current model configuration.

        Returns:
            The model's configuration dictionary.
        """
        return self.config

    def _format_request_message_content(self, content: ContentBlock) -> dict[str, Any]:
        """Format a content block for the API request.

        TODO: Implement conversion from Strands ContentBlock to your API's format.

        Args:
            content: A Strands content block (text, image, toolUse, toolResult, etc.).

        Returns:
            Your API's content format.

        Raises:
            TypeError: If the content block type is not supported.
        """
        if "text" in content:
            # TODO: Format text content
            return {"type": "text", "text": content["text"]}

        if "image" in content:
            # TODO: Format image content
            return {
                "type": "image",
                "source": content["image"]["source"],
            }

        if "toolUse" in content:
            # TODO: Format tool use content
            return {
                "type": "tool_use",
                "id": content["toolUse"]["toolUseId"],
                "name": content["toolUse"]["name"],
                "input": content["toolUse"]["input"],
            }

        if "toolResult" in content:
            # TODO: Format tool result content
            return {
                "type": "tool_result",
                "tool_use_id": content["toolResult"]["toolUseId"],
                "content": content["toolResult"]["content"],
            }

        raise TypeError(f"content_type=<{next(iter(content))}> | unsupported type")

    def _format_request_messages(
        self, messages: Messages, system_prompt: str | None = None
    ) -> list[dict[str, Any]]:
        """Format messages for the API request.

        TODO: Implement conversion from Strands Messages to your API's format.

        Args:
            messages: List of message objects to be processed.
            system_prompt: System prompt to provide context to the model.

        Returns:
            Your API's messages format.
        """
        formatted_messages = []

        # TODO: Handle system prompt if your API requires it in messages
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})

        for message in messages:
            formatted_content = [
                self._format_request_message_content(content)
                for content in message["content"]
            ]
            formatted_messages.append({
                "role": message["role"],
                "content": formatted_content,
            })

        return formatted_messages

    def _format_tool_specs(self, tool_specs: list[ToolSpec] | None) -> list[dict[str, Any]] | None:
        """Format tool specifications for the API request.

        TODO: Implement conversion from Strands ToolSpec to your API's format.

        Args:
            tool_specs: List of tool specifications.

        Returns:
            Your API's tool format, or None if no tools provided.
        """
        if not tool_specs:
            return None

        return [
            {
                "type": "function",
                "function": {
                    "name": spec["name"],
                    "description": spec["description"],
                    "parameters": spec["inputSchema"]["json"],
                },
            }
            for spec in tool_specs
        ]

    def format_request(
        self,
        messages: Messages,
        tool_specs: list[ToolSpec] | None = None,
        system_prompt: str | None = None,
    ) -> dict[str, Any]:
        """Format a complete API request.

        TODO: Implement the full request formatting for your API.

        Args:
            messages: List of message objects to be processed.
            tool_specs: List of tool specifications to make available.
            system_prompt: System prompt to provide context.

        Returns:
            A complete request dictionary for your API.
        """
        request = {
            "model": self.config.get("model_id"),
            "messages": self._format_request_messages(messages, system_prompt),
            "stream": True,
        }

        # Add optional parameters
        if self.config.get("max_tokens"):
            request["max_tokens"] = self.config["max_tokens"]
        if self.config.get("temperature") is not None:
            request["temperature"] = self.config["temperature"]
        if self.config.get("top_p") is not None:
            request["top_p"] = self.config["top_p"]
        if self.config.get("stop_sequences"):
            request["stop"] = self.config["stop_sequences"]

        # Add tools if provided
        tools = self._format_tool_specs(tool_specs)
        if tools:
            request["tools"] = tools

        # Add any additional arguments
        if self.config.get("additional_args"):
            request.update(self.config["additional_args"])

        return request

    def format_chunk(self, event: dict[str, Any]) -> StreamEvent:
        """Format API response events into standardized Strands StreamEvents.

        TODO: Implement conversion from your API's streaming events to Strands StreamEvent.

        The Strands SDK expects these event types:
        - messageStart: Indicates the start of a new message
        - contentBlockStart: Indicates the start of a content block (text or tool use)
        - contentBlockDelta: Contains incremental content (text chunks or tool input)
        - contentBlockStop: Indicates the end of a content block
        - messageStop: Indicates the end of a message with stop reason
        - metadata: Contains usage statistics and metrics

        Args:
            event: A response event from your API.

        Returns:
            A formatted Strands StreamEvent.

        Raises:
            RuntimeError: If the event type is not recognized.
        """
        chunk_type = event.get("chunk_type")

        if chunk_type == "message_start":
            return {"messageStart": {"role": "assistant"}}

        if chunk_type == "content_start":
            if event.get("data_type") == "text":
                return {"contentBlockStart": {"start": {}}}
            # Tool use start
            tool_name = event["data"]["name"]
            tool_id = event["data"]["id"]
            return {
                "contentBlockStart": {
                    "start": {"toolUse": {"name": tool_name, "toolUseId": tool_id}}
                }
            }

        if chunk_type == "content_delta":
            if event.get("data_type") == "text":
                return {"contentBlockDelta": {"delta": {"text": event["data"]}}}
            # Tool input delta
            return {
                "contentBlockDelta": {
                    "delta": {"toolUse": {"input": event["data"]}}
                }
            }

        if chunk_type == "content_stop":
            return {"contentBlockStop": {}}

        if chunk_type == "message_stop":
            # Map your API's stop reasons to Strands StopReason
            reason_map: dict[str, StopReason] = {
                "stop": "end_turn",
                "end_turn": "end_turn",
                "tool_use": "tool_use",
                "tool_calls": "tool_use",
                "length": "max_tokens",
                "max_tokens": "max_tokens",
            }
            reason = reason_map.get(event.get("data", ""), "end_turn")
            return {"messageStop": {"stopReason": reason}}

        if chunk_type == "metadata":
            # TODO: Extract usage from your API's response
            usage = event.get("data", {})
            return {
                "metadata": {
                    "usage": {
                        "inputTokens": usage.get("input_tokens", 0),
                        "outputTokens": usage.get("output_tokens", 0),
                        "totalTokens": usage.get("total_tokens", 0),
                    },
                    "metrics": {
                        "latencyMs": usage.get("latency_ms", 0),
                    },
                }
            }

        raise RuntimeError(f"chunk_type=<{chunk_type}> | unknown type")

    @override
    async def stream(
        self,
        messages: Messages,
        tool_specs: list[ToolSpec] | None = None,
        system_prompt: str | None = None,
        *,
        tool_choice: ToolChoice | None = None,
        system_prompt_content: list[SystemContentBlock] | None = None,
        invocation_state: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> AsyncGenerator[StreamEvent, None]:
        """Stream conversation with the model.

        This method handles the full lifecycle of conversing with the model:
        1. Format the messages, tool specs, and configuration into a streaming request
        2. Send the request to the model
        3. Yield the formatted message chunks

        TODO: Implement the streaming logic for your API.

        Args:
            messages: List of message objects to be processed by the model.
            tool_specs: List of tool specifications to make available to the model.
            system_prompt: System prompt to provide context to the model.
            tool_choice: Selection strategy for tool invocation.
            system_prompt_content: System prompt content blocks for advanced features.
            invocation_state: Caller-provided state/context that was passed to the agent.
            **kwargs: Additional keyword arguments for future extensibility.

        Yields:
            Formatted message chunks from the model.

        Raises:
            ModelThrottledException: When the model service is throttling requests.
            Exception: When the API request fails.

        Example:
            ```python
            async for event in model.stream(
                messages=[{"role": "user", "content": [{"text": "Hello"}]}],
                system_prompt="You are a helpful assistant.",
            ):
                print(event)
            ```
        """
        logger.debug("formatting request")
        request = self.format_request(messages, tool_specs, system_prompt)
        logger.debug("request=<%s>", request)

        logger.debug("invoking model")

        # TODO: Replace this with your actual API call
        # Example structure for streaming:
        #
        # response = await self.client.chat.completions.create(**request)
        #
        # yield self.format_chunk({"chunk_type": "message_start"})
        # yield self.format_chunk({"chunk_type": "content_start", "data_type": "text"})
        #
        # async for chunk in response:
        #     # Process each chunk from your API
        #     if chunk.choices[0].delta.content:
        #         yield self.format_chunk({
        #             "chunk_type": "content_delta",
        #             "data_type": "text",
        #             "data": chunk.choices[0].delta.content
        #         })
        #
        #     # Handle tool calls if present
        #     if chunk.choices[0].delta.tool_calls:
        #         for tool_call in chunk.choices[0].delta.tool_calls:
        #             yield self.format_chunk({
        #                 "chunk_type": "content_start",
        #                 "data_type": "tool",
        #                 "data": {"name": tool_call.function.name, "id": tool_call.id}
        #             })
        #             yield self.format_chunk({
        #                 "chunk_type": "content_delta",
        #                 "data_type": "tool",
        #                 "data": tool_call.function.arguments
        #             })
        #             yield self.format_chunk({"chunk_type": "content_stop"})
        #
        # yield self.format_chunk({"chunk_type": "content_stop", "data_type": "text"})
        # yield self.format_chunk({
        #     "chunk_type": "message_stop",
        #     "data": chunk.choices[0].finish_reason
        # })
        # yield self.format_chunk({
        #     "chunk_type": "metadata",
        #     "data": {"input_tokens": ..., "output_tokens": ..., "total_tokens": ...}
        # })

        # Placeholder implementation - remove this and implement your actual logic
        yield self.format_chunk({"chunk_type": "message_start"})
        yield self.format_chunk({"chunk_type": "content_start", "data_type": "text"})
        yield self.format_chunk({
            "chunk_type": "content_delta",
            "data_type": "text",
            "data": "TODO: Implement your model's streaming logic"
        })
        yield self.format_chunk({"chunk_type": "content_stop"})
        yield self.format_chunk({"chunk_type": "message_stop", "data": "end_turn"})
        yield self.format_chunk({
            "chunk_type": "metadata",
            "data": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
        })

        logger.debug("finished streaming response from model")

    @override
    async def structured_output(
        self,
        output_model: type[T],
        prompt: Messages,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> AsyncGenerator[dict[str, T | Any], None]:
        """Get structured output from the model.

        This method requests the model to generate output that conforms to a
        specific Pydantic model schema, enabling type-safe responses.

        TODO: Implement structured output for your API if it supports it.
        Many APIs support JSON mode or function calling that can be used for this.

        Args:
            output_model: The Pydantic model class defining the output structure.
            prompt: The prompt messages to use for the agent.
            system_prompt: System prompt to provide context to the model.
            **kwargs: Additional keyword arguments for future extensibility.

        Yields:
            Model events with the last being the structured output in format:
            {"output": <instance of output_model>}

        Raises:
            ValidationException: If the response doesn't match the output_model schema.
            ValueError: If the response cannot be parsed as valid JSON.

        Example:
            ```python
            from pydantic import BaseModel

            class WeatherResponse(BaseModel):
                temperature: float
                conditions: str
                humidity: int

            async for event in model.structured_output(
                output_model=WeatherResponse,
                prompt=[{"role": "user", "content": [{"text": "What's the weather?"}]}],
            ):
                if "output" in event:
                    weather = event["output"]  # WeatherResponse instance
                    print(f"Temperature: {weather.temperature}")
            ```
        """
        # TODO: Implement structured output for your API
        # Common approaches:
        # 1. Use JSON mode if your API supports it
        # 2. Use function calling/tool use to enforce schema
        # 3. Request JSON output and parse/validate with the output_model

        # Example implementation using JSON schema:
        #
        # request = self.format_request(messages=prompt, system_prompt=system_prompt)
        # request["response_format"] = {
        #     "type": "json_schema",
        #     "json_schema": output_model.model_json_schema()
        # }
        # request["stream"] = False
        #
        # response = await self.client.chat.completions.create(**request)
        # content = response.choices[0].message.content
        #
        # try:
        #     yield {"output": output_model.model_validate_json(content)}
        # except Exception as e:
        #     raise ValueError(f"Failed to parse response into model: {e}") from e

        # Placeholder - remove and implement your logic
        raise NotImplementedError(
            "structured_output is not yet implemented for this model provider. "
            "TODO: Implement structured output support."
        )
