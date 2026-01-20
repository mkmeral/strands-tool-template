"""
Strands Model Provider Template - Your Model Name

TODO: Replace this docstring with a description of your model provider.

This module provides a model provider implementation for [service/platform name],
enabling Strands Agents to use [model name] for AI inference.

Example:
    Basic usage of the model provider:

    >>> from strands import Agent
    >>> from strands_model_yourname import YourModel
    >>>
    >>> model = YourModel(api_key="your-api-key", model_id="your-model-id")
    >>> agent = Agent(model=model)
    >>> agent("Hello, how are you?")
"""

from strands_model_yourname.your_model import YourModel

__all__ = ["YourModel"]
__version__ = "0.1.0"
