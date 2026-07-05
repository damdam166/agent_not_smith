# Agent

A modular, extensible file summarizer powered by **OpenRouter** (free LLM models) and the **OpenAI Python SDK**.

## Quick Start

```bash
cp .env.example .env        # edit .env and set OPENROUTER_APIKEY
uv sync
uv run python -m app.src.main.main README.md
```

## Prerequisites

- **Python >= 3.14**
- **uv** (install: `curl -fsSL https://astral.sh/uv/install.sh | sh`)

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENROUTER_APIKEY` | Yes | — | OpenRouter API key |
| `OPENROUTER_BASE_URL` | No | `https://openrouter.ai/api/v1` | API endpoint |
| `OPENROUTER_MODEL` | No | `cohere/north-mini-code:free` | Model to use |
| `OPENROUTER_MAX_TOKENS` | No | `4096` | Max tokens in response |
| `OPENROUTER_TEMPERATURE` | No | `0.0` | Sampling temperature |
| `OPENAI_SDK_SYSTEM_PROMPT` | No | `"You are a helpful assistant."` | System prompt |

## Usage

```bash
# Summarize a file
uv run agent path/to/file.txt
```

## Docker

The agent routes all traffic through a **squid** container that only allows outbound connections to `openrouter.ai:443`. All other destinations are blocked at the proxy level.

```bash
# Create an input directory with the file to summarise
mkdir -p input
cp README.md input/myfile.txt

# Build both containers (proxy + agent)
OPENROUTER_APIKEY="sk-or-v1-..." docker compose build

# Or to run a single file non-interactively:
OPENROUTER_APIKEY="sk-or-v1-..." \
  docker compose run --rm agent /input/myfile.txt
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full breakdown.

```
app/src/main/main.py
  → data/src/main/di/data_module.py      (singleton repository)
    → openai/src/main/di/openai_module.py (wires Provider → OpenAIAgent)
      → config/src/main/config.py         (env vars)
      → model/src/main/provider.py        (dataclass)
      → openai/src/main/agent.py          (OpenAIAgent)
```

## Project Structure

| Directory | Purpose |
|---|---|
| `core/config/` | Env variable loading and typed constants |
| `core/model/` | Data classes (`Provider`) and abstract contracts (`Agent`) |
| `core/openai/` | OpenAI/OpenRouter agent implementation |
| `core/data/` | Repository layer wrapping agents |
| `app/` | CLI entry point |
| `*/src/test/` | Co-located unit tests for each component |

## Development

```bash
# Install dev dependencies
uv sync --group dev

# Run tests
uv run pytest

# Format code
uv run black .

# Lint
uv run ruff check .

# Type check
uv run mypy .
```

## TODO

| Item | Description | Status |
|---|---|---|
| Docker agents | Support running multiple isolated agents in separate containers | ❌ |
| LangChain datasource | Integrate LangChain document loaders as an alternative datasource | ❌ |
| OpenRouter analytics | Explore usage analytics (cost per model, token tracking, generation lookup) | ❌ |

### EOF

