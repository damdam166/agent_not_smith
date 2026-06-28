# Architecture

## Overview

This project is a **modular, extensible file summarizer** that uses **OpenRouter** as the LLM provider and the **OpenAI Python SDK** for agent creation. The design follows a layered architecture with dependency injection to keep each layer decoupled and testable.

## Why OpenRouter?

**OpenRouter** provides a unified API for 300+ models, including **free models** (e.g. `cohere/north-mini-code:free`) that cost $0 per request. This lets the agent run without any paid subscription. Key features:

- **Free tier** — many models available at zero cost
- **OpenAI-compatible** — works with the OpenAI Python SDK by just swapping the base URL
- **No lock-in** — switch models by changing a single env var
- **Usage tracking** — per-request token counts and costs via the `/key` and `/generation` endpoints

## Why OpenAI SDK (not LangChain)?

The **OpenAI Python SDK** was chosen over LangChain because:

| Factor | OpenAI SDK | LangChain |
|---|---|---|
| Lines of code | ~10 per call | ~30+ for same task |
| Dependencies | 1 package | 15+ sub-packages |
| Learning curve | Minimal | Significant |
| Transparency | Direct API control | Abstracted behind chains |
| Best for | Simple/medium agents | Multi-step RAG pipelines |

The project's current scope (single file summarization) doesn't benefit from LangChain's abstractions. If RAG or multi-document flows are added later, LangChain can be introduced as a datasource layer without changing the agent core.

## Layers

### 1. Config Layer (`core/config/src/main/config.py`)

Loads `.env` via `python-dotenv` once at import time. Exports typed constants (`OPENROUTER_APIKEY`, `OPENROUTER_MODEL`, `OPENAI_SDK_SYSTEM_PROMPT`, etc.).

### 2. Model Layer (`core/model/src/main/`)

- **`provider.py`** — `Provider` dataclass holding all agent configuration (api_key, model, base_url, max_tokens, temperature, system_prompt).
- **`agent.py`** — `Agent` abstract base class defining the contract: `goal(filepath) → str` and `get_model() → str`.

### 3. Agent Layer (`core/openai/src/main/`)

- **`agent.py`** — `OpenAIAgent(Agent)` concrete implementation. Uses the OpenAI SDK pointed at OpenRouter's base URL. Sends a system prompt + user message, returns the completion.
- **`di/openai_module.py`** — Wires a `Provider` from config, instantiates `OpenAIAgent`, exports `openAIAgentInstance` as a singleton.

### 4. Repository Layer (`core/data/src/main/`)

- **`openai_agent_repository.py`** — `OpenAIAgentRepository` wraps any `Agent`-compatible object behind a simple interface (`summarize_file`, `get_model`).
- **`di/data_module.py`** — Exports `OpenAIAgentRepositoryInstance` singleton.

### 5. App Layer (`app/src/main/main.py`)

CLI entry point that parses arguments, imports the repository singleton, calls `summarize_file()`, and prints the result.

## Extension Points

| What | How |
|---|---|
| New LLM provider | Create `core/<provider>/src/main/agent.py` extending `Agent`, add config vars |
| New datasource | Create a datasource loader (e.g. LangChain document loader), feed content into the existing agent |
| Analytics | Use OpenRouter's `/generation` endpoint with the `id` from each completion response to track per-call costs |

## Layer Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     app/src/main                        │
│                   (CLI entry point)                     │
├─────────────────────────────────────────────────────────┤
│                 core/data/src/main                      │
│              (Repository — wraps Agent)                 │
├─────────────────────────────────────────────────────────┤
│     ┌──────────────────┬──────────────────────┐         │
│     │ core/openai/     │ core/config/         │         │
│     │ (Agent impl)     │ (env vars)           │         │
│     └──────────────────┴──────────────────────┘         │
├─────────────────────────────────────────────────────────┤
│                 core/model/src/main                     │
│           (Provider dataclass + Agent ABC)              │
└─────────────────────────────────────────────────────────┘
```
