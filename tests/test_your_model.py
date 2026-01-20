"""
Tests for YourModel

TODO: Add comprehensive tests for your model provider.
"""

import pytest

from strands_tool_yourname import YourModel


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


class TestYourModelConfig:
    """Tests for configuration methods."""

    def test_update_config(self):
        """Test updating configuration."""
        model = YourModel(api_key="test-key", model_id="test-model")
        model.update_config(temperature=0.9, max_tokens=2000)
        config = model.get_config()
        assert config["temperature"] == 0.9
        assert config["max_tokens"] == 2000


class TestYourModelFormatting:
    """Tests for request/response formatting."""

    def test_format_text_content(self):
        """Test formatting text content."""
        model = YourModel(api_key="test-key", model_id="test-model")
        content = {"text": "Hello, world!"}
        formatted = model._format_request_message_content(content)
        assert formatted["type"] == "text"
        assert formatted["text"] == "Hello, world!"

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
        )
        messages = [{"role": "user", "content": [{"text": "Hello"}]}]
        request = model.format_request(messages, system_prompt="You are helpful")
        assert request["model"] == "test-model"
        assert request["stream"] is True


class TestYourModelChunkFormatting:
    """Tests for stream chunk formatting."""

    def test_format_message_start_chunk(self):
        """Test formatting message start chunk."""
        model = YourModel(api_key="test-key", model_id="test-model")
        result = model.format_chunk({"chunk_type": "message_start"})
        assert "messageStart" in result
        assert result["messageStart"]["role"] == "assistant"

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

        events = []
        async for event in model.stream(messages):
            events.append(event)

        assert any("messageStart" in event for event in events)
        assert any("messageStop" in event for event in events)
