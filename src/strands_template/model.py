"""Model Provider Implementation."""

import logging
from collections.abc import AsyncGenerator
from typing import Any

from typing_extensions import override

from strands.models.model import Model
from strands.types.content import Messages
from strands.types.streaming import StreamEvent
from strands.types.tools import ToolSpec

logger = logging.getLogger(__name__)


class TemplateModel(Model):
    """Template model provider implementation."""

    def __init__(self, api_key: str, model_id: str) -> None:
        """Initialize the model provider."""
        self.api_key = api_key
        self.model_id = model_id

    @override
    def update_config(self, **model_config: Any) -> None:
        """Update the model configuration."""
        pass

    @override
    def get_config(self) -> dict[str, Any]:
        """Get the current model configuration."""
        return {"api_key": self.api_key, "model_id": self.model_id}

    @override
    async def stream(
        self,
        messages: Messages,
        tool_specs: list[ToolSpec] | None = None,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> AsyncGenerator[StreamEvent, None]:
        """Stream conversation with the model."""
        # TODO: Implement streaming logic
        raise NotImplementedError
        yield  # type: ignore
