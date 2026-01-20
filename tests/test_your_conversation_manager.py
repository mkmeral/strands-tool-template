"""
Tests for YourConversationManager

TODO: Add comprehensive tests for your conversation manager.
"""

import pytest
from unittest.mock import MagicMock

from strands_tool_yourname import YourConversationManager
from strands.types.exceptions import ContextWindowOverflowException


class TestYourConversationManagerInit:
    """Tests for initialization."""

    def test_init_default(self):
        """Test default initialization."""
        cm = YourConversationManager()
        assert cm.max_messages == 50
        assert cm.preserve_important is True
        assert cm.removed_message_count == 0

    def test_init_with_config(self):
        """Test initialization with configuration."""
        cm = YourConversationManager(max_messages=100, preserve_important=False)
        assert cm.max_messages == 100
        assert cm.preserve_important is False


class TestYourConversationManagerApplyManagement:
    """Tests for apply_management."""

    def test_no_management_needed(self):
        """Test when under limit."""
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


class TestYourConversationManagerReduceContext:
    """Tests for reduce_context."""

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

    def test_reduce_context_raises_on_minimal(self):
        """Test raises when cannot reduce."""
        cm = YourConversationManager()
        mock_agent = MagicMock()
        mock_agent.messages = [{"role": "user", "content": [{"text": "Hello"}]}]

        with pytest.raises(ContextWindowOverflowException):
            cm.reduce_context(mock_agent)


class TestYourConversationManagerState:
    """Tests for state management."""

    def test_get_state(self):
        """Test getting state."""
        cm = YourConversationManager(max_messages=75)
        cm.removed_message_count = 10
        state = cm.get_state()

        assert state["__name__"] == "YourConversationManager"
        assert state["removed_message_count"] == 10
        assert state["max_messages"] == 75

    def test_restore_from_session(self):
        """Test restoring state."""
        cm = YourConversationManager()
        state = {
            "__name__": "YourConversationManager",
            "removed_message_count": 5,
            "custom_state": {"key": "value"},
        }

        result = cm.restore_from_session(state)

        assert cm.removed_message_count == 5
        assert result is None


class TestYourConversationManagerHelpers:
    """Tests for helper methods."""

    def test_find_valid_trim_index_basic(self):
        """Test finding valid trim index."""
        cm = YourConversationManager()
        messages = [
            {"role": "user", "content": [{"text": "1"}]},
            {"role": "assistant", "content": [{"text": "2"}]},
            {"role": "user", "content": [{"text": "3"}]},
        ]

        index = cm._find_valid_trim_index(messages, 1)
        assert index == 1

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
        assert index == 3
