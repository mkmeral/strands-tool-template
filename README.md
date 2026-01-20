# Strands Agents SDK Templates

A collection of templates for building custom components for [Strands Agents](https://github.com/strands-agents/sdk-python).

## Available Templates

This repository provides templates for extending the Strands Agents SDK with custom components:

| Template | Description | Location |
|----------|-------------|----------|
| **Tool** | Custom tools that agents can use | [`src/`](src/) (root) |
| **Model Provider** | Custom AI model integrations | [`templates/model_provider/`](templates/model_provider/) |
| **Hook Provider** | Event callbacks for agent lifecycle | [`templates/hook_provider/`](templates/hook_provider/) |
| **Session Manager** | Conversation persistence backends | [`templates/session_manager/`](templates/session_manager/) |
| **Conversation Manager** | Conversation history management strategies | [`templates/conversation_manager/`](templates/conversation_manager/) |

## Quick Start

### Using the Tool Template (Root)

The root of this repository is a ready-to-use tool template:

```bash
# Clone the template
git clone https://github.com/mkmeral/strands-tool-template my-tool
cd my-tool

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

### Using Other Templates

Each template in the `templates/` directory is a self-contained project:

```bash
# Copy the template you need
cp -r templates/model_provider my-model-provider
cd my-model-provider

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Template Details

### 🔧 Tool Template (Root)

Create custom tools that agents can use to perform actions.

```python
from strands import Agent, tool

@tool
def my_tool(param: str) -> dict:
    """My custom tool description."""
    return {"status": "success", "content": [{"text": f"Result: {param}"}]}

agent = Agent(tools=[my_tool])
agent("Use my tool with 'hello'")
```

**Key files:**
- `src/strands_tool_yourname/your_tool.py` - Tool implementation
- `tests/test_your_tool.py` - Tests

### 🤖 Model Provider Template

Integrate custom AI models with Strands Agents.

```python
from strands import Agent
from strands_model_yourname import YourModel

model = YourModel(api_key="...", model_id="...")
agent = Agent(model=model)
agent("Hello!")
```

**Key files:**
- `src/strands_model_yourname/your_model.py` - Model implementation
- Implements: `Model` abstract class from `strands.models.model`

**What to implement:**
- `stream()` - Stream responses from your model
- `structured_output()` - Get typed outputs (optional)
- `format_request()` / `format_chunk()` - Convert between formats

### 🪝 Hook Provider Template

Add custom callbacks to agent lifecycle events.

```python
from strands import Agent
from strands_hooks_yourname import YourHookProvider

hooks = YourHookProvider(config="value")
agent = Agent(hooks=[hooks])
agent("Hello!")  # Hooks are triggered automatically
```

**Key files:**
- `src/strands_hooks_yourname/your_hooks.py` - Hook implementation
- Implements: `HookProvider` protocol from `strands.hooks.registry`

**Available events:**
- `AgentInitializedEvent` - After agent initialization
- `BeforeInvocationEvent` / `AfterInvocationEvent` - Request lifecycle
- `MessageAddedEvent` - When messages are added
- `BeforeToolCallEvent` / `AfterToolCallEvent` - Tool execution
- `BeforeModelCallEvent` / `AfterModelCallEvent` - Model inference

### 💾 Session Manager Template

Persist conversations to custom storage backends.

```python
from strands import Agent
from strands_session_yourname import YourSessionManager

session = YourSessionManager(session_id="user-123", connection_string="...")
agent = Agent(session_manager=session)
agent("Hello!")  # Conversation is persisted
```

**Key files:**
- `src/strands_session_yourname/your_session_manager.py` - Session manager
- Extends: `SessionManager` abstract class from `strands.session`

**What to implement:**
- `initialize()` - Load agent state from storage
- `append_message()` - Save new messages
- `sync_agent()` - Persist agent state
- `redact_latest_message()` - Update/redact messages

### 📜 Conversation Manager Template

Control how conversation history is managed.

```python
from strands import Agent
from strands_conversation_yourname import YourConversationManager

cm = YourConversationManager(max_messages=50)
agent = Agent(conversation_manager=cm)
agent("Hello!")  # Conversation is managed automatically
```

**Key files:**
- `src/strands_conversation_yourname/your_conversation_manager.py` - Manager
- Extends: `ConversationManager` abstract class

**What to implement:**
- `apply_management()` - Regular conversation management
- `reduce_context()` - Emergency context reduction

## Development

### Common Commands

All templates use the same development workflow:

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
ruff format

# Check linting
ruff check

# Type checking
mypy src
```

### Project Structure

Each template follows this structure:

```
template-name/
├── src/
│   └── strands_<component>_yourname/
│       ├── __init__.py
│       └── your_<component>.py
├── tests/
│   └── test_your_<component>.py
├── README.md
├── pyproject.toml
└── LICENSE
```

## Publishing to PyPI

1. Update the version in `pyproject.toml`
2. Commit your changes: `git commit -am "Release v0.1.0"`
3. Create a git tag: `git tag v0.1.0`
4. Push with tags: `git push && git push --tags`
5. Create a GitHub release from the tag
6. The GitHub Action will automatically build and publish to PyPI

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Apache 2.0 License - see [LICENSE](LICENSE) file for details.

## Links

- [Strands Agents Documentation](https://strandsagents.com/)
- [Strands Agents GitHub](https://github.com/strands-agents/sdk-python)
- [Official Tools Collection](https://github.com/strands-agents/tools)

---

Built with ❤️ for the [Strands Agents](https://github.com/strands-agents/sdk-python) community
