# strands-model-yourname

> **TODO**: Replace "yourname" with your model name throughout this repository

A [Strands Agents](https://github.com/strands-agents/sdk-python) model provider for [service/platform name].

## Installation

```bash
pip install strands-model-yourname
```

## Usage

### Basic Usage

```python
from strands import Agent
from strands_model_yourname import YourModel

# Initialize the model provider
model = YourModel(
    api_key="your-api-key",  # Or set via environment variable
    model_id="your-model-id",
)

# Create an agent with your model
agent = Agent(model=model)

# Use the agent
result = agent("Hello, how are you?")
print(result)
```

### Configuration Options

```python
from strands_model_yourname import YourModel

model = YourModel(
    api_key="your-api-key",
    model_id="your-model-id",
    max_tokens=1000,           # Maximum tokens to generate
    temperature=0.7,           # Randomness (0.0-1.0)
    top_p=0.9,                 # Nucleus sampling
    stop_sequences=["END"],    # Stop generation sequences
)
```

### With Tools

```python
from strands import Agent, tool
from strands_model_yourname import YourModel

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    return str(eval(expression))

model = YourModel(api_key="your-api-key", model_id="your-model-id")
agent = Agent(model=model, tools=[calculator])

result = agent("What is 2 + 2?")
```

### Update Configuration at Runtime

```python
model = YourModel(api_key="your-api-key", model_id="your-model-id")

# Update configuration after initialization
model.update_config(temperature=0.9, max_tokens=2000)
```

## Configuration

### Environment Variables

**TODO**: Document environment variables your model provider supports

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `YOUR_API_KEY` | API key for authentication | None | Yes |
| `YOUR_MODEL_ID` | Default model identifier | None | No |

### Example Configuration

```bash
export YOUR_API_KEY="your-api-key-here"
export YOUR_MODEL_ID="your-model-id"
```

## Supported Features

- [x] Streaming responses
- [x] Tool/function calling
- [x] Configurable parameters (temperature, max_tokens, etc.)
- [ ] Structured output (TODO)
- [ ] Vision/image input (TODO)
- [ ] [Other features]

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/strands-model-yourname
cd strands-model-yourname

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

# Fix linting issues
ruff check --fix

# Type checking
mypy src
```

## Implementing Your Model Provider

To implement your model provider, you need to:

1. **Implement the `stream` method**: This is the core method that handles communication with your model's API.

2. **Format requests**: Convert Strands message format to your API's format in `format_request`.

3. **Format responses**: Convert your API's streaming events to Strands `StreamEvent` format in `format_chunk`.

4. **(Optional) Implement `structured_output`**: If your API supports JSON mode or schema-constrained output.

### Key Concepts

- **Messages**: Strands uses a standard message format with roles (`user`, `assistant`) and content blocks (`text`, `image`, `toolUse`, `toolResult`).

- **StreamEvents**: Your model must yield events in the Strands format:
  - `messageStart`: Start of assistant response
  - `contentBlockStart`: Start of a content block
  - `contentBlockDelta`: Incremental content
  - `contentBlockStop`: End of content block
  - `messageStop`: End of message with stop reason
  - `metadata`: Usage statistics

- **Tool Calling**: If your model supports function calling, convert tool specs and handle tool use responses.

## Publishing to PyPI

### Setup (One-time)

1. Create a PyPI account at https://pypi.org/
2. Generate an API token at https://pypi.org/manage/account/token/
3. Add the token as a GitHub secret named `PYPI_API_TOKEN`

### Release Process

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
- [Model Providers in SDK](https://github.com/strands-agents/sdk-python/tree/main/src/strands/models)

---

Built with ❤️ for the [Strands Agents](https://github.com/strands-agents/sdk-python) community
