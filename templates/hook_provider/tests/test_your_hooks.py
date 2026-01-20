"""
Tests for Hook Providers

TODO: Add comprehensive tests for your hook providers.
"""

import pytest
from unittest.mock import MagicMock, patch

from strands.hooks.registry import HookRegistry
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

from strands_hooks_yourname import YourHookProvider
from strands_hooks_yourname.your_hooks import LoggingHookProvider


class TestYourHookProviderInit:
    """Tests for YourHookProvider initialization."""

    def test_init_default(self):
        """Test default initialization."""
        hooks = YourHookProvider()

        assert hooks.config_option is None
        assert hooks.enable_feature is True

    def test_init_with_config(self):
        """Test initialization with configuration."""
        hooks = YourHookProvider(
            config_option="custom_value",
            enable_feature=False,
        )

        assert hooks.config_option == "custom_value"
        assert hooks.enable_feature is False


class TestYourHookProviderRegistration:
    """Tests for hook registration."""

    def test_register_hooks(self):
        """Test that hooks are registered with the registry."""
        hooks = YourHookProvider()
        registry = HookRegistry()

        hooks.register_hooks(registry)

        # Verify callbacks are registered by checking the registry has callbacks
        assert registry.has_callbacks()

    def test_register_hooks_for_all_events(self):
        """Test that callbacks are registered for expected events."""
        hooks = YourHookProvider()
        registry = HookRegistry()

        hooks.register_hooks(registry)

        # Create mock events and verify callbacks exist
        mock_agent = MagicMock()

        # These should not raise errors if callbacks are registered
        event_types = [
            AgentInitializedEvent,
            BeforeInvocationEvent,
            AfterInvocationEvent,
            MessageAddedEvent,
            BeforeToolCallEvent,
            AfterToolCallEvent,
            BeforeModelCallEvent,
            AfterModelCallEvent,
        ]

        for event_type in event_types:
            # Check that callbacks exist for each event type
            assert event_type in registry._registered_callbacks


class TestYourHookProviderCallbacks:
    """Tests for hook callback behavior."""

    def test_on_agent_initialized(self):
        """Test agent initialized callback."""
        hooks = YourHookProvider()
        mock_agent = MagicMock()
        event = AgentInitializedEvent(agent=mock_agent)

        # Should not raise
        hooks._on_agent_initialized(event)

    def test_on_before_invocation_increments_counter(self):
        """Test that before invocation increments request counter."""
        hooks = YourHookProvider()
        mock_agent = MagicMock()
        event = BeforeInvocationEvent(agent=mock_agent)

        assert hooks._request_count == 0

        hooks._on_before_invocation(event)

        assert hooks._request_count == 1

    def test_on_after_invocation(self):
        """Test after invocation callback."""
        hooks = YourHookProvider()
        mock_agent = MagicMock()
        event = AfterInvocationEvent(agent=mock_agent)

        # Should not raise
        hooks._on_after_invocation(event)

    def test_on_message_added(self):
        """Test message added callback."""
        hooks = YourHookProvider()
        mock_agent = MagicMock()
        message = {"role": "user", "content": [{"text": "Hello"}]}
        event = MessageAddedEvent(agent=mock_agent, message=message)

        # Should not raise
        hooks._on_message_added(event)

    def test_on_before_tool_call(self):
        """Test before tool call callback."""
        hooks = YourHookProvider()
        mock_agent = MagicMock()
        event = BeforeToolCallEvent(
            agent=mock_agent,
            selected_tool=MagicMock(),
            tool_use={"name": "test_tool", "toolUseId": "123", "input": {}},
            invocation_state={},
        )

        # Should not raise
        hooks._on_before_tool_call(event)

    def test_on_after_tool_call(self):
        """Test after tool call callback."""
        hooks = YourHookProvider()
        mock_agent = MagicMock()
        event = AfterToolCallEvent(
            agent=mock_agent,
            selected_tool=MagicMock(),
            tool_use={"name": "test_tool", "toolUseId": "123", "input": {}},
            invocation_state={},
            result={"status": "success", "content": [{"text": "result"}]},
        )

        # Should not raise
        hooks._on_after_tool_call(event)

    def test_on_before_model_call(self):
        """Test before model call callback."""
        hooks = YourHookProvider()
        mock_agent = MagicMock()
        event = BeforeModelCallEvent(agent=mock_agent)

        # Should not raise
        hooks._on_before_model_call(event)

    def test_on_after_model_call_success(self):
        """Test after model call callback with successful response."""
        hooks = YourHookProvider()
        mock_agent = MagicMock()

        stop_response = AfterModelCallEvent.ModelStopResponse(
            message={"role": "assistant", "content": [{"text": "Hello"}]},
            stop_reason="end_turn",
        )
        event = AfterModelCallEvent(agent=mock_agent, stop_response=stop_response)

        # Should not raise
        hooks._on_after_model_call(event)

    def test_on_after_model_call_error(self):
        """Test after model call callback with error."""
        hooks = YourHookProvider()
        mock_agent = MagicMock()
        event = AfterModelCallEvent(
            agent=mock_agent,
            exception=Exception("Test error"),
        )

        # Should not raise
        hooks._on_after_model_call(event)


class TestYourHookProviderMetrics:
    """Tests for metrics collection."""

    def test_get_metrics(self):
        """Test getting metrics."""
        hooks = YourHookProvider()

        metrics = hooks.get_metrics()

        assert "request_count" in metrics
        assert "total_tokens" in metrics
        assert metrics["request_count"] == 0
        assert metrics["total_tokens"] == 0

    def test_metrics_after_invocations(self):
        """Test metrics are updated after invocations."""
        hooks = YourHookProvider()
        mock_agent = MagicMock()

        # Simulate multiple invocations
        for _ in range(3):
            event = BeforeInvocationEvent(agent=mock_agent)
            hooks._on_before_invocation(event)

        metrics = hooks.get_metrics()
        assert metrics["request_count"] == 3

    def test_reset_metrics(self):
        """Test resetting metrics."""
        hooks = YourHookProvider()
        mock_agent = MagicMock()

        # Add some metrics
        event = BeforeInvocationEvent(agent=mock_agent)
        hooks._on_before_invocation(event)
        assert hooks._request_count == 1

        # Reset
        hooks.reset_metrics()

        assert hooks._request_count == 0
        assert hooks._total_tokens == 0


class TestLoggingHookProvider:
    """Tests for LoggingHookProvider."""

    def test_init_default_level(self):
        """Test default log level."""
        hooks = LoggingHookProvider()

        import logging
        assert hooks.level == logging.DEBUG

    def test_init_custom_level(self):
        """Test custom log level."""
        hooks = LoggingHookProvider(level="INFO")

        import logging
        assert hooks.level == logging.INFO

    def test_register_hooks(self):
        """Test that logging hooks are registered."""
        hooks = LoggingHookProvider()
        registry = HookRegistry()

        hooks.register_hooks(registry)

        assert registry.has_callbacks()

    def test_log_event(self):
        """Test that events are logged."""
        hooks = LoggingHookProvider()
        mock_agent = MagicMock()
        event = AgentInitializedEvent(agent=mock_agent)

        with patch.object(hooks._logger, 'log') as mock_log:
            hooks._log_event(event)
            mock_log.assert_called_once()


# TODO: Add integration tests with real Agent if needed

@pytest.mark.skip(reason="Integration test - requires full agent setup")
class TestHookProviderIntegration:
    """Integration tests for hook providers."""

    def test_hooks_with_agent(self):
        """Test hooks work with real agent."""
        # TODO: Implement integration test
        pass


# Parametrized tests for different configurations

@pytest.mark.parametrize("config_option,enable_feature", [
    (None, True),
    ("value1", True),
    ("value2", False),
    (None, False),
])
def test_hook_provider_configurations(config_option, enable_feature):
    """Test various configuration combinations."""
    hooks = YourHookProvider(
        config_option=config_option,
        enable_feature=enable_feature,
    )

    assert hooks.config_option == config_option
    assert hooks.enable_feature == enable_feature


@pytest.mark.parametrize("level", ["DEBUG", "INFO", "WARNING", "ERROR"])
def test_logging_hook_provider_levels(level):
    """Test various logging levels."""
    import logging

    hooks = LoggingHookProvider(level=level)

    expected_level = getattr(logging, level)
    assert hooks.level == expected_level
