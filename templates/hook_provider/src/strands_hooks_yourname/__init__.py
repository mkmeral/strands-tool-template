"""
Strands Hook Provider Template - Your Hook Provider Name

TODO: Replace this docstring with a description of your hook provider.

This module provides hook providers for extending Strands Agent functionality,
enabling [describe what your hooks enable].

Example:
    Basic usage of the hook provider:

    >>> from strands import Agent
    >>> from strands_hooks_yourname import YourHookProvider
    >>>
    >>> hooks = YourHookProvider(config_option="value")
    >>> agent = Agent(hooks=[hooks])
    >>> agent("Hello, how are you?")
"""

from strands_hooks_yourname.your_hooks import YourHookProvider

__all__ = ["YourHookProvider"]
__version__ = "0.1.0"
