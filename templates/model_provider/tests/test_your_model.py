"""
Tests for YourModel

TODO: Add comprehensive tests for your model provider.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from strands_model_yourname import YourModel


class TestYourModelInit:
    """Tests for YourModel initialization."""

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        model = YourModel(api_key="test-key", model_id="test-model")

        config = model.get_config()
        assert config["api_key"] == "test-key"
        assert config["model_id"] == "test-model"

    def test_init_with_all_config(self):
        """Test initialization with all configuration options."""
        model = YourModel(
            api_key="test-key",
            model_id="test-model",
            max_tokens=1000,
            temperature=0.7,
            top_p=0.9,
            stop_sequences=["END"],
        )

        config = model.get_config()
        assert config["max_tokens"] == 1000
        assert config["temperature"] == 0.7
        assert config["top_p"] == 0.9
        assert config["stop_sequences"] == ["END"]


class TestYourModelConfig:
    """Tests for YourModel configuration methods."""

    def test_update_config(self):
        """Test updating configuration."""
        model = YourModel(api_key="test-key", model_id="test-model")
        model.update_config(temperature=0.9, max_tokens=2000)

        config = model.get_config()
        assert config["temperature"] == 0.9
        assert config["max_tokens"] == 2000

    def test_get_config(self):
        """Test getting configuration."""
        model = YourModel(api_key="test-key", model_id="test-model", temperature=0.5)

        config = model.get_config()
        assert "api_key" in config
        assert "model_id" in config
        assert config["temperature"] == 0.5


class TestYourModelFormatting:
    """Tests for request/response formatting."""

    def test_format_text_content(self):
        """Test formatting text content."""
        model = YourModel(api_key="test-key", model_id="test-model")
        content = {"text": "Hello, world!"}

        formatted = model._format_request_message_content(content)

        assert formatted["type"] == "text"
        assert formatted["text"] == "Hello, world!"

    def test_format_tool_use_content(self):
        """Test formatting tool use content."""
        model = YourModel(api_key="test-key", model_id="test-model")
        content = {
            "toolUse": {
                "toolUseId": "tool-123",
                "name": "calculator",
                "input": {"expression": "2+2"},
            }
        }

        formatted = model._format_request_message_content(content)

        assert formatted["type"] == "tool_use"
        assert formatted["id"] == "tool-123"
        assert formatted["name"] == "calculator"

    def test_format_unsupported_content_raises_error(self):
        """Test that unsupported content types raise TypeError."""
        model = YourModel(api_key="test-key", model_id="test-model")
        content = {"unsupported_type": "data"}

        with pytest.raises(TypeError, match="unsupported type"):
            model._format_request_message_content(content)

    def test_format_request(self):
        """Test formatting a complete request."""
        model = YourModel(
            api_key="test-key",
            model_id="test-model",
            temperature=0.7,
            max_tokens=100,
        )

        messages = [{"role": "user", "content": [{"text": "Hello"}]}]
        tool_specs = [
            {
                "name": "test_tool",
                "description": "A test tool",
                "inputSchema": {"json": {"type": "object", "properties": {}}},
            }
        ]

        request = model.format_request(messages, tool_specs, "You are helpful")

        assert request["model"] == "test-model"
        assert request["stream"] is True
        assert request["temperature"] == 0.7
        assert request["max_tokens"] == 100
        assert "tools" in request
        assert len(request["tools"]) == 1

    def test_format_tool_specs(self):
        """Test formatting tool specifications."""
        model = YourModel(api_key="test-key", model_id="test-model")
        tool_specs = [
            {
                "name": "calculator",
                "description": "Performs calculations",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {"expression": {"type": "string"}},
                        "required": ["expression"],
                    }
                },
            }
        ]

        formatted = model._format_tool_specs(tool_specs)

        assert len(formatted) == 1
        assert formatted[0]["type"] == "function"
        assert formatted[0]["function"]["name"] == "calculator"

    def test_format_tool_specs_none(self):
        """Test formatting None tool specs returns None."""
        model = YourModel(api_key="test-key", model_id="test-model")

        assert model._format_tool_specs(None) is None


class TestYourModelChunkFormatting:
    """Tests for stream chunk formatting."""

    def test_format_message_start_chunk(self):
        """Test formatting message start chunk."""
        model = YourModel(api_key="test-key", model_id="test-model")

        result = model.format_chunk({"chunk_type": "message_start"})

        assert "messageStart" in result
        assert result["messageStart"]["role"] == "assistant"

    def test_format_content_start_text_chunk(self):
        """Test formatting text content start chunk."""
        model = YourModel(api_key="test-key", model_id="test-model")

        result = model.format_chunk({"chunk_type": "content_start", "data_type": "text"})

        assert "contentBlockStart" in result

    def test_format_content_delta_text_chunk(self):
        """Test formatting text content delta chunk."""
        model = YourModel(api_key="test-key", model_id="test-model")

        result = model.format_chunk({
            "chunk_type": "content_delta",
            "data_type": "text",
            "data": "Hello",
        })

        assert "contentBlockDelta" in result
        assert result["contentBlockDelta"]["delta"]["text"] == "Hello"

    def test_format_content_stop_chunk(self):
        """Test formatting content stop chunk."""
        model = YourModel(api_key="test-key", model_id="test-model")

        result = model.format_chunk({"chunk_type": "content_stop"})

        assert "contentBlockStop" in result

    def test_format_message_stop_chunk(self):
        """Test formatting message stop chunk."""
        model = YourModel(api_key="test-key", model_id="test-model")

        result = model.format_chunk({"chunk_type": "message_stop", "data": "end_turn"})

        assert "messageStop" in result
        assert result["messageStop"]["stopReason"] == "end_turn"

    def test_format_metadata_chunk(self):
        """Test formatting metadata chunk."""
        model = YourModel(api_key="test-key", model_id="test-model")

        result = model.format_chunk({
            "chunk_type": "metadata",
            "data": {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
        })

        assert "metadata" in result
        assert result["metadata"]["usage"]["inputTokens"] == 10
        assert result["metadata"]["usage"]["outputTokens"] == 20

    def test_format_unknown_chunk_raises_error(self):
        """Test that unknown chunk types raise RuntimeError."""
        model = YourModel(api_key="test-key", model_id="test-model")

        with pytest.raises(RuntimeError, match="unknown type"):
            model.format_chunk({"chunk_type": "unknown"})


class TestYourModelStream:
    """Tests for streaming functionality."""

    @pytest.mark.asyncio
    async def test_stream_basic(self):
        """Test basic streaming functionality."""
        model = YourModel(api_key="test-key", model_id="test-model")
        messages = [{"role": "user", "content": [{"text": "Hello"}]}]

        # TODO: Mock your API client and test the actual streaming
        # For now, test that the placeholder implementation works
        events = []
        async for event in model.stream(messages):
            events.append(event)

        # Verify we got the expected event types
        assert any("messageStart" in event for event in events)
        assert any("contentBlockStart" in event for event in events)
        assert any("contentBlockDelta" in event for event in events)
        assert any("contentBlockStop" in event for event in events)
        assert any("messageStop" in event for event in events)
        assert any("metadata" in event for event in events)


# TODO: Add integration tests if you want to test against real API
# These should be skipped by default and only run with specific flags

@pytest.mark.skip(reason="Integration test - requires real API credentials")
class TestYourModelIntegration:
    """Integration tests for YourModel."""

    @pytest.mark.asyncio
    async def test_real_api_call(self):
        """Test against real API."""
        # TODO: Implement integration test
        pass


# TODO: Add parametrized tests for edge cases

@pytest.mark.parametrize("stop_reason,expected", [
    ("stop", "end_turn"),
    ("end_turn", "end_turn"),
    ("tool_use", "tool_use"),
    ("tool_calls", "tool_use"),
    ("length", "max_tokens"),
    ("max_tokens", "max_tokens"),
    ("unknown", "end_turn"),  # Default fallback
])
def test_stop_reason_mapping(stop_reason, expected):
    """Test stop reason mapping from API to Strands format."""
    model = YourModel(api_key="test-key", model_id="test-model")

    result = model.format_chunk({"chunk_type": "message_stop", "data": stop_reason})

    assert result["messageStop"]["stopReason"] == expected
