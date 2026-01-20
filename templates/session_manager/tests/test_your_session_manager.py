"""
Tests for YourSessionManager

TODO: Add comprehensive tests for your session manager.
"""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock

from strands_session_yourname import YourSessionManager


class TestYourSessionManagerInit:
    """Tests for YourSessionManager initialization."""

    def test_init_with_session_id(self):
        """Test initialization with session ID."""
        session = YourSessionManager(session_id="test-session")

        assert session.session_id == "test-session"
        assert session.auto_create is True

    def test_init_with_all_config(self):
        """Test initialization with all configuration options."""
        session = YourSessionManager(
            session_id="test-session",
            connection_string="your://connection/string",
            auto_create=False,
        )

        assert session.session_id == "test-session"
        assert session.connection_string == "your://connection/string"
        assert session.auto_create is False


class TestYourSessionManagerInitialize:
    """Tests for agent initialization."""

    def test_initialize_new_agent(self):
        """Test initializing a new agent with no existing session."""
        session = YourSessionManager(session_id="test-session")
        mock_agent = MagicMock()
        mock_agent.name = "test-agent"
        mock_agent.messages = []
        mock_agent.conversation_manager = None

        session.initialize(mock_agent)

        assert "test-agent" in session._initialized_agents
        assert session._message_counters["test-agent"] == 0

    def test_initialize_agent_with_existing_messages(self):
        """Test initializing an agent that already has messages."""
        session = YourSessionManager(session_id="test-session")
        mock_agent = MagicMock()
        mock_agent.name = "test-agent"
        mock_agent.messages = [
            {"role": "user", "content": [{"text": "Hello"}]},
            {"role": "assistant", "content": [{"text": "Hi!"}]},
        ]
        mock_agent.conversation_manager = None

        session.initialize(mock_agent)

        assert session._message_counters["test-agent"] == 2

    def test_initialize_agent_without_name(self):
        """Test initializing an agent without a name attribute."""
        session = YourSessionManager(session_id="test-session")
        mock_agent = MagicMock(spec=[])  # No 'name' attribute
        mock_agent.messages = []
        mock_agent.conversation_manager = None
        # Simulate no name attribute
        del mock_agent.name

        session.initialize(mock_agent)

        # Should use object id as fallback
        assert len(session._initialized_agents) == 1


class TestYourSessionManagerMessages:
    """Tests for message handling."""

    def test_append_message(self):
        """Test appending a message to the session."""
        session = YourSessionManager(session_id="test-session")
        mock_agent = MagicMock()
        mock_agent.name = "test-agent"
        mock_agent.messages = []
        mock_agent.conversation_manager = None

        # Initialize first
        session.initialize(mock_agent)

        message = {"role": "user", "content": [{"text": "Hello"}]}
        session.append_message(message, mock_agent)

        assert session._message_counters["test-agent"] == 1

    def test_append_multiple_messages(self):
        """Test appending multiple messages."""
        session = YourSessionManager(session_id="test-session")
        mock_agent = MagicMock()
        mock_agent.name = "test-agent"
        mock_agent.messages = []
        mock_agent.conversation_manager = None

        session.initialize(mock_agent)

        messages = [
            {"role": "user", "content": [{"text": "Hello"}]},
            {"role": "assistant", "content": [{"text": "Hi!"}]},
            {"role": "user", "content": [{"text": "How are you?"}]},
        ]

        for msg in messages:
            session.append_message(msg, mock_agent)

        assert session._message_counters["test-agent"] == 3

    def test_redact_latest_message(self):
        """Test redacting the latest message."""
        session = YourSessionManager(session_id="test-session")
        mock_agent = MagicMock()
        mock_agent.name = "test-agent"
        mock_agent.messages = [{"role": "user", "content": [{"text": "Original"}]}]
        mock_agent.conversation_manager = None

        session.initialize(mock_agent)
        session.append_message({"role": "user", "content": [{"text": "Original"}]}, mock_agent)

        redacted_message = {"role": "user", "content": [{"text": "[REDACTED]"}]}
        session.redact_latest_message(redacted_message, mock_agent)

        # Message counter should not change on redaction
        assert session._message_counters["test-agent"] == 1


class TestYourSessionManagerSync:
    """Tests for agent synchronization."""

    def test_sync_agent(self):
        """Test syncing agent state."""
        session = YourSessionManager(session_id="test-session")
        mock_agent = MagicMock()
        mock_agent.name = "test-agent"
        mock_agent.messages = []
        mock_agent.conversation_manager = MagicMock()
        mock_agent.conversation_manager.get_state.return_value = {"some": "state"}

        session.initialize(mock_agent)

        # Should not raise
        session.sync_agent(mock_agent)


class TestYourSessionManagerMultiAgent:
    """Tests for multi-agent support."""

    def test_initialize_multi_agent_raises(self):
        """Test that multi-agent initialization raises by default."""
        session = YourSessionManager(session_id="test-session")
        mock_multi_agent = MagicMock()

        with pytest.raises(NotImplementedError):
            session.initialize_multi_agent(mock_multi_agent)

    def test_sync_multi_agent_raises(self):
        """Test that multi-agent sync raises by default."""
        session = YourSessionManager(session_id="test-session")
        mock_multi_agent = MagicMock()

        with pytest.raises(NotImplementedError):
            session.sync_multi_agent(mock_multi_agent)


class TestYourSessionManagerUtilities:
    """Tests for utility methods."""

    def test_get_agent_id_with_name(self):
        """Test getting agent ID when agent has a name."""
        session = YourSessionManager(session_id="test-session")
        mock_agent = MagicMock()
        mock_agent.name = "my-agent"

        agent_id = session._get_agent_id(mock_agent)

        assert agent_id == "my-agent"

    def test_get_agent_id_without_name(self):
        """Test getting agent ID when agent has no name."""
        session = YourSessionManager(session_id="test-session")
        mock_agent = MagicMock(spec=[])
        del mock_agent.name

        agent_id = session._get_agent_id(mock_agent)

        assert agent_id.startswith("agent_")

    def test_list_agents(self):
        """Test listing initialized agents."""
        session = YourSessionManager(session_id="test-session")
        mock_agent1 = MagicMock()
        mock_agent1.name = "agent-1"
        mock_agent1.messages = []
        mock_agent1.conversation_manager = None

        mock_agent2 = MagicMock()
        mock_agent2.name = "agent-2"
        mock_agent2.messages = []
        mock_agent2.conversation_manager = None

        session.initialize(mock_agent1)
        session.initialize(mock_agent2)

        agents = session.list_agents()

        assert "agent-1" in agents
        assert "agent-2" in agents

    def test_close(self):
        """Test closing the session manager."""
        session = YourSessionManager(session_id="test-session")

        # Should not raise
        session.close()


class TestYourSessionManagerHookRegistration:
    """Tests for hook registration."""

    def test_register_hooks(self):
        """Test that hooks are registered correctly."""
        from strands.hooks.registry import HookRegistry

        session = YourSessionManager(session_id="test-session")
        registry = HookRegistry()

        session.register_hooks(registry)

        # Verify callbacks were registered
        assert registry.has_callbacks()


# TODO: Add integration tests with actual storage backend

@pytest.mark.skip(reason="Integration test - requires storage backend")
class TestYourSessionManagerIntegration:
    """Integration tests for YourSessionManager."""

    def test_full_session_lifecycle(self):
        """Test complete session lifecycle with real storage."""
        # TODO: Implement integration test
        pass

    def test_session_resume(self):
        """Test resuming a session with new agent instance."""
        # TODO: Implement integration test
        pass


# Parametrized tests

@pytest.mark.parametrize("session_id", [
    "simple-id",
    "id-with-numbers-123",
    "UUID-like-550e8400-e29b-41d4-a716-446655440000",
])
def test_session_id_formats(session_id):
    """Test various session ID formats are accepted."""
    session = YourSessionManager(session_id=session_id)
    assert session.session_id == session_id


@pytest.mark.parametrize("auto_create", [True, False])
def test_auto_create_option(auto_create):
    """Test auto_create configuration option."""
    session = YourSessionManager(session_id="test", auto_create=auto_create)
    assert session.auto_create == auto_create
