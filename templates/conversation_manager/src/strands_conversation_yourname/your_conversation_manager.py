"""
Your Conversation Manager Implementation

TODO: Replace this docstring with a detailed description of your conversation manager.

This module implements a conversation manager using [describe your strategy],
allowing Strands Agents to [describe what the manager enables].

Key Features:
1. [Feature 1: e.g., Intelligent message pruning]
2. [Feature 2: e.g., Context window optimization]
3. [Feature 3: e.g., Important message preservation]

Common Strategies:
- Sliding Window: Keep the N most recent messages
- Summarization: Replace old messages with summaries
- Importance-Based: Keep messages based on relevance scores
- Token-Based: Manage based on token count rather than message count
- Hybrid: Combine multiple strategies

Usage with Strands Agent:
```python
from strands import Agent
from strands_conversation_yourname import YourConversationManager

# Create conversation manager with configuration
cm = YourConversationManager(
    max_messages=50,
    preserve_system_messages=True,
)

# Attach to agent
agent = Agent(conversation_manager=cm)

# Use the agent - conversation is automatically managed
result = agent("Help me with a long conversation task")
```

Conversation Manager Lifecycle:
1. `apply_management()` - Called after each agent loop cycle
2. `reduce_context()` - Called when context window is exceeded
3. `get_state()` / `restore_from_session()` - For session persistence
"""

import logging
from typing import TYPE_CHECKING, Any

from strands.agent.conversation_manager.conversation_manager import ConversationManager
from strands.hooks.registry import HookRegistry
from strands.types.content import Message, Messages
from strands.types.exceptions import ContextWindowOverflowException

if TYPE_CHECKING:
    from strands.agent.agent import Agent

logger = logging.getLogger(__name__)


class YourConversationManager(ConversationManager):
    """Your conversation manager implementation.

    TODO: Replace this docstring with a detailed description of your strategy.

    This conversation manager implements [describe strategy] to manage
    conversation history, enabling:

    - [Capability 1: e.g., Efficient memory usage]
    - [Capability 2: e.g., Preservation of important context]
    - [Capability 3: e.g., Graceful context window handling]

    The manager is invoked at key points in the agent lifecycle:
    - After each event loop cycle via `apply_management()`
    - When context overflow occurs via `reduce_context()`

    Attributes:
        max_messages: Maximum number of messages to retain.
        preserve_important: Whether to preserve important messages.

    Example:
        ```python
        from strands import Agent
        from strands_conversation_yourname import YourConversationManager

        cm = YourConversationManager(
            max_messages=100,
            preserve_important=True,
        )
        agent = Agent(conversation_manager=cm)
        ```
    """

    def __init__(
        self,
        max_messages: int = 50,
        preserve_important: bool = True,
        # TODO: Add your configuration parameters
        **kwargs: Any,
    ) -> None:
        """Initialize the conversation manager.

        Args:
            max_messages: Maximum number of messages to keep in history.
                When exceeded, older messages will be removed/processed.
                Defaults to 50.
            preserve_important: If True, attempt to preserve messages marked
                as important even when pruning. Defaults to True.
            **kwargs: Additional keyword arguments for future extensibility.

        Example:
            ```python
            cm = YourConversationManager(
                max_messages=100,
                preserve_important=True,
            )
            ```
        """
        super().__init__()

        self.max_messages = max_messages
        self.preserve_important = preserve_important

        # TODO: Initialize any internal state for your strategy
        self._custom_state: dict[str, Any] = {}

        logger.debug(
            "max_messages=<%d>, preserve_important=<%s> | initialized conversation manager",
            max_messages,
            preserve_important,
        )

    # =========================================================================
    # Hook Registration (Optional)
    # =========================================================================

    def register_hooks(self, registry: HookRegistry, **kwargs: Any) -> None:
        """Register hooks for agent lifecycle events.

        Override this method to register callbacks for specific events.
        Always call the base implementation first.

        Args:
            registry: The hook registry to register callbacks with.
            **kwargs: Additional keyword arguments.

        Example:
            If you want to apply management before each model call:
            ```python
            def register_hooks(self, registry: HookRegistry, **kwargs: Any) -> None:
                super().register_hooks(registry, **kwargs)
                from strands.hooks.events import BeforeModelCallEvent
                registry.add_callback(BeforeModelCallEvent, self._on_before_model_call)
            ```
        """
        super().register_hooks(registry, **kwargs)

        # TODO: Register any custom hooks your strategy needs
        # Example: Apply management before each model call
        # from strands.hooks.events import BeforeModelCallEvent
        # registry.add_callback(BeforeModelCallEvent, self._on_before_model_call)

    # =========================================================================
    # Core Methods (Abstract - Must Implement)
    # =========================================================================

    def apply_management(self, agent: "Agent", **kwargs: Any) -> None:
        """Apply conversation management strategy to the agent's messages.

        This method is called after every agent event loop cycle. It should
        check if management is needed and apply your strategy to keep the
        conversation history within bounds.

        The agent's messages list should be modified in-place.

        Args:
            agent: The agent whose conversation history will be managed.
            **kwargs: Additional keyword arguments.

        Note:
            This method is called frequently, so it should be efficient.
            Consider early returns if no management is needed.

        Example implementation for sliding window:
            ```python
            def apply_management(self, agent: "Agent", **kwargs: Any) -> None:
                messages = agent.messages
                if len(messages) <= self.max_messages:
                    return  # No management needed

                # Keep only the most recent messages
                trim_count = len(messages) - self.max_messages
                self.removed_message_count += trim_count
                messages[:] = messages[trim_count:]
            ```
        """
        messages = agent.messages

        # Early return if no management needed
        if len(messages) <= self.max_messages:
            logger.debug(
                "message_count=<%d>, max_messages=<%d> | no management needed",
                len(messages),
                self.max_messages,
            )
            return

        # TODO: Implement your management strategy
        # Example: Simple sliding window

        # Calculate how many messages to remove
        excess_count = len(messages) - self.max_messages

        # Find a valid trim point (handle tool use/result pairs)
        trim_index = self._find_valid_trim_index(messages, excess_count)

        if trim_index > 0:
            # Track removed messages
            self.removed_message_count += trim_index

            # Remove old messages in-place
            messages[:] = messages[trim_index:]

            logger.info(
                "trimmed_count=<%d>, remaining=<%d> | applied conversation management",
                trim_index,
                len(messages),
            )

    def reduce_context(self, agent: "Agent", e: Exception | None = None, **kwargs: Any) -> None:
        """Reduce conversation context when overflow occurs.

        This method is called when a ContextWindowOverflowException is caught,
        indicating the model's context window has been exceeded. It should
        aggressively reduce the conversation size.

        Args:
            agent: The agent whose conversation needs reduction.
            e: The exception that triggered the reduction, if any.
            **kwargs: Additional keyword arguments.

        Raises:
            ContextWindowOverflowException: If context cannot be reduced further.
            Exception: Re-raise the original exception if provided and unhandleable.

        Note:
            This is a recovery mechanism. Be aggressive in reducing context
            but ensure you don't create invalid conversation states.
        """
        messages = agent.messages

        logger.warning(
            "message_count=<%d> | context overflow, attempting reduction",
            len(messages),
        )

        # TODO: Implement your context reduction strategy
        # This should be more aggressive than apply_management()

        # Example: Remove half of the messages
        if len(messages) <= 2:
            # Cannot reduce further
            if e:
                raise e
            raise ContextWindowOverflowException(
                "Cannot reduce context further - conversation is already minimal"
            )

        # Find a valid trim point at roughly half the messages
        target_trim = len(messages) // 2
        trim_index = self._find_valid_trim_index(messages, target_trim)

        if trim_index == 0:
            # Couldn't find a valid trim point
            if e:
                raise e
            raise ContextWindowOverflowException(
                "Unable to find valid trim point for context reduction"
            )

        # Track removed messages
        self.removed_message_count += trim_index

        # Remove messages in-place
        messages[:] = messages[trim_index:]

        logger.info(
            "trimmed_count=<%d>, remaining=<%d> | reduced context",
            trim_index,
            len(messages),
        )

    # =========================================================================
    # State Management (For Session Persistence)
    # =========================================================================

    def get_state(self) -> dict[str, Any]:
        """Get the current state of the conversation manager.

        This method is called when persisting the agent to a session.
        Return all state that should be restored when the session is resumed.

        Returns:
            Dictionary containing the manager's state, JSON-serializable.

        Note:
            Always include the base class state by calling super().get_state()
        """
        state = super().get_state()

        # TODO: Add your custom state
        state["max_messages"] = self.max_messages
        state["preserve_important"] = self.preserve_important
        state["custom_state"] = self._custom_state

        return state

    def restore_from_session(self, state: dict[str, Any]) -> list[Message] | None:
        """Restore the conversation manager's state from a session.

        This method is called when resuming an agent from a session.
        Restore all state that was saved in get_state().

        Args:
            state: Previous state dictionary from get_state().

        Returns:
            Optional list of messages to prepend to the agent's messages.
            Return None if no messages need to be prepended.

        Raises:
            ValueError: If the state is invalid or incompatible.

        Note:
            Always call super().restore_from_session() first to restore base state.
        """
        result = super().restore_from_session(state)

        # TODO: Restore your custom state
        # Note: Configuration (max_messages, etc.) is typically set during __init__,
        # so only restore mutable state that changes during operation
        self._custom_state = state.get("custom_state", {})

        return result

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _find_valid_trim_index(self, messages: Messages, target_trim: int) -> int:
        """Find a valid index to trim messages at.

        This helper ensures we don't create invalid conversation states by
        trimming in the middle of a tool use/result pair.

        Rules:
        - Cannot start with a toolResult (needs preceding toolUse)
        - Cannot end with a toolUse without following toolResult

        Args:
            messages: The messages list to analyze.
            target_trim: Target number of messages to remove from the start.

        Returns:
            The valid trim index (0 if no valid index found).
        """
        trim_index = target_trim

        while trim_index < len(messages):
            # Check if this would be a valid starting point
            if trim_index >= len(messages):
                break

            current_msg = messages[trim_index]
            current_content = current_msg.get("content", [])

            # Can't start with a toolResult
            has_tool_result = any("toolResult" in c for c in current_content)
            if has_tool_result:
                trim_index += 1
                continue

            # If current is toolUse, next must be toolResult
            has_tool_use = any("toolUse" in c for c in current_content)
            if has_tool_use:
                if trim_index + 1 < len(messages):
                    next_msg = messages[trim_index + 1]
                    next_content = next_msg.get("content", [])
                    next_has_result = any("toolResult" in c for c in next_content)
                    if not next_has_result:
                        trim_index += 1
                        continue

            # Valid trim point found
            return trim_index

        return 0  # No valid trim point found

    def _is_important_message(self, message: Message) -> bool:
        """Check if a message is marked as important.

        TODO: Implement your importance detection logic.

        Args:
            message: The message to check.

        Returns:
            True if the message should be preserved.
        """
        # Example: Check for a custom importance marker
        # This could be based on message content, metadata, etc.
        return False

    def _count_tokens(self, messages: Messages) -> int:
        """Estimate token count for messages.

        TODO: Implement token counting if your strategy is token-based.

        Args:
            messages: Messages to count tokens for.

        Returns:
            Estimated token count.
        """
        # Simple approximation: ~4 chars per token
        total_chars = 0
        for msg in messages:
            for content in msg.get("content", []):
                if "text" in content:
                    total_chars += len(content["text"])
        return total_chars // 4


# =============================================================================
# Additional Example: Token-Based Conversation Manager
# =============================================================================


class TokenBasedConversationManager(ConversationManager):
    """Example: A token-based conversation manager.

    This manager tracks token usage and prunes based on a maximum
    token limit rather than message count.

    Example:
        ```python
        from strands_conversation_yourname.your_conversation_manager import (
            TokenBasedConversationManager
        )

        cm = TokenBasedConversationManager(max_tokens=8000)
        agent = Agent(conversation_manager=cm)
        ```
    """

    def __init__(self, max_tokens: int = 8000) -> None:
        """Initialize the token-based manager.

        Args:
            max_tokens: Maximum tokens to keep in conversation history.
        """
        super().__init__()
        self.max_tokens = max_tokens
        self._current_tokens = 0

    def apply_management(self, agent: "Agent", **kwargs: Any) -> None:
        """Apply token-based management."""
        messages = agent.messages
        self._current_tokens = self._estimate_tokens(messages)

        if self._current_tokens <= self.max_tokens:
            return

        # Remove oldest messages until under token limit
        while self._current_tokens > self.max_tokens and len(messages) > 2:
            removed = messages.pop(0)
            self.removed_message_count += 1
            self._current_tokens = self._estimate_tokens(messages)

    def reduce_context(self, agent: "Agent", e: Exception | None = None, **kwargs: Any) -> None:
        """Aggressively reduce context for token-based strategy."""
        messages = agent.messages

        # Remove messages until at half capacity
        target_tokens = self.max_tokens // 2

        while self._estimate_tokens(messages) > target_tokens and len(messages) > 2:
            messages.pop(0)
            self.removed_message_count += 1

        if len(messages) <= 2 and self._estimate_tokens(messages) > self.max_tokens:
            if e:
                raise e
            raise ContextWindowOverflowException("Cannot reduce context further")

    def _estimate_tokens(self, messages: Messages) -> int:
        """Estimate total tokens in messages."""
        total = 0
        for msg in messages:
            for content in msg.get("content", []):
                if "text" in content:
                    # Rough estimation: ~4 characters per token
                    total += len(content["text"]) // 4
        return total

    def get_state(self) -> dict[str, Any]:
        """Get state for persistence."""
        state = super().get_state()
        state["current_tokens"] = self._current_tokens
        return state

    def restore_from_session(self, state: dict[str, Any]) -> list[Message] | None:
        """Restore state from session."""
        result = super().restore_from_session(state)
        self._current_tokens = state.get("current_tokens", 0)
        return result
