"""
Tests for YourSessionManager

TODO: Add comprehensive tests for your session manager.
"""

import pytest
from unittest.mock import MagicMock

from strands_tool_yourname import YourSessionManager


class TestYourSessionManagerInit:
    """Tests for initialization."""

    def test_init_with_session_id(self):
        """Test initialization with session ID."""
        session = YourSessionManager(session_id="test-session")
        assert session.session_id == "test-session"
        assert session.auto_create is True

    def test_init_with_all_config(self):
        """Test initialization with all options."""
        session = YourSessionManager(
            session_id="test-session",
            connection_string="your://connection",
            auto_create=False,
        )
        assert session.connection_string == "your://connection"
        assert session.auto_create is False


class TestYourSessionManagerInitialize:
    """Tests for agent initialization."""

    def test_initialize_new_agent(self):
        """Test initializing a new agent."""
        session = YourSessionManager(session_id="test-session")
        mock_agent = MagicMock()
        mock_agent.name = "test-agent"
        mock_agent.messages = []
        mock_agent.conversation_manager = None

        session.initialize(mock_agent)

        assert "test-agent" in session._initialized_agents
        assert session._message_counters["test-agent"] == 0


class TestYourSessionManagerMessages:
    """Tests for message handling."""

    def test_append_message(self):
        """Test appending a message."""
        session = YourSessionManager(session_id="test-session")
        mock_agent = MagicMock()
        mock_agent.name = "test-agent"
        mock_agent.messages = []
        mock_agent.conversation_manager = None

        session.initialize(mock_agent)
        message = {"role": "user", "content": [{"text": "Hello"}]}
        session.append_message(message, mock_agent)

        assert session._message_counters["test-agent"] == 1

    def test_redact_latest_message(self):
        """Test redacting the latest message."""
        session = YourSessionManager(session_id="test-session")
        mock_agent = MagicMock()
        mock_agent.name = "test-agent"
        mock_agent.messages = [{"role": "user", "content": [{"text": "Original"}]}]
        mock_agent.conversation_manager = None

        session.initialize(mock_agent)
        session.append_message({"role": "user", "content": [{"text": "Original"}]}, mock_agent)
        redacted = {"role": "user", "content": [{"text": "[REDACTED]"}]}
        session.redact_latest_message(redacted, mock_agent)

        # Counter should not change
        assert session._message_counters["test-agent"] == 1


class TestYourSessionManagerUtilities:
    """Tests for utility methods."""

    def test_get_agent_id_with_name(self):
        """Test getting agent ID with name."""
        session = YourSessionManager(session_id="test-session")
        mock_agent = MagicMock()
        mock_agent.name = "my-agent"
        assert session._get_agent_id(mock_agent) == "my-agent"

    def test_list_agents(self):
        """Test listing agents."""
        session = YourSessionManager(session_id="test-session")
        mock_agent = MagicMock()
        mock_agent.name = "agent-1"
        mock_agent.messages = []
        mock_agent.conversation_manager = None

        session.initialize(mock_agent)
        agents = session.list_agents()

        assert "agent-1" in agents
