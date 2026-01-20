"""
Tests for YourConversationManager

TODO: Add comprehensive tests for your conversation manager.
"""

import pytest
from unittest.mock import MagicMock

from strands_conversation_yourname import YourConversationManager
from strands_conversation_yourname.your_conversation_manager import TokenBasedConversationManager
from strands.types.exceptions import ContextWindowOverflowException


class TestYourConversationManagerInit:
    """Tests for YourConversationManager initialization."""

    def test_init_default(self):
        """Test default initialization."""
        cm = YourConversationManager()

        assert cm.max_messages == 50
        assert cm.preserve_important is True
        assert cm.removed_message_count == 0

    def test_init_with_config(self):
        """Test initialization with configuration."""
        cm = YourConversationManager(
            max_messages=100,
            preserve_important=False,
        )

        assert cm.max_messages == 100
        assert cm.preserve_important is False


class TestYourConversationManagerApplyManagement:
    """Tests for apply_management method."""

    def test_no_management_needed(self):
        """Test when message count is under limit."""
        cm = YourConversationManager(max_messages=10)
        mock_agent = MagicMock()
        mock_agent.messages = [
            {"role": "user", "content": [{"text": "Hello"}]},
            {"role": "assistant", "content": [{"text": "Hi!"}]},
        ]

        cm.apply_management(mock_agent)

        assert len(mock_agent.messages) == 2
        assert cm.removed_message_count == 0

    def test_management_trims_messages(self):
        """Test that excess messages are trimmed."""
        cm = YourConversationManager(max_messages=3)
        mock_agent = MagicMock()
        mock_agent.messages = [
            {"role": "user", "content": [{"text": f"Message {i}"}]}
            for i in range(5)
        ]

        cm.apply_management(mock_agent)

        assert len(mock_agent.messages) <= 3
        assert cm.removed_message_count > 0

    def test_preserves_tool_use_pairs(self):
        """Test that tool use/result pairs are preserved together."""
        cm = YourConversationManager(max_messages=3)
        mock_agent = MagicMock()
        mock_agent.messages = [
            {"role": "user", "content": [{"text": "Start"}]},
            {"role": "assistant", "content": [{"toolUse": {"toolUseId": "1", "name": "test", "input": {}}}]},
            {"role": "user", "content": [{"toolResult": {"toolUseId": "1", "content": [{"text": "result"}]}}]},
            {"role": "assistant", "content": [{"text": "Done"}]},
            {"role": "user", "content": [{"text": "Next"}]},
        ]

        cm.apply_management(mock_agent)

        # Verify no orphaned toolResult at the start
        first_msg = mock_agent.messages[0]
        has_orphaned_result = any("toolResult" in c for c in first_msg.get("content", []))
        assert not has_orphaned_result


class TestYourConversationManagerReduceContext:
    """Tests for reduce_context method."""

    def test_reduce_context_removes_messages(self):
        """Test that reduce_context removes messages."""
        cm = YourConversationManager(max_messages=100)
        mock_agent = MagicMock()
        mock_agent.messages = [
            {"role": "user", "content": [{"text": f"Message {i}"}]}
            for i in range(10)
        ]

        original_count = len(mock_agent.messages)
        cm.reduce_context(mock_agent)

        assert len(mock_agent.messages) < original_count
        assert cm.removed_message_count > 0

    def test_reduce_context_raises_on_minimal_conversation(self):
        """Test that reduce_context raises when conversation cannot be reduced."""
        cm = YourConversationManager()
        mock_agent = MagicMock()
        mock_agent.messages = [
            {"role": "user", "content": [{"text": "Hello"}]},
        ]

        with pytest.raises(ContextWindowOverflowException):
            cm.reduce_context(mock_agent)

    def test_reduce_context_reraises_exception(self):
        """Test that original exception is re-raised when cannot reduce."""
        cm = YourConversationManager()
        mock_agent = MagicMock()
        mock_agent.messages = [
            {"role": "user", "content": [{"text": "Hello"}]},
        ]
        original_exception = Exception("Original error")

        with pytest.raises(Exception) as exc_info:
            cm.reduce_context(mock_agent, e=original_exception)

        assert exc_info.value is original_exception


class TestYourConversationManagerState:
    """Tests for state management."""

    def test_get_state(self):
        """Test getting state for persistence."""
        cm = YourConversationManager(max_messages=75, preserve_important=False)
        cm.removed_message_count = 10

        state = cm.get_state()

        assert state["__name__"] == "YourConversationManager"
        assert state["removed_message_count"] == 10
        assert state["max_messages"] == 75
        assert state["preserve_important"] is False

    def test_restore_from_session(self):
        """Test restoring state from session."""
        cm = YourConversationManager()
        state = {
            "__name__": "YourConversationManager",
            "removed_message_count": 5,
            "max_messages": 100,
            "preserve_important": True,
            "custom_state": {"key": "value"},
        }

        result = cm.restore_from_session(state)

        assert cm.removed_message_count == 5
        assert result is None  # No messages to prepend

    def test_restore_from_session_invalid_name(self):
        """Test that invalid state name raises error."""
        cm = YourConversationManager()
        state = {
            "__name__": "WrongManager",
            "removed_message_count": 0,
        }

        with pytest.raises(ValueError):
            cm.restore_from_session(state)


class TestYourConversationManagerHelpers:
    """Tests for helper methods."""

    def test_find_valid_trim_index_basic(self):
        """Test finding valid trim index with simple messages."""
        cm = YourConversationManager()
        messages = [
            {"role": "user", "content": [{"text": "1"}]},
            {"role": "assistant", "content": [{"text": "2"}]},
            {"role": "user", "content": [{"text": "3"}]},
            {"role": "assistant", "content": [{"text": "4"}]},
        ]

        index = cm._find_valid_trim_index(messages, 2)

        assert index == 2

    def test_find_valid_trim_index_skips_tool_result(self):
        """Test that trim index skips orphaned tool results."""
        cm = YourConversationManager()
        messages = [
            {"role": "user", "content": [{"text": "1"}]},
            {"role": "assistant", "content": [{"toolUse": {"toolUseId": "1", "name": "test", "input": {}}}]},
            {"role": "user", "content": [{"toolResult": {"toolUseId": "1", "content": []}}]},
            {"role": "assistant", "content": [{"text": "Done"}]},
        ]

        # Trying to trim at index 2 (toolResult) should skip ahead
        index = cm._find_valid_trim_index(messages, 2)

        assert index == 3  # Should skip the toolResult


class TestTokenBasedConversationManager:
    """Tests for TokenBasedConversationManager example."""

    def test_init(self):
        """Test initialization."""
        cm = TokenBasedConversationManager(max_tokens=4000)
        assert cm.max_tokens == 4000

    def test_apply_management_under_limit(self):
        """Test no management when under token limit."""
        cm = TokenBasedConversationManager(max_tokens=10000)
        mock_agent = MagicMock()
        mock_agent.messages = [
            {"role": "user", "content": [{"text": "Hello"}]},
        ]

        cm.apply_management(mock_agent)

        assert len(mock_agent.messages) == 1

    def test_apply_management_over_limit(self):
        """Test management when over token limit."""
        cm = TokenBasedConversationManager(max_tokens=100)
        mock_agent = MagicMock()
        # Create messages with lots of text
        mock_agent.messages = [
            {"role": "user", "content": [{"text": "x" * 200}]}
            for _ in range(5)
        ]

        cm.apply_management(mock_agent)

        # Should have removed some messages
        assert cm.removed_message_count > 0

    def test_get_state(self):
        """Test state persistence."""
        cm = TokenBasedConversationManager(max_tokens=4000)
        cm._current_tokens = 1500

        state = cm.get_state()

        assert state["current_tokens"] == 1500

    def test_restore_from_session(self):
        """Test state restoration."""
        cm = TokenBasedConversationManager()
        state = {
            "__name__": "TokenBasedConversationManager",
            "removed_message_count": 3,
            "current_tokens": 2000,
        }

        cm.restore_from_session(state)

        assert cm._current_tokens == 2000
        assert cm.removed_message_count == 3


# Parametrized tests

@pytest.mark.parametrize("max_messages,expected_trim", [
    (5, True),   # Should trim 10 -> 5
    (10, False), # No trim needed
    (20, False), # No trim needed
])
def test_apply_management_parametrized(max_messages, expected_trim):
    """Test apply_management with various limits."""
    cm = YourConversationManager(max_messages=max_messages)
    mock_agent = MagicMock()
    mock_agent.messages = [
        {"role": "user", "content": [{"text": f"Message {i}"}]}
        for i in range(10)
    ]

    cm.apply_management(mock_agent)

    if expected_trim:
        assert len(mock_agent.messages) <= max_messages
        assert cm.removed_message_count > 0
    else:
        assert cm.removed_message_count == 0


@pytest.mark.parametrize("message_count", [1, 2, 3])
def test_reduce_context_minimal_conversations(message_count):
    """Test reduce_context with minimal conversations."""
    cm = YourConversationManager()
    mock_agent = MagicMock()
    mock_agent.messages = [
        {"role": "user", "content": [{"text": f"Message {i}"}]}
        for i in range(message_count)
    ]

    if message_count <= 2:
        with pytest.raises((ContextWindowOverflowException, Exception)):
            cm.reduce_context(mock_agent)
    else:
        # Should succeed with 3+ messages
        cm.reduce_context(mock_agent)
        assert len(mock_agent.messages) < message_count


# TODO: Add integration tests

@pytest.mark.skip(reason="Integration test - requires full agent setup")
class TestConversationManagerIntegration:
    """Integration tests for conversation managers."""

    def test_with_real_agent(self):
        """Test conversation manager with real agent."""
        pass
