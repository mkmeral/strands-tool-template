# Strands Template

This template helps you build and publish custom components for [Strands Agents](https://github.com/strands-agents/sdk-python). Whether you're creating a new tool, model provider, or session manager, this repo gives you a starting point with the right structure and conventions.

## Getting started

### 1. Create your repository

Click "Use this template" on GitHub to create your own repository. Then clone it locally:

```bash
git clone https://github.com/yourusername/your-repo-name
cd your-repo-name
```

### 2. Run the setup script

The setup script customizes the template for your project. It renames files, updates imports, and configures `pyproject.toml` with your details.

```bash
python setup_template.py
```

You'll be prompted for:

- **Package name** — A short identifier like `amazon`, `slack`, or `redis`. This becomes your module name (`strands_amazon`) and PyPI package name (`strands-amazon`).
- **Author info** — Your name, email, and GitHub username for `pyproject.toml`.
- **Description** — A one-line description of your package.

### 3. Install dependencies

```bash
pip install -e ".[dev]"
```

## What's in this template

The template includes skeleton implementations for all major Strands extension points.

| File | Component | Purpose |
|------|-----------|---------|
| `tool.py` | Tool | Add capabilities to agents using the `@tool` decorator |
| `model.py` | Model provider | Integrate custom LLM APIs |
| `hook_provider.py` | Hook provider | React to agent lifecycle events |
| `session_manager.py` | Session manager | Persist conversations across restarts |
| `conversation_manager.py` | Conversation manager | Control how conversation history is managed |

### Keep what you need, delete the rest

Most packages only need one or two components. Delete the files you don't need and remove their exports from `__init__.py`.

For example, if you're building a tool package:

1. Keep `tool.py` and `test_tool.py`
2. Delete the other component files
3. Update `__init__.py` to only export your tool

## Implementing your components

Each file contains a minimal skeleton. Here's what to implement:

### Tools

Tools let agents interact with external systems and perform actions. Implement your logic inside the decorated function and return a result dict.

- [Creating custom tools](https://strandsagents.com/latest/user-guide/concepts/tools/custom-tools/) — Documentation
- [Official tools repository](https://github.com/strands-agents/tools) — Implementation examples

### Model providers

Model providers connect agents to LLM APIs. Implement the `stream()` method to receive messages and yield streaming events.

- [Custom providers](https://strandsagents.com/latest/user-guide/concepts/model-providers/custom_model_provider/) — Documentation
- [Anthropic provider](https://github.com/strands-agents/sdk-python/blob/main/src/strands/models/anthropic.py) — Implementation example

### Hook providers

Hooks let you react to agent lifecycle events like invocations, tool calls, and model calls. Register callbacks for the events you care about.

- [Hooks](https://strandsagents.com/latest/user-guide/concepts/agents/hooks/) — Documentation

### Session managers

Session managers persist conversations to external storage, enabling conversations to resume after restarts or be shared across instances.

- [Session management](https://strandsagents.com/latest/user-guide/concepts/agents/session-management/) — Documentation
- [File session manager](https://github.com/strands-agents/sdk-python/blob/main/src/strands/session/file_session_manager.py) — Implementation example

### Conversation managers

Conversation managers control how message history grows over time. They handle trimming old messages or summarizing context to stay within model limits.

- [Conversation management](https://strandsagents.com/latest/user-guide/concepts/agents/conversation-management/) — Documentation
- [Sliding window manager](https://github.com/strands-agents/sdk-python/blob/main/src/strands/agent/conversation_manager/sliding_window_conversation_manager.py) — Implementation example

## Testing

Run all checks (format, lint, typecheck, test):

```bash
hatch run prepare
```

Or run them individually:

```bash
hatch run test        # Run tests
hatch run lint        # Run linter
hatch run typecheck   # Run type checker
hatch run format      # Format code
```

## Publishing to PyPI

You can publish manually or through GitHub Actions.

### Option 1: GitHub release (recommended)

The included workflow automatically publishes to PyPI when you create a GitHub release. Version is derived from the git tag automatically.

1. Create a release on GitHub with a tag like `v0.1.0`
2. The workflow runs checks, builds, and publishes

To enable this, configure PyPI trusted publishing:

1. Go to PyPI → Your projects → Publishing
2. Add a new pending publisher with your GitHub repo details
3. Set environment name to `pypi`

### Option 2: Manual publish

```bash
hatch build
pip install twine
twine upload dist/*
```

## Naming conventions

Follow these conventions so your package fits the Strands ecosystem:

| Item | Convention | Example |
|------|------------|---------|
| PyPI package | `strands-{name}` | `strands-amazon` |
| Python module | `strands_{name}` | `strands_amazon` |
| Model class | `{Name}Model` | `AmazonModel` |
| Session manager | `{Name}SessionManager` | `RedisSessionManager` |
| Conversation manager | `{Name}ConversationManager` | `SummarizingConversationManager` |
| Hook provider | `{Name}HookProvider` | `TelemetryHookProvider` |
| Tool function | `{descriptive_name}` | `search_web`, `send_email` |

## Get featured

Help others discover your package by adding the `strands-agents` topic to your GitHub repository. This makes it easier for the community to find Strands extensions.

To add topics: go to your repo → click the ⚙️ gear next to "About" → add `strands-agents` and other relevant topics.

You can also submit your package to be featured on the Strands website. See [Get Featured](https://strandsagents.com/latest/documentation/docs/community/get-featured/) for details.

## Resources

- [Strands Agents documentation](https://strandsagents.com/)
- [SDK Python repository](https://github.com/strands-agents/sdk-python)
- [Official tools repository](https://github.com/strands-agents/tools)

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.
