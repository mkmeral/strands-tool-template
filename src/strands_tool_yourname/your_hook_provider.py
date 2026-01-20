"""
Your Hook Provider Implementation

TODO: Replace this docstring with a detailed description of your hook provider.

This module implements hook providers for extending Strands Agent functionality.

Available Hook Events:
- AgentInitializedEvent: Triggered when agent is fully initialized
- BeforeInvocationEvent: Triggered before processing a request
- AfterInvocationEvent: Triggered after processing completes
- MessageAddedEvent: Triggered when a message is added to history
- BeforeToolCallEvent: Triggered before a tool is executed
- AfterToolCallEvent: Triggered after a tool execution completes
- BeforeModelCallEvent: Triggered before calling the model
- AfterModelCallEvent: Triggered after model call completes

Usage with Strands Agent:
```python
from strands import Agent
from strands_tool_yourname import YourHookProvider

hooks = YourHookProvider(config_option="value")
agent = Agent(hooks=[hooks])
result = agent("Help me with a task")
```
"""

import logging
from typing import Any

from strands.hooks.registry import HookProvider, HookRegistry
from strands.hooks.events import (
    AgentInitializedEvent,
    BeforeInvocationEvent,
    AfterInvocationEvent,
    MessageAddedEvent,
    BeforeToolCallEvent,
    AfterToolCallEvent,
    BeforeModelCallEvent,
    AfterModelCallEvent,
)

logger = logging.getLogger(__name__)


class YourHookProvider(HookProvider):
    """Your hook provider implementation.

    TODO: Replace this docstring with a detailed description.

    This hook provider implements [describe purpose], enabling:

    - [Capability 1: e.g., Logging of agent interactions]
    - [Capability 2: e.g., Performance monitoring]
    - [Capability 3: e.g., Custom validation]

    Example:
        ```python
        hooks = YourHookProvider(config_option="value", enable_feature=True)
        agent = Agent(hooks=[hooks])
        ```
    """

    def __init__(
        self,
        *,
        config_option: str | None = None,
        enable_feature: bool = True,
    ) -> None:
        """Initialize the hook provider.

        Args:
            config_option: Description of this configuration option.
            enable_feature: Whether to enable a specific feature.
        """
        self.config_option = config_option
        self.enable_feature = enable_feature
        self._request_count = 0
        self._total_tokens = 0

        logger.debug(
            "config_option=<%s>, enable_feature=<%s> | initialized",
            config_option, enable_feature,
        )

    def register_hooks(self, registry: HookRegistry, **kwargs: Any) -> None:
        """Register callback functions for agent lifecycle events.

        Args:
            registry: The hook registry to register callbacks with.
            **kwargs: Additional keyword arguments.
        """
        # TODO: Uncomment the callbacks you need
        registry.add_callback(AgentInitializedEvent, self._on_agent_initialized)
        registry.add_callback(BeforeInvocationEvent, self._on_before_invocation)
        registry.add_callback(AfterInvocationEvent, self._on_after_invocation)
        registry.add_callback(MessageAddedEvent, self._on_message_added)
        registry.add_callback(BeforeToolCallEvent, self._on_before_tool_call)
        registry.add_callback(AfterToolCallEvent, self._on_after_tool_call)
        registry.add_callback(BeforeModelCallEvent, self._on_before_model_call)
        registry.add_callback(AfterModelCallEvent, self._on_after_model_call)

        logger.debug("registered hook callbacks")

    def _on_agent_initialized(self, event: AgentInitializedEvent) -> None:
        """Handle agent initialization completion.

        NOTE: This callback must be synchronous (not async).

        Args:
            event: The initialization event containing the agent instance.
        """
        # TODO: Implement your initialization logic
        logger.info("agent_id=<%s> | agent initialized", id(event.agent))

    def _on_before_invocation(self, event: BeforeInvocationEvent) -> None:
        """Handle the start of an agent invocation.

        The `messages` attribute can be modified to redact or transform content.

        Args:
            event: The event containing the agent and input messages.
        """
        self._request_count += 1
        logger.debug("request_count=<%d> | starting invocation", self._request_count)

        # Example: Modify messages
        # if event.messages:
        #     for msg in event.messages:
        #         pass  # Transform content

    def _on_after_invocation(self, event: AfterInvocationEvent) -> None:
        """Handle the completion of an agent invocation.

        NOTE: Callbacks are invoked in reverse registration order.

        Args:
            event: The event containing the agent and result.
        """
        logger.debug("request_count=<%d> | completed invocation", self._request_count)

    def _on_message_added(self, event: MessageAddedEvent) -> None:
        """Handle a message being added to conversation history.

        Args:
            event: The event containing the agent and added message.
        """
        role = event.message.get("role", "unknown")
        logger.debug("role=<%s> | message added", role)

    def _on_before_tool_call(self, event: BeforeToolCallEvent) -> None:
        """Handle the start of a tool execution.

        Set `cancel_tool` to True or a message string to cancel the tool call.

        Args:
            event: The event containing tool execution details.
        """
        tool_name = event.tool_use.get("name", "unknown")
        logger.debug("tool=<%s> | before tool call", tool_name)

        # Example: Cancel specific tools
        # if tool_name == "dangerous_tool":
        #     event.cancel_tool = "This tool is not allowed"

    def _on_after_tool_call(self, event: AfterToolCallEvent) -> None:
        """Handle the completion of a tool execution.

        NOTE: Callbacks are invoked in reverse registration order.

        Args:
            event: The event containing tool execution results.
        """
        tool_name = event.tool_use.get("name", "unknown")
        status = event.result.get("status", "unknown")
        logger.debug("tool=<%s>, status=<%s> | after tool call", tool_name, status)

    def _on_before_model_call(self, event: BeforeModelCallEvent) -> None:
        """Handle the start of a model inference call.

        Args:
            event: The event containing the agent instance.
        """
        logger.debug("before model call")

    def _on_after_model_call(self, event: AfterModelCallEvent) -> None:
        """Handle the completion of a model inference call.

        Set `retry` to True to discard the response and retry.

        NOTE: Callbacks are invoked in reverse registration order.

        Args:
            event: The event containing model call results.
        """
        if event.stop_response:
            logger.debug("stop_reason=<%s> | after model call", event.stop_response.stop_reason)
        elif event.exception:
            logger.error("exception=<%s> | model call failed", event.exception)
            # Example: Retry on specific errors
            # if "rate_limit" in str(event.exception).lower():
            #     event.retry = True

    def get_metrics(self) -> dict[str, Any]:
        """Get collected metrics from this hook provider."""
        return {
            "request_count": self._request_count,
            "total_tokens": self._total_tokens,
        }

    def reset_metrics(self) -> None:
        """Reset all collected metrics."""
        self._request_count = 0
        self._total_tokens = 0
