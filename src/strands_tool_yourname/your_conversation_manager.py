"""
Your Conversation Manager Implementation

TODO: Replace this docstring with a detailed description.

This module implements a conversation manager for managing agent conversation
history using [describe your strategy].

Common Strategies:
- Sliding Window: Keep the N most recent messages
- Summarization: Replace old messages with summaries
- Importance-Based: Keep messages based on relevance
- Token-Based: Manage based on token count

Usage with Strands Agent:
```python
from strands import Agent
from strands_tool_yourname import YourConversationManager

cm = YourConversationManager(max_messages=50, preserve_important=True)
agent = Agent(conversation_manager=cm)
result = agent("Help me with a long conversation task")
```
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

    TODO: Replace this docstring with a detailed description.

    This conversation manager implements [describe strategy] to manage
    conversation history, enabling:

    - [Capability 1: e.g., Efficient memory usage]
    - [Capability 2: e.g., Preservation of important context]
    - [Capability 3: e.g., Graceful context window handling]

    Example:
        ```python
        cm = YourConversationManager(max_messages=100, preserve_important=True)
        agent = Agent(conversation_manager=cm)
        ```
    """

    def __init__(
        self,
        max_messages: int = 50,
        preserve_important: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize the conversation manager.

        Args:
            max_messages: Maximum number of messages to keep.
            preserve_important: Preserve important messages when pruning.
            **kwargs: Additional keyword arguments.
        """
        super().__init__()

        self.max_messages = max_messages
        self.preserve_important = preserve_important
        self._custom_state: dict[str, Any] = {}

        logger.debug(
            "max_messages=<%d>, preserve_important=<%s> | initialized",
            max_messages, preserve_important,
        )

    def register_hooks(self, registry: HookRegistry, **kwargs: Any) -> None:
        """Register hooks for agent lifecycle events.

        Override to register callbacks for specific events.

        Args:
            registry: The hook registry.
            **kwargs: Additional keyword arguments.
        """
        super().register_hooks(registry, **kwargs)
        # TODO: Register custom hooks if needed
        # from strands.hooks.events import BeforeModelCallEvent
        # registry.add_callback(BeforeModelCallEvent, self._on_before_model_call)

    def apply_management(self, agent: "Agent", **kwargs: Any) -> None:
        """Apply conversation management strategy.

        Called after every agent event loop cycle. Check if management is
        needed and apply your strategy to keep history within bounds.

        Args:
            agent: The agent whose conversation will be managed.
            **kwargs: Additional keyword arguments.
        """
        messages = agent.messages

        if len(messages) <= self.max_messages:
            logger.debug(
                "message_count=<%d>, max_messages=<%d> | no management needed",
                len(messages), self.max_messages,
            )
            return

        # Calculate how many messages to remove
        excess_count = len(messages) - self.max_messages

        # Find a valid trim point (handle tool use/result pairs)
        trim_index = self._find_valid_trim_index(messages, excess_count)

        if trim_index > 0:
            self.removed_message_count += trim_index
            messages[:] = messages[trim_index:]

            logger.info(
                "trimmed_count=<%d>, remaining=<%d> | applied management",
                trim_index, len(messages),
            )

    def reduce_context(self, agent: "Agent", e: Exception | None = None, **kwargs: Any) -> None:
        """Reduce conversation context when overflow occurs.

        Called when ContextWindowOverflowException is caught. Should
        aggressively reduce the conversation size.

        Args:
            agent: The agent whose conversation needs reduction.
            e: The exception that triggered the reduction.
            **kwargs: Additional keyword arguments.

        Raises:
            ContextWindowOverflowException: If context cannot be reduced.
        """
        messages = agent.messages

        logger.warning(
            "message_count=<%d> | context overflow, reducing",
            len(messages),
        )

        if len(messages) <= 2:
            if e:
                raise e
            raise ContextWindowOverflowException(
                "Cannot reduce context further - conversation is minimal"
            )

        # Remove roughly half the messages
        target_trim = len(messages) // 2
        trim_index = self._find_valid_trim_index(messages, target_trim)

        if trim_index == 0:
            if e:
                raise e
            raise ContextWindowOverflowException(
                "Unable to find valid trim point for context reduction"
            )

        self.removed_message_count += trim_index
        messages[:] = messages[trim_index:]

        logger.info(
            "trimmed_count=<%d>, remaining=<%d> | reduced context",
            trim_index, len(messages),
        )

    def get_state(self) -> dict[str, Any]:
        """Get the current state for session persistence.

        Returns:
            Dictionary containing the manager's state.
        """
        state = super().get_state()
        state["max_messages"] = self.max_messages
        state["preserve_important"] = self.preserve_important
        state["custom_state"] = self._custom_state
        return state

    def restore_from_session(self, state: dict[str, Any]) -> list[Message] | None:
        """Restore state from a session.

        Args:
            state: Previous state dictionary.

        Returns:
            Optional list of messages to prepend.
        """
        result = super().restore_from_session(state)
        self._custom_state = state.get("custom_state", {})
        return result

    def _find_valid_trim_index(self, messages: Messages, target_trim: int) -> int:
        """Find a valid index to trim messages at.

        Ensures we don't create invalid states by trimming in the middle
        of a tool use/result pair.

        Args:
            messages: The messages list.
            target_trim: Target number of messages to remove.

        Returns:
            The valid trim index (0 if none found).
        """
        trim_index = target_trim

        while trim_index < len(messages):
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
            if has_tool_use and trim_index + 1 < len(messages):
                next_msg = messages[trim_index + 1]
                next_content = next_msg.get("content", [])
                next_has_result = any("toolResult" in c for c in next_content)
                if not next_has_result:
                    trim_index += 1
                    continue

            return trim_index

        return 0
