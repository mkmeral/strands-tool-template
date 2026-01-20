"""
Strands SDK Component Templates

TODO: Replace this docstring with a description of your package.

This module provides custom components for Strands Agents:

- Tool: Custom tool implementation
- Model Provider: Custom AI model integration
- Hook Provider: Event callbacks for agent lifecycle
- Session Manager: Conversation persistence
- Conversation Manager: Conversation history management

Example:
    Using the tool:

    >>> from strands import Agent
    >>> from strands_tool_yourname import your_tool
    >>> agent = Agent(tools=[your_tool])
    >>> agent("Help me with [task]")

    Using the model provider:

    >>> from strands import Agent
    >>> from strands_tool_yourname import YourModel
    >>> model = YourModel(api_key="...", model_id="...")
    >>> agent = Agent(model=model)

    Using hooks:

    >>> from strands import Agent
    >>> from strands_tool_yourname import YourHookProvider
    >>> agent = Agent(hooks=[YourHookProvider()])

    Using session manager:

    >>> from strands import Agent
    >>> from strands_tool_yourname import YourSessionManager
    >>> session = YourSessionManager(session_id="my-session")
    >>> agent = Agent(session_manager=session)

    Using conversation manager:

    >>> from strands import Agent
    >>> from strands_tool_yourname import YourConversationManager
    >>> cm = YourConversationManager(max_messages=50)
    >>> agent = Agent(conversation_manager=cm)
"""

from strands_tool_yourname.your_tool import your_tool
from strands_tool_yourname.your_model import YourModel
from strands_tool_yourname.your_hook_provider import YourHookProvider
from strands_tool_yourname.your_session_manager import YourSessionManager
from strands_tool_yourname.your_conversation_manager import YourConversationManager

__all__ = [
    "your_tool",
    "YourModel",
    "YourHookProvider",
    "YourSessionManager",
    "YourConversationManager",
]
__version__ = "0.1.0"
