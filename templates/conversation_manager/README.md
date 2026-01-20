# strands-conversation-yourname

> **TODO**: Replace "yourname" with your conversation manager name throughout this repository

A [Strands Agents](https://github.com/strands-agents/sdk-python) conversation manager implementing [describe your strategy].

## Installation

```bash
pip install strands-conversation-yourname
```

## Usage

### Basic Usage

```python
from strands import Agent
from strands_conversation_yourname import YourConversationManager

# Create conversation manager
cm = YourConversationManager(
    max_messages=50,
    preserve_important=True,
)

# Attach to agent
agent = Agent(conversation_manager=cm)

# Use the agent - conversation is automatically managed
result = agent("Help me with a task that requires many interactions")
```

### Configuration Options

```python
cm = YourConversationManager(
    max_messages=100,        # Maximum messages to keep
    preserve_important=True, # Preserve important messages when pruning
)
```

### With Session Persistence

```python
from strands import Agent
from strands_conversation_yourname import YourConversationManager
from strands.session import FileSessionManager

cm = YourConversationManager(max_messages=50)
session = FileSessionManager(session_id="my-session")

agent = Agent(
    conversation_manager=cm,
    session_manager=session,
)
```

## How It Works

The conversation manager is invoked at two key points:

### 1. `apply_management()` - Regular Management

Called after each agent event loop cycle. This method checks if the conversation
exceeds configured limits and applies your management strategy.

```python
def apply_management(self, agent: "Agent", **kwargs) -> None:
    messages = agent.messages
    if len(messages) <= self.max_messages:
        return  # No management needed
    
    # Apply your strategy to trim/manage messages
    # Modify agent.messages in-place
```

### 2. `reduce_context()` - Emergency Reduction

Called when a `ContextWindowOverflowException` is caught, indicating the model's
context window has been exceeded. This should aggressively reduce context.

```python
def reduce_context(self, agent: "Agent", e: Exception | None = None, **kwargs) -> None:
    # Aggressively reduce conversation size
    # Raise ContextWindowOverflowException if unable to reduce further
```

## Common Strategies

### Sliding Window
Keep the N most recent messages:
```python
messages[:] = messages[-max_messages:]
```

### Summarization
Replace old messages with summaries:
```python
old_messages = messages[:-keep_recent]
summary = summarize(old_messages)
messages[:] = [summary_message] + messages[-keep_recent:]
```

### Token-Based
Manage based on token count:
```python
while count_tokens(messages) > max_tokens:
    messages.pop(0)
```

### Importance-Based
Keep important messages regardless of age:
```python
important = [m for m in messages if is_important(m)]
recent = messages[-keep_recent:]
messages[:] = important + recent
```

## Important Considerations

### Tool Use/Result Pairs

When trimming messages, ensure you don't create invalid states:
- Don't start with a `toolResult` (needs preceding `toolUse`)
- Don't have a `toolUse` without its following `toolResult`

```python
def _find_valid_trim_index(self, messages, target):
    # Skip toolResult at trim point
    # Skip toolUse without immediate toolResult
    # Return valid trim index
```

### State Persistence

Implement `get_state()` and `restore_from_session()` for session support:

```python
def get_state(self) -> dict:
    state = super().get_state()
    state["my_custom_field"] = self.my_field
    return state

def restore_from_session(self, state: dict) -> list | None:
    result = super().restore_from_session(state)
    self.my_field = state.get("my_custom_field", default)
    return result
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/strands-conversation-yourname
cd strands-conversation-yourname

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
- [Conversation Managers in SDK](https://github.com/strands-agents/sdk-python/tree/main/src/strands/agent/conversation_manager)

---

Built with ❤️ for the [Strands Agents](https://github.com/strands-agents/sdk-python) community
