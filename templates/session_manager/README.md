# strands-session-yourname

> **TODO**: Replace "yourname" with your session manager name throughout this repository

A [Strands Agents](https://github.com/strands-agents/sdk-python) session manager for persisting conversations to [your storage backend].

## Installation

```bash
pip install strands-session-yourname
```

## Usage

### Basic Usage

```python
from strands import Agent
from strands_session_yourname import YourSessionManager

# Create session manager
session = YourSessionManager(
    session_id="user-123-session",
    connection_string="your://connection/string",
)

# Attach to agent
agent = Agent(session_manager=session)

# Use the agent - conversations are automatically persisted
result = agent("Hello, how are you?")
```

### Resume a Session

```python
from strands import Agent
from strands_session_yourname import YourSessionManager

# Create a new agent with the same session ID
session = YourSessionManager(session_id="user-123-session")
agent = Agent(session_manager=session)

# The agent automatically has the full conversation history
result = agent("What did we talk about earlier?")
```

### Configuration Options

```python
session = YourSessionManager(
    session_id="my-session",
    connection_string="your://connection/string",
    auto_create=True,  # Auto-create session if not exists
)
```

## How It Works

The session manager automatically hooks into agent lifecycle events:

1. **Agent Initialization** (`AgentInitializedEvent`)
   - Loads existing messages from storage
   - Restores conversation manager state

2. **Message Added** (`MessageAddedEvent`)
   - Persists each new message to storage
   - Syncs agent state

3. **After Invocation** (`AfterInvocationEvent`)
   - Syncs final agent state after each request

## Session Structure

```
session/
├── session_id: "user-123-session"
├── agents/
│   └── agent-name/
│       ├── metadata (conversation_manager_state, etc.)
│       └── messages/
│           ├── message_0.json
│           ├── message_1.json
│           └── ...
└── multi_agents/
    └── multi-agent-id/
        └── state.json
```

## Configuration

### Environment Variables

**TODO**: Document environment variables for your storage backend

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `YOUR_STORAGE_CONNECTION` | Connection string | None | Yes |
| `YOUR_STORAGE_TIMEOUT` | Connection timeout | 30 | No |

### Example Configuration

```bash
export YOUR_STORAGE_CONNECTION="your://localhost:6379"
```

## Implementing Your Session Manager

To implement a custom session manager:

1. **Extend `SessionManager`** base class
2. **Implement required methods**:
   - `initialize()` - Load agent state from storage
   - `append_message()` - Save new messages
   - `redact_latest_message()` - Update/redact messages
   - `sync_agent()` - Persist agent state

3. **(Optional) Implement multi-agent methods**:
   - `initialize_multi_agent()`
   - `sync_multi_agent()`

### Required Method Signatures

```python
def initialize(self, agent: "Agent", **kwargs) -> None:
    """Load agent state from storage on initialization."""
    pass

def append_message(self, message: Message, agent: "Agent", **kwargs) -> None:
    """Persist a new message to storage."""
    pass

def redact_latest_message(self, redact_message: Message, agent: "Agent", **kwargs) -> None:
    """Update the most recent message (for redaction)."""
    pass

def sync_agent(self, agent: "Agent", **kwargs) -> None:
    """Sync agent state (conversation manager, etc.) to storage."""
    pass
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/strands-session-yourname
cd strands-session-yourname

# Install in development mode
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Linting and Formatting

```bash
# Check formatting
ruff format --check

# Format code
ruff format

# Run linter
ruff check

# Type checking
mypy src
```

## Publishing to PyPI

1. Update the version in `pyproject.toml`
2. Commit your changes: `git commit -am "Release v0.1.0"`
3. Create a git tag: `git tag v0.1.0`
4. Push with tags: `git push && git push --tags`
5. Create a GitHub release from the tag

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Apache 2.0 License - see [LICENSE](LICENSE) file for details.

## Links

- [Strands Agents Documentation](https://strandsagents.com/)
- [Strands Agents GitHub](https://github.com/strands-agents/sdk-python)
- [Session Management in SDK](https://github.com/strands-agents/sdk-python/tree/main/src/strands/session)

---

Built with ❤️ for the [Strands Agents](https://github.com/strands-agents/sdk-python) community
