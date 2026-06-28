# Project Structure

```
agent/
├── pyproject.toml                           # Project config (openai + python-dotenv)
├── .env                                     # Local env vars (gitignored)
├── .env.example                             # Template for .env
├── Dockerfile                               # Container build
├── AGENTS.md                                # This file
├── README.md
├── openrouter/
│   ├── openrouter_test_apikey.sh            # Quick API key test
│   └── openrouter_get_apikey_usage.sh       # Check credits usage
├── core/
│   ├── config/src/main/config.py            # Canonical config, wraps dotenv
│   ├── model/src/main/
│   │   ├── provider.py                      # Provider dataclass (api_key, model, ...)
│   │   └── agent.py                         # Abstract Agent ABC with goal() + get_model()
│   ├── openai/src/main/
│   │   ├── agent.py                         # OpenAIAgent(Agent) – concrete implementation
│   │   └── di/openai_module.py              # DI module: wires Provider → OpenAIAgent
│   └── data/src/main/
│       ├── openai_agent_repository.py       # Repository wrapping any Agent
│       └── di/data_module.py                # DI module: exposes singleton repository
├── app/src/main/main.py                     # CLI entry point
├── core/config/src/test/                    # Config unit tests
├── core/model/src/test/                     # Model unit tests
├── core/openai/src/test/                    # OpenAI agent unit tests
├── core/data/src/test/                      # Repository unit tests
└── app/src/test/                            # CLI unit tests
```

# Architecture & Data Flow

```
app/src/main/main.py
    ↓  (imports singleton)
core/data/src/main/di/data_module.py       openai_agent_repository_instance
    ↓  (imports singleton)
core/openai/src/main/di/openai_module.py   OpenAIAgentInstance
    ↓  (reads config)
core/config/src/main/config.py              OPENROUTER_APIKEY, OPENAI_SDK_SYSTEM_PROMPT...
    ↓  (builds)
core/model/src/main/Provider.py             Provider(api_key=..., model=...)
    ↓  (passed to)
core/openai/src/main/agent.py               OpenAIAgent(provider) → goal(filepath)
    ↓  (delegates)
core/model/src/main/Agent.py                Agent ABC (goal + get_model)
```

# Layers

| Layer | Package | Responsibility |
|---|---|---|
| **Config** | `core.config.src.main` | Load `.env`, export typed constants |
| **Model** | `core.model.src.main` | Dataclass (`Provider`) + abstract contract (`Agent`) |
| **Agent** | `core.openai.src.main` | LLM interaction logic |
| **DI** | `core.openai.src.main.di` | Wire provider → agent singleton |
| **Repository** | `core.data.src.main` | High-level wrapper around an `Agent` |
| **DI** | `core.data.src.main.di` | Expose singleton repository |
| **App** | `app.src.main` | CLI entry point, user-facing |

# Conventions

- **All imports use full package paths** (e.g. `from core.model.src.main.provider import Provider`)
- **Dataclasses for data** — no business logic in model layer
- **Agent ABC** — all agents extend `Agent` and implement `goal(filepath)`
- **Config is loaded once** at import time via `dotenv.load_dotenv()` in `core/config/src/main/config.py`
- **Python >= 3.14** required (uses `X | None` syntax)
- **Edit `core/config/src/main/config.py`** to add/change env vars
- **Tests** — `pytest` (`uv run pytest`)
- **Formatter** — `black` (`uv run black .`)
- **Linter** — `ruff` (`uv run ruff check .`)
- **Type checker** — `mypy` (`uv run mypy .`)

# Adding a new provider (e.g. Anthropic)

1. Create `core/anthropic/src/main/agent.py` extending `Agent` and implementing `goal()`
2. Add provider-specific config to `core/config/src/main/config.py`
3. Optionally add a DI module at `core/anthropic/src/main/di/`
4. Create a matching repository or reuse `OpenAIAgentRepository` by injecting the new agent

# Running

```bash
uv sync
uv run python -m app.src.main.main <filepath>
```

# Testing the API key

```bash
./openrouter/openrouter_test_apikey.sh
```

Use shell scripts in `openrouter/` to verify the API key works before running the agent.
