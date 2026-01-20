"""
Strands Conversation Manager Template - Your Conversation Manager Name

TODO: Replace this docstring with a description of your conversation manager.

This module provides a conversation manager implementation for managing
agent conversation history using [describe your strategy].

Example:
    Basic usage of the conversation manager:

    >>> from strands import Agent
    >>> from strands_conversation_yourname import YourConversationManager
    >>>
    >>> cm = YourConversationManager(max_messages=50)
    >>> agent = Agent(conversation_manager=cm)
    >>> agent("Hello, how are you?")
"""

from strands_conversation_yourname.your_conversation_manager import YourConversationManager

__all__ = ["YourConversationManager"]
__version__ = "0.1.0"
