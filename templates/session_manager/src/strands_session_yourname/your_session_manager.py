"""
Your Session Manager Implementation

TODO: Replace this docstring with a detailed description of your session manager.

This module implements a session manager for persisting agent conversations
and state to [describe your storage backend, e.g., Redis, DynamoDB, PostgreSQL].

Key Features:
1. [Feature 1: e.g., Persistent conversation storage]
2. [Feature 2: e.g., Session resume across restarts]
3. [Feature 3: e.g., Multi-agent session support]

Usage with Strands Agent:
```python
from strands import Agent
from strands_session_yourname import YourSessionManager

# Create session manager with storage configuration
session = YourSessionManager(
    session_id="my-session-123",
    connection_string="your-storage-connection-string",
)

# Attach to agent
agent = Agent(session_manager=session)

# Use the agent - conversation is automatically persisted
result = agent("Hello, how are you?")

# Later, create a new agent with the same session to resume
agent2 = Agent(session_manager=YourSessionManager(session_id="my-session-123"))
# agent2 will have the full conversation history
```

Session Structure:
```
session/
├── session_id: "my-session-123"
├── agents/
│   └── agent_id/
│       ├── agent_metadata
│       └── messages[]
└── multi_agents/
    └── multi_agent_id/
        └── multi_agent_state
```
"""

import logging
from typing import TYPE_CHECKING, Any

from strands.hooks.events import AgentInitializedEvent, AfterInvocationEvent, MessageAddedEvent
from strands.hooks.registry import HookProvider, HookRegistry
from strands.session.session_manager import SessionManager
from strands.types.content import Message

if TYPE_CHECKING:
    from strands.agent.agent import Agent
    from strands.multiagent.base import MultiAgentBase

logger = logging.getLogger(__name__)


class YourSessionManager(SessionManager):
    """Your session manager implementation.

    TODO: Replace this docstring with a detailed description of your session manager.

    This session manager persists agent conversations and state to
    [describe your storage backend], enabling:

    - [Capability 1: e.g., Resume conversations after agent restarts]
    - [Capability 2: e.g., Share sessions across multiple agent instances]
    - [Capability 3: e.g., Audit trail of all conversations]

    The session manager automatically hooks into agent lifecycle events to
    persist changes as they happen, ensuring durability.

    Attributes:
        session_id: Unique identifier for this session.
        connection_string: Connection string for the storage backend.

    Example:
        ```python
        from strands import Agent
        from strands_session_yourname import YourSessionManager

        session = YourSessionManager(
            session_id="user-123-session",
            connection_string="your://connection/string",
        )
        agent = Agent(session_manager=session)
        ```
    """

    def __init__(
        self,
        session_id: str,
        *,
        connection_string: str | None = None,
        auto_create: bool = True,
        # TODO: Add your storage-specific configuration parameters
        **kwargs: Any,
    ) -> None:
        """Initialize the session manager.

        Args:
            session_id: Unique identifier for this session.
                This ID is used to store and retrieve session data.
            connection_string: Connection string for your storage backend.
                Can also be set via environment variable.
            auto_create: If True, automatically create the session if it doesn't exist.
                Defaults to True.
            **kwargs: Additional keyword arguments for future extensibility.

        Raises:
            ValueError: If session_id is invalid.
            ConnectionError: If unable to connect to storage backend.

        Example:
            ```python
            session = YourSessionManager(
                session_id="my-session",
                connection_string="redis://localhost:6379",
                auto_create=True,
            )
            ```
        """
        self.session_id = session_id
        self.connection_string = connection_string
        self.auto_create = auto_create

        # TODO: Initialize your storage client
        # self._client = YourStorageClient(connection_string)

        # Internal state tracking
        self._initialized_agents: set[str] = set()
        self._message_counters: dict[str, int] = {}

        logger.debug(
            "session_id=<%s>, auto_create=<%s> | initialized session manager",
            session_id,
            auto_create,
        )

    # =========================================================================
    # Hook Registration (inherited from SessionManager)
    # =========================================================================

    # The base SessionManager.register_hooks() method automatically registers
    # callbacks for:
    # - AgentInitializedEvent -> self.initialize()
    # - MessageAddedEvent -> self.append_message() and self.sync_agent()
    # - AfterInvocationEvent -> self.sync_agent()
    #
    # You can override register_hooks() to add custom hooks if needed.

    # =========================================================================
    # Core Session Methods (Abstract - Must Implement)
    # =========================================================================

    def initialize(self, agent: "Agent", **kwargs: Any) -> None:
        """Initialize an agent with session data.

        This method is called when the agent is initialized. It should:
        1. Check if a session exists for this agent
        2. If exists, restore the agent's state (messages, conversation manager state)
        3. If not exists and auto_create is True, create a new session

        Args:
            agent: The agent to initialize with session data.
            **kwargs: Additional keyword arguments.

        Note:
            This method is called via the AgentInitializedEvent hook.
        """
        agent_id = self._get_agent_id(agent)

        logger.debug(
            "session_id=<%s>, agent_id=<%s> | initializing agent with session",
            self.session_id,
            agent_id,
        )

        # TODO: Implement session initialization
        # 1. Check if session/agent exists in storage
        # existing_session = self._client.get_session(self.session_id, agent_id)
        #
        # if existing_session:
        #     # Restore messages
        #     messages = existing_session.get("messages", [])
        #     agent.messages.extend(messages)
        #
        #     # Restore conversation manager state if present
        #     cm_state = existing_session.get("conversation_manager_state")
        #     if cm_state and agent.conversation_manager:
        #         prepend_messages = agent.conversation_manager.restore_from_session(cm_state)
        #         if prepend_messages:
        #             agent.messages[:0] = prepend_messages
        #
        # elif self.auto_create:
        #     # Create new session entry
        #     self._client.create_session(self.session_id, agent_id)

        self._initialized_agents.add(agent_id)
        self._message_counters[agent_id] = len(agent.messages)

        logger.info(
            "session_id=<%s>, agent_id=<%s>, message_count=<%d> | agent initialized with session",
            self.session_id,
            agent_id,
            len(agent.messages),
        )

    def append_message(self, message: Message, agent: "Agent", **kwargs: Any) -> None:
        """Append a message to the session storage.

        This method is called each time a message is added to the agent's
        conversation history. It should persist the message to storage.

        Args:
            message: The message to append.
            agent: The agent the message belongs to.
            **kwargs: Additional keyword arguments.

        Note:
            This method is called via the MessageAddedEvent hook.
        """
        agent_id = self._get_agent_id(agent)
        message_index = self._message_counters.get(agent_id, 0)

        logger.debug(
            "session_id=<%s>, agent_id=<%s>, message_index=<%d> | appending message",
            self.session_id,
            agent_id,
            message_index,
        )

        # TODO: Implement message persistence
        # self._client.append_message(
        #     session_id=self.session_id,
        #     agent_id=agent_id,
        #     message_index=message_index,
        #     message=message,
        # )

        self._message_counters[agent_id] = message_index + 1

    def redact_latest_message(self, redact_message: Message, agent: "Agent", **kwargs: Any) -> None:
        """Redact (replace) the most recently appended message.

        This method is called when a message needs to be redacted (e.g., for
        privacy or content filtering). It should update the most recent
        message in storage.

        Args:
            redact_message: The new message content to replace the latest message.
            agent: The agent whose message should be redacted.
            **kwargs: Additional keyword arguments.
        """
        agent_id = self._get_agent_id(agent)
        message_index = self._message_counters.get(agent_id, 1) - 1

        logger.debug(
            "session_id=<%s>, agent_id=<%s>, message_index=<%d> | redacting message",
            self.session_id,
            agent_id,
            message_index,
        )

        # TODO: Implement message redaction
        # self._client.update_message(
        #     session_id=self.session_id,
        #     agent_id=agent_id,
        #     message_index=message_index,
        #     message=redact_message,
        # )

    def sync_agent(self, agent: "Agent", **kwargs: Any) -> None:
        """Synchronize agent state with session storage.

        This method is called after each invocation and message to ensure
        the agent's current state is persisted. It should save:
        - Conversation manager state
        - Any agent-level metadata that changed

        Args:
            agent: The agent to synchronize.
            **kwargs: Additional keyword arguments.

        Note:
            This method is called via MessageAddedEvent and AfterInvocationEvent hooks.
        """
        agent_id = self._get_agent_id(agent)

        logger.debug(
            "session_id=<%s>, agent_id=<%s> | syncing agent state",
            self.session_id,
            agent_id,
        )

        # TODO: Implement agent state synchronization
        # Get conversation manager state
        # cm_state = None
        # if agent.conversation_manager:
        #     cm_state = agent.conversation_manager.get_state()
        #
        # self._client.update_agent(
        #     session_id=self.session_id,
        #     agent_id=agent_id,
        #     conversation_manager_state=cm_state,
        #     # Add any other agent metadata to persist
        # )

    # =========================================================================
    # Multi-Agent Session Methods (Optional - Override if needed)
    # =========================================================================

    def initialize_multi_agent(self, source: "MultiAgentBase", **kwargs: Any) -> None:
        """Initialize a multi-agent system with session data.

        Override this method if your session manager supports multi-agent
        persistence. The default implementation raises NotImplementedError.

        Args:
            source: The multi-agent source to initialize.
            **kwargs: Additional keyword arguments.
        """
        # TODO: Implement if supporting multi-agent persistence
        # multi_agent_id = source.id
        # existing_state = self._client.get_multi_agent(self.session_id, multi_agent_id)
        # if existing_state:
        #     source.deserialize_state(existing_state)
        super().initialize_multi_agent(source, **kwargs)

    def sync_multi_agent(self, source: "MultiAgentBase", **kwargs: Any) -> None:
        """Synchronize multi-agent state with session storage.

        Override this method if your session manager supports multi-agent
        persistence. The default implementation raises NotImplementedError.

        Args:
            source: The multi-agent source to synchronize.
            **kwargs: Additional keyword arguments.
        """
        # TODO: Implement if supporting multi-agent persistence
        # multi_agent_id = source.id
        # state = source.serialize_state()
        # self._client.update_multi_agent(self.session_id, multi_agent_id, state)
        super().sync_multi_agent(source, **kwargs)

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _get_agent_id(self, agent: "Agent") -> str:
        """Get a unique identifier for an agent.

        Args:
            agent: The agent to get an ID for.

        Returns:
            A unique string identifier for the agent.
        """
        # Use agent's name if available, otherwise use object id
        return getattr(agent, "name", None) or f"agent_{id(agent)}"

    # =========================================================================
    # Session Management Methods (Optional utilities)
    # =========================================================================

    def delete_session(self) -> None:
        """Delete this session and all associated data.

        This permanently removes the session from storage.

        Raises:
            SessionException: If the session doesn't exist or deletion fails.
        """
        logger.info("session_id=<%s> | deleting session", self.session_id)

        # TODO: Implement session deletion
        # self._client.delete_session(self.session_id)

    def list_agents(self) -> list[str]:
        """List all agent IDs in this session.

        Returns:
            List of agent IDs that have data in this session.
        """
        # TODO: Implement agent listing
        # return self._client.list_agents(self.session_id)
        return list(self._initialized_agents)

    def get_messages(self, agent_id: str, limit: int | None = None) -> list[Message]:
        """Retrieve messages for an agent from storage.

        Args:
            agent_id: The agent ID to get messages for.
            limit: Maximum number of messages to return (most recent).

        Returns:
            List of messages from the session.
        """
        # TODO: Implement message retrieval
        # return self._client.get_messages(self.session_id, agent_id, limit=limit)
        return []

    def close(self) -> None:
        """Close the session manager and release resources.

        Call this when done with the session manager to clean up
        connections and resources.
        """
        logger.debug("session_id=<%s> | closing session manager", self.session_id)

        # TODO: Implement cleanup
        # self._client.close()
