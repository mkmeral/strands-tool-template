"""
Tests for YourHookProvider

TODO: Add comprehensive tests for your hook provider.
"""

import pytest
from unittest.mock import MagicMock

from strands.hooks.registry import HookRegistry
from strands.hooks.events import (
    AgentInitializedEvent,
    BeforeInvocationEvent,
    AfterInvocationEvent,
    BeforeToolCallEvent,
    AfterToolCallEvent,
    AfterModelCallEvent,
)

from strands_tool_yourname import YourHookProvider


class TestYourHookProviderInit:
    """Tests for initialization."""

    def test_init_default(self):
        """Test default initialization."""
        hooks = YourHookProvider()
        assert hooks.config_option is None
        assert hooks.enable_feature is True

    def test_init_with_config(self):
        """Test initialization with configuration."""
        hooks = YourHookProvider(config_option="value", enable_feature=False)
        assert hooks.config_option == "value"
        assert hooks.enable_feature is False


class TestYourHookProviderRegistration:
    """Tests for hook registration."""

    def test_register_hooks(self):
        """Test that hooks are registered."""
        hooks = YourHookProvider()
        registry = HookRegistry()
        hooks.register_hooks(registry)
        assert registry.has_callbacks()


class TestYourHookProviderCallbacks:
    """Tests for callback behavior."""

    def test_on_agent_initialized(self):
        """Test agent initialized callback."""
        hooks = YourHookProvider()
        mock_agent = MagicMock()
        event = AgentInitializedEvent(agent=mock_agent)
        hooks._on_agent_initialized(event)  # Should not raise

    def test_on_before_invocation_increments_counter(self):
        """Test that before invocation increments request counter."""
        hooks = YourHookProvider()
        mock_agent = MagicMock()
        event = BeforeInvocationEvent(agent=mock_agent)
        assert hooks._request_count == 0
        hooks._on_before_invocation(event)
        assert hooks._request_count == 1

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
        hooks._on_before_tool_call(event)  # Should not raise

    def test_on_after_model_call_success(self):
        """Test after model call callback with success."""
        hooks = YourHookProvider()
        mock_agent = MagicMock()
        stop_response = AfterModelCallEvent.ModelStopResponse(
            message={"role": "assistant", "content": [{"text": "Hi"}]},
            stop_reason="end_turn",
        )
        event = AfterModelCallEvent(agent=mock_agent, stop_response=stop_response)
        hooks._on_after_model_call(event)  # Should not raise


class TestYourHookProviderMetrics:
    """Tests for metrics."""

    def test_get_metrics(self):
        """Test getting metrics."""
        hooks = YourHookProvider()
        metrics = hooks.get_metrics()
        assert metrics["request_count"] == 0

    def test_reset_metrics(self):
        """Test resetting metrics."""
        hooks = YourHookProvider()
        hooks._request_count = 5
        hooks.reset_metrics()
        assert hooks._request_count == 0
