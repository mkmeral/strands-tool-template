"""
Your Hook Provider Implementation

TODO: Replace this docstring with a detailed description of your hook provider.

This module implements hook providers for [describe functionality], allowing
Strands Agents to [describe what the hooks enable].

Key Features:
1. [Feature 1: e.g., Logging all agent interactions]
2. [Feature 2: e.g., Rate limiting model calls]
3. [Feature 3: e.g., Custom metrics collection]

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
from strands_hooks_yourname import YourHookProvider

# Create hook provider with configuration
hooks = YourHookProvider(
    log_level="debug",
    enable_metrics=True,
)

# Attach to agent
agent = Agent(hooks=[hooks])

# Use the agent - hooks will be triggered automatically
result = agent("Help me with a task")
```

Using Multiple Hook Providers:
```python
from strands import Agent
from strands_hooks_yourname import YourHookProvider, AnotherHookProvider

agent = Agent(hooks=[
    YourHookProvider(option="value"),
    AnotherHookProvider(),
])
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

    TODO: Replace this docstring with a detailed description of your hook provider.

    This hook provider implements [describe purpose], enabling:

    - [Capability 1: e.g., Comprehensive logging of agent interactions]
    - [Capability 2: e.g., Performance monitoring and metrics]
    - [Capability 3: e.g., Custom validation or transformation]

    The provider registers callbacks for various agent lifecycle events and
    executes custom logic at each stage.

    Attributes:
        config_option: Description of configuration option.
        enable_feature: Whether to enable a specific feature.

    Example:
        ```python
        from strands import Agent
        from strands_hooks_yourname import YourHookProvider

        hooks = YourHookProvider(
            config_option="value",
            enable_feature=True,
        )
        agent = Agent(hooks=[hooks])
        ```
    """

    def __init__(
        self,
        *,
        config_option: str | None = None,
        enable_feature: bool = True,
        # TODO: Add your configuration parameters
    ) -> None:
        """Initialize the hook provider.

        Args:
            config_option: Description of this configuration option.
            enable_feature: Whether to enable a specific feature. Defaults to True.

        Example:
            ```python
            hooks = YourHookProvider(
                config_option="custom_value",
                enable_feature=True,
            )
            ```
        """
        self.config_option = config_option
        self.enable_feature = enable_feature

        # TODO: Initialize any internal state
        self._request_count = 0
        self._total_tokens = 0

        logger.debug(
            "config_option=<%s>, enable_feature=<%s> | initialized hook provider",
            config_option,
            enable_feature,
        )

    def register_hooks(self, registry: HookRegistry, **kwargs: Any) -> None:
        """Register callback functions for agent lifecycle events.

        This method is called by the Strands Agent during initialization to
        register all hook callbacks. Each callback will be invoked when its
        corresponding event occurs during agent execution.

        Args:
            registry: The hook registry to register callbacks with.
            **kwargs: Additional keyword arguments for future extensibility.

        Note:
            Callbacks can be either synchronous or asynchronous (async def).
            However, AgentInitializedEvent only supports synchronous callbacks.
        """
        # Register callbacks for events you want to handle
        # TODO: Uncomment and customize the callbacks you need

        # Called after agent is fully initialized
        registry.add_callback(AgentInitializedEvent, self._on_agent_initialized)

        # Called at the start of each agent invocation
        registry.add_callback(BeforeInvocationEvent, self._on_before_invocation)

        # Called at the end of each agent invocation
        registry.add_callback(AfterInvocationEvent, self._on_after_invocation)

        # Called when a message is added to conversation history
        registry.add_callback(MessageAddedEvent, self._on_message_added)

        # Called before a tool is executed
        registry.add_callback(BeforeToolCallEvent, self._on_before_tool_call)

        # Called after a tool execution completes
        registry.add_callback(AfterToolCallEvent, self._on_after_tool_call)

        # Called before calling the model
        registry.add_callback(BeforeModelCallEvent, self._on_before_model_call)

        # Called after model call completes
        registry.add_callback(AfterModelCallEvent, self._on_after_model_call)

        logger.debug("registered hook callbacks")

    # =========================================================================
    # Agent Lifecycle Hooks
    # =========================================================================

    def _on_agent_initialized(self, event: AgentInitializedEvent) -> None:
        """Handle agent initialization completion.

        This callback is invoked after the agent has been fully constructed
        and all built-in components have been initialized.

        NOTE: This callback must be synchronous (not async).

        Args:
            event: The initialization event containing the agent instance.

        Use cases:
            - Perform additional setup that requires a fully initialized agent
            - Log agent configuration
            - Initialize connections to external services
        """
        # TODO: Implement your initialization logic
        logger.info("agent_id=<%s> | agent initialized", id(event.agent))

        # Example: Access agent properties
        # system_prompt = event.agent.system_prompt
        # tools = event.agent.tool_registry.get_all_tools()

    def _on_before_invocation(self, event: BeforeInvocationEvent) -> None:
        """Handle the start of an agent invocation.

        This callback is invoked before the agent begins processing a request,
        before any model inference or tool execution occurs.

        The `messages` attribute can be modified to redact or transform content.

        Args:
            event: The event containing the agent and input messages.
                - event.agent: The agent instance
                - event.messages: Input messages (can be modified)

        Use cases:
            - Log incoming requests
            - Validate or sanitize input
            - Start timing/metrics collection
            - Implement rate limiting
        """
        self._request_count += 1

        # TODO: Implement your pre-invocation logic
        logger.debug(
            "request_count=<%d> | starting invocation",
            self._request_count,
        )

        # Example: Modify messages (e.g., redact sensitive content)
        # if event.messages:
        #     for msg in event.messages:
        #         # Transform message content
        #         pass

    def _on_after_invocation(self, event: AfterInvocationEvent) -> None:
        """Handle the completion of an agent invocation.

        This callback is invoked after the agent has completed processing,
        regardless of success or failure.

        NOTE: Callbacks for this event are invoked in reverse registration order.

        Args:
            event: The event containing the agent and result.
                - event.agent: The agent instance
                - event.result: The AgentResult (may be None for structured_output)

        Use cases:
            - Log completion and results
            - Record metrics and timing
            - Clean up resources
            - Persist conversation state
        """
        # TODO: Implement your post-invocation logic
        logger.debug(
            "request_count=<%d> | completed invocation",
            self._request_count,
        )

        # Example: Access result data
        # if event.result:
        #     logger.info("stop_reason=<%s>", event.result.stop_reason)

    # =========================================================================
    # Message Hooks
    # =========================================================================

    def _on_message_added(self, event: MessageAddedEvent) -> None:
        """Handle a message being added to conversation history.

        This callback is invoked whenever a new message is added to the agent's
        internal message history, including user messages, assistant responses,
        and tool results.

        Args:
            event: The event containing the agent and added message.
                - event.agent: The agent instance
                - event.message: The message that was added

        Use cases:
            - Log conversation history
            - Persist messages to external storage
            - Analyze message content
            - Track conversation metrics
        """
        # TODO: Implement your message handling logic
        message = event.message
        role = message.get("role", "unknown")

        logger.debug("role=<%s> | message added to history", role)

        # Example: Count tokens or analyze content
        # for content in message.get("content", []):
        #     if "text" in content:
        #         text_length = len(content["text"])

    # =========================================================================
    # Tool Hooks
    # =========================================================================

    def _on_before_tool_call(self, event: BeforeToolCallEvent) -> None:
        """Handle the start of a tool execution.

        This callback is invoked just before a tool is executed, allowing
        inspection, modification, or cancellation of the tool call.

        The `selected_tool` and `tool_use` attributes can be modified.
        Set `cancel_tool` to True or a message string to cancel the tool call.

        Args:
            event: The event containing tool execution details.
                - event.agent: The agent instance
                - event.selected_tool: The tool to be invoked (can be modified)
                - event.tool_use: Tool parameters (can be modified)
                - event.invocation_state: State passed to the tool
                - event.cancel_tool: Set to True/string to cancel

        Use cases:
            - Log tool invocations
            - Validate tool inputs
            - Implement tool-level permissions
            - Replace or modify tools dynamically
        """
        tool_name = event.tool_use.get("name", "unknown")

        # TODO: Implement your pre-tool logic
        logger.debug("tool=<%s> | before tool call", tool_name)

        # Example: Cancel specific tools
        # if tool_name == "dangerous_tool":
        #     event.cancel_tool = "This tool is not allowed"

        # Example: Modify tool input
        # event.tool_use["input"]["additional_param"] = "value"

    def _on_after_tool_call(self, event: AfterToolCallEvent) -> None:
        """Handle the completion of a tool execution.

        This callback is invoked after a tool has finished executing,
        regardless of success or failure.

        The `result` attribute can be modified to transform the tool output.

        NOTE: Callbacks for this event are invoked in reverse registration order.

        Args:
            event: The event containing tool execution results.
                - event.agent: The agent instance
                - event.selected_tool: The tool that was invoked
                - event.tool_use: Tool parameters that were used
                - event.invocation_state: State that was passed to the tool
                - event.result: The tool result (can be modified)
                - event.exception: Exception if tool failed
                - event.cancel_message: Cancellation message if cancelled

        Use cases:
            - Log tool results
            - Record tool execution metrics
            - Transform or filter tool output
            - Handle tool errors
        """
        tool_name = event.tool_use.get("name", "unknown")
        status = event.result.get("status", "unknown")

        # TODO: Implement your post-tool logic
        logger.debug(
            "tool=<%s>, status=<%s> | after tool call",
            tool_name,
            status,
        )

        # Example: Transform tool result
        # if "content" in event.result:
        #     # Modify the result content
        #     pass

    # =========================================================================
    # Model Hooks
    # =========================================================================

    def _on_before_model_call(self, event: BeforeModelCallEvent) -> None:
        """Handle the start of a model inference call.

        This callback is invoked just before the agent calls the model,
        allowing inspection of the request.

        NOTE: This event is not fired for structured_output calls.

        Args:
            event: The event containing the agent instance.
                - event.agent: The agent instance

        Use cases:
            - Log model requests
            - Implement rate limiting
            - Track model call frequency
            - Start latency timing
        """
        # TODO: Implement your pre-model logic
        logger.debug("before model call")

        # Example: Access messages being sent to model
        # messages = event.agent.messages

    def _on_after_model_call(self, event: AfterModelCallEvent) -> None:
        """Handle the completion of a model inference call.

        This callback is invoked after the model has finished generating,
        regardless of success or failure.

        Set `retry` to True to discard the response and retry the model call.

        NOTE: Callbacks for this event are invoked in reverse registration order.
        NOTE: This event is not fired for structured_output calls.

        Args:
            event: The event containing model call results.
                - event.agent: The agent instance
                - event.stop_response: Model response data (if successful)
                    - stop_response.message: The generated message
                    - stop_response.stop_reason: Why generation stopped
                - event.exception: Exception if model call failed
                - event.retry: Set to True to retry the model call

        Use cases:
            - Log model responses
            - Record token usage metrics
            - Implement response validation
            - Handle model errors
            - Retry on specific conditions
        """
        # TODO: Implement your post-model logic
        if event.stop_response:
            stop_reason = event.stop_response.stop_reason
            logger.debug("stop_reason=<%s> | after model call", stop_reason)

            # Example: Track token usage from message metadata
            # message = event.stop_response.message
            # usage = message.get("usage", {})
            # self._total_tokens += usage.get("total_tokens", 0)

        elif event.exception:
            logger.error("exception=<%s> | model call failed", event.exception)

            # Example: Retry on specific errors
            # if "rate_limit" in str(event.exception).lower():
            #     event.retry = True

    # =========================================================================
    # Utility Methods
    # =========================================================================

    def get_metrics(self) -> dict[str, Any]:
        """Get collected metrics from this hook provider.

        Returns:
            Dictionary containing collected metrics.

        Example:
            ```python
            hooks = YourHookProvider()
            agent = Agent(hooks=[hooks])
            agent("Hello")

            metrics = hooks.get_metrics()
            print(f"Total requests: {metrics['request_count']}")
            ```
        """
        return {
            "request_count": self._request_count,
            "total_tokens": self._total_tokens,
        }

    def reset_metrics(self) -> None:
        """Reset all collected metrics to initial values."""
        self._request_count = 0
        self._total_tokens = 0
        logger.debug("metrics reset")


# =============================================================================
# Additional Hook Provider Example
# =============================================================================


class LoggingHookProvider(HookProvider):
    """A simple logging hook provider example.

    This hook provider logs all agent lifecycle events for debugging
    and monitoring purposes.

    Example:
        ```python
        from strands import Agent
        from strands_hooks_yourname import LoggingHookProvider

        agent = Agent(hooks=[LoggingHookProvider(level="INFO")])
        ```
    """

    def __init__(self, level: str = "DEBUG") -> None:
        """Initialize the logging hook provider.

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR).
        """
        self.level = getattr(logging, level.upper(), logging.DEBUG)
        self._logger = logging.getLogger(f"{__name__}.LoggingHookProvider")

    def register_hooks(self, registry: HookRegistry, **kwargs: Any) -> None:
        """Register logging callbacks for all events."""
        registry.add_callback(AgentInitializedEvent, self._log_event)
        registry.add_callback(BeforeInvocationEvent, self._log_event)
        registry.add_callback(AfterInvocationEvent, self._log_event)
        registry.add_callback(MessageAddedEvent, self._log_event)
        registry.add_callback(BeforeToolCallEvent, self._log_event)
        registry.add_callback(AfterToolCallEvent, self._log_event)
        registry.add_callback(BeforeModelCallEvent, self._log_event)
        registry.add_callback(AfterModelCallEvent, self._log_event)

    def _log_event(self, event: Any) -> None:
        """Log any event."""
        event_type = type(event).__name__
        self._logger.log(self.level, "event=<%s>", event_type)
