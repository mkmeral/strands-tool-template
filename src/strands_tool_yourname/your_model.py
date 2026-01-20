"""
Your Model Provider Implementation

TODO: Replace this docstring with a detailed description of your model provider.

This module implements a model provider for [service/platform name], allowing
Strands Agents to use [model description] for AI inference.

Key Features:
1. Streaming responses with real-time token generation
2. Tool/function calling support
3. Configurable model parameters

Usage with Strands Agent:
```python
from strands import Agent
from strands_tool_yourname import YourModel

model = YourModel(
    api_key="your-api-key",
    model_id="your-model-id",
    temperature=0.7,
)

agent = Agent(model=model)
result = agent("Help me with a task")
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

    TODO: Replace this docstring with a detailed description.

    This implementation handles [model/service name]-specific features such as:

    - [Feature 1: e.g., API authentication]
    - [Feature 2: e.g., Streaming responses]
    - [Feature 3: e.g., Tool/function calling]

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
            max_tokens: Maximum number of tokens to generate.
            temperature: Controls randomness (0.0-1.0).
            top_p: Controls diversity via nucleus sampling.
            stop_sequences: Sequences that stop generation.
            additional_args: Additional request arguments.
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
        client_args: dict[str, Any] | None = None,
        **model_config: Unpack[YourModelConfig],
    ) -> None:
        """Initialize the model provider instance.

        Args:
            api_key: API key for authentication.
            client_args: Additional arguments for the API client.
            **model_config: Configuration options for the model.
        """
        if api_key:
            model_config["api_key"] = api_key

        self.config = YourModel.YourModelConfig(**model_config)
        self.client_args = client_args or {}

        # TODO: Initialize your API client
        # self.client = your_model_sdk.Client(api_key=api_key, **self.client_args)

        logger.debug("config=<%s> | initializing", self.config)

    @override
    def update_config(self, **model_config: Unpack[YourModelConfig]) -> None:  # type: ignore[override]
        """Update the model configuration."""
        self.config.update(model_config)

    @override
    def get_config(self) -> YourModelConfig:
        """Get the current model configuration."""
        return self.config

    def _format_request_message_content(self, content: ContentBlock) -> dict[str, Any]:
        """Format a content block for the API request.

        TODO: Implement conversion from Strands ContentBlock to your API's format.
        """
        if "text" in content:
            return {"type": "text", "text": content["text"]}

        if "image" in content:
            return {"type": "image", "source": content["image"]["source"]}

        if "toolUse" in content:
            return {
                "type": "tool_use",
                "id": content["toolUse"]["toolUseId"],
                "name": content["toolUse"]["name"],
                "input": content["toolUse"]["input"],
            }

        if "toolResult" in content:
            return {
                "type": "tool_result",
                "tool_use_id": content["toolResult"]["toolUseId"],
                "content": content["toolResult"]["content"],
            }

        raise TypeError(f"content_type=<{next(iter(content))}> | unsupported type")

    def _format_request_messages(
        self, messages: Messages, system_prompt: str | None = None
    ) -> list[dict[str, Any]]:
        """Format messages for the API request."""
        formatted_messages = []

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
        """Format tool specifications for the API request."""
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
        """Format a complete API request."""
        request: dict[str, Any] = {
            "model": self.config.get("model_id"),
            "messages": self._format_request_messages(messages, system_prompt),
            "stream": True,
        }

        if self.config.get("max_tokens"):
            request["max_tokens"] = self.config["max_tokens"]
        if self.config.get("temperature") is not None:
            request["temperature"] = self.config["temperature"]
        if self.config.get("top_p") is not None:
            request["top_p"] = self.config["top_p"]
        if self.config.get("stop_sequences"):
            request["stop"] = self.config["stop_sequences"]

        tools = self._format_tool_specs(tool_specs)
        if tools:
            request["tools"] = tools

        if self.config.get("additional_args"):
            request.update(self.config["additional_args"])

        return request

    def format_chunk(self, event: dict[str, Any]) -> StreamEvent:
        """Format API response events into Strands StreamEvents.

        TODO: Implement conversion from your API's streaming events.

        The Strands SDK expects these event types:
        - messageStart: Start of a new message
        - contentBlockStart: Start of content block (text or tool use)
        - contentBlockDelta: Incremental content
        - contentBlockStop: End of content block
        - messageStop: End of message with stop reason
        - metadata: Usage statistics
        """
        chunk_type = event.get("chunk_type")

        if chunk_type == "message_start":
            return {"messageStart": {"role": "assistant"}}

        if chunk_type == "content_start":
            if event.get("data_type") == "text":
                return {"contentBlockStart": {"start": {}}}
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
            return {"contentBlockDelta": {"delta": {"toolUse": {"input": event["data"]}}}}

        if chunk_type == "content_stop":
            return {"contentBlockStop": {}}

        if chunk_type == "message_stop":
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
            usage = event.get("data", {})
            return {
                "metadata": {
                    "usage": {
                        "inputTokens": usage.get("input_tokens", 0),
                        "outputTokens": usage.get("output_tokens", 0),
                        "totalTokens": usage.get("total_tokens", 0),
                    },
                    "metrics": {"latencyMs": usage.get("latency_ms", 0)},
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

        TODO: Implement the streaming logic for your API.

        Args:
            messages: List of message objects to be processed.
            tool_specs: List of tool specifications.
            system_prompt: System prompt for context.
            tool_choice: Tool selection strategy.
            system_prompt_content: System prompt content blocks.
            invocation_state: Caller-provided state/context.
            **kwargs: Additional arguments.

        Yields:
            Formatted message chunks from the model.
        """
        logger.debug("formatting request")
        request = self.format_request(messages, tool_specs, system_prompt)
        logger.debug("request=<%s>", request)

        logger.debug("invoking model")

        # TODO: Replace with your actual API call
        # response = await self.client.chat.completions.create(**request)
        # yield self.format_chunk({"chunk_type": "message_start"})
        # async for chunk in response:
        #     # Process chunks from your API
        #     pass

        # Placeholder implementation - remove and implement your logic
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

        TODO: Implement structured output for your API if supported.

        Args:
            output_model: Pydantic model defining output structure.
            prompt: The prompt messages.
            system_prompt: System prompt for context.
            **kwargs: Additional arguments.

        Yields:
            Model events with the last being {"output": <output_model instance>}
        """
        # TODO: Implement structured output
        raise NotImplementedError(
            "structured_output is not yet implemented for this model provider."
        )
