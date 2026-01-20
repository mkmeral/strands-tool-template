# strands-tool-yourname

> **TODO**: Replace "yourname" with your package name throughout this repository

A [Strands Agents](https://github.com/strands-agents/sdk-python) package providing custom components.

## Installation

```bash
pip install strands-tool-yourname
```

## Components

This package includes templates for all major Strands SDK extension points:

### Tool

```python
from strands import Agent
from strands_tool_yourname import your_tool

agent = Agent(tools=[your_tool])
agent("Use my tool")
```

### Model Provider

```python
from strands import Agent
from strands_tool_yourname import YourModel

model = YourModel(api_key="your-api-key", model_id="your-model-id")
agent = Agent(model=model)
agent("Hello!")
```

### Hook Provider

```python
from strands import Agent
from strands_tool_yourname import YourHookProvider

hooks = YourHookProvider(config_option="value")
agent = Agent(hooks=[hooks])
agent("Hello!")  # Hooks triggered automatically
```

### Session Manager

```python
from strands import Agent
from strands_tool_yourname import YourSessionManager

session = YourSessionManager(session_id="my-session")
agent = Agent(session_manager=session)
agent("Hello!")  # Conversation persisted
```

### Conversation Manager

```python
from strands import Agent
from strands_tool_yourname import YourConversationManager

cm = YourConversationManager(max_messages=50)
agent = Agent(conversation_manager=cm)
agent("Hello!")  # History managed automatically
```

## Component Files

| Component | File | Base Class/Interface |
|-----------|------|---------------------|
| Tool | `your_tool.py` | `@tool` decorator |
| Model Provider | `your_model.py` | `strands.models.model.Model` |
| Hook Provider | `your_hook_provider.py` | `strands.hooks.registry.HookProvider` |
| Session Manager | `your_session_manager.py` | `strands.session.SessionManager` |
| Conversation Manager | `your_conversation_manager.py` | `strands.agent.conversation_manager.ConversationManager` |

## Development

### Setup

```bash
git clone https://github.com/yourusername/strands-tool-yourname
cd strands-tool-yourname
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Linting and Formatting

```bash
ruff format
ruff check
mypy src
```

## Customization

Each component file contains TODO comments indicating what needs to be customized:

1. **Tool** (`your_tool.py`): Implement your tool's logic in the function body
2. **Model Provider** (`your_model.py`): Implement `stream()` method with your API
3. **Hook Provider** (`your_hook_provider.py`): Implement callbacks for events you need
4. **Session Manager** (`your_session_manager.py`): Implement storage operations
5. **Conversation Manager** (`your_conversation_manager.py`): Implement your management strategy

## Publishing to PyPI

1. Update the version in `pyproject.toml`
2. Commit: `git commit -am "Release v0.1.0"`
3. Tag: `git tag v0.1.0`
4. Push: `git push && git push --tags`
5. Create a GitHub release

## License

Apache 2.0 License - see [LICENSE](LICENSE) file for details.

## Links

- [Strands Agents Documentation](https://strandsagents.com/)
- [Strands Agents GitHub](https://github.com/strands-agents/sdk-python)

---

Built with ❤️ for the [Strands Agents](https://github.com/strands-agents/sdk-python) community
