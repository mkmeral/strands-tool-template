# strands-hooks-yourname

> **TODO**: Replace "yourname" with your hook provider name throughout this repository

A [Strands Agents](https://github.com/strands-agents/sdk-python) hook provider for [describe purpose].

## Installation

```bash
pip install strands-hooks-yourname
```

## Usage

### Basic Usage

```python
from strands import Agent
from strands_hooks_yourname import YourHookProvider

# Create hook provider with configuration
hooks = YourHookProvider(
    config_option="value",
    enable_feature=True,
)

# Attach to agent
agent = Agent(hooks=[hooks])

# Use the agent - hooks are triggered automatically
result = agent("Hello, how are you?")
```

### Multiple Hook Providers

```python
from strands import Agent
from strands_hooks_yourname import YourHookProvider, LoggingHookProvider

agent = Agent(hooks=[
    YourHookProvider(config_option="value"),
    LoggingHookProvider(level="INFO"),
])
```

### Accessing Metrics

```python
from strands import Agent
from strands_hooks_yourname import YourHookProvider

hooks = YourHookProvider()
agent = Agent(hooks=[hooks])

# Run some requests
agent("Hello")
agent("How are you?")

# Get collected metrics
metrics = hooks.get_metrics()
print(f"Total requests: {metrics['request_count']}")
print(f"Total tokens: {metrics['total_tokens']}")

# Reset metrics
hooks.reset_metrics()
```

## Available Hook Events

The Strands SDK provides the following hook events:

| Event | Description | Timing |
|-------|-------------|--------|
| `AgentInitializedEvent` | Agent fully initialized | After construction |
| `BeforeInvocationEvent` | Before processing request | Start of `__call__`/`stream_async` |
| `AfterInvocationEvent` | After processing completes | End of `__call__`/`stream_async` |
| `MessageAddedEvent` | Message added to history | When messages are appended |
| `BeforeToolCallEvent` | Before tool execution | Before each tool runs |
| `AfterToolCallEvent` | After tool execution | After each tool completes |
| `BeforeModelCallEvent` | Before model inference | Before each model call |
| `AfterModelCallEvent` | After model inference | After each model call |

## Creating Custom Hook Providers

```python
from strands.hooks.registry import HookProvider, HookRegistry
from strands.hooks.events import BeforeInvocationEvent, AfterInvocationEvent

class MyCustomHooks(HookProvider):
    def __init__(self, setting: str = "default"):
        self.setting = setting
    
    def register_hooks(self, registry: HookRegistry, **kwargs):
        registry.add_callback(BeforeInvocationEvent, self._on_before)
        registry.add_callback(AfterInvocationEvent, self._on_after)
    
    def _on_before(self, event: BeforeInvocationEvent):
        print(f"Starting request with setting: {self.setting}")
    
    def _on_after(self, event: AfterInvocationEvent):
        print("Request completed")
```

## Modifying Events

Some events allow you to modify their properties:

### Modify Messages (BeforeInvocationEvent)

```python
def _on_before_invocation(self, event: BeforeInvocationEvent):
    # Redact sensitive content from messages
    if event.messages:
        for msg in event.messages:
            for content in msg.get("content", []):
                if "text" in content:
                    content["text"] = self._redact_pii(content["text"])
```

### Cancel Tool Calls (BeforeToolCallEvent)

```python
def _on_before_tool_call(self, event: BeforeToolCallEvent):
    tool_name = event.tool_use.get("name")
    if tool_name in self.blocked_tools:
        event.cancel_tool = f"Tool '{tool_name}' is not allowed"
```

### Retry Model Calls (AfterModelCallEvent)

```python
def _on_after_model_call(self, event: AfterModelCallEvent):
    if event.exception and "rate_limit" in str(event.exception):
        time.sleep(1)  # Wait before retry
        event.retry = True
```

## Configuration

### Environment Variables

**TODO**: Document environment variables if applicable

| Variable | Description | Default |
|----------|-------------|---------|
| `YOUR_HOOK_SETTING` | Description | `default` |

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/strands-hooks-yourname
cd strands-hooks-yourname

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
- [Hooks System in SDK](https://github.com/strands-agents/sdk-python/tree/main/src/strands/hooks)

---

Built with ❤️ for the [Strands Agents](https://github.com/strands-agents/sdk-python) community
