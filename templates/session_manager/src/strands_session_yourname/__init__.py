"""
Strands Session Manager Template - Your Session Manager Name

TODO: Replace this docstring with a description of your session manager.

This module provides a session manager implementation for persisting agent
conversations and state to [describe your storage backend].

Example:
    Basic usage of the session manager:

    >>> from strands import Agent
    >>> from strands_session_yourname import YourSessionManager
    >>>
    >>> session = YourSessionManager(session_id="my-session", storage_config="...")
    >>> agent = Agent(session_manager=session)
    >>> agent("Hello, how are you?")
"""

from strands_session_yourname.your_session_manager import YourSessionManager

__all__ = ["YourSessionManager"]
__version__ = "0.1.0"
