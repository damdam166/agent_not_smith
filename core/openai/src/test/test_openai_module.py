from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest import MonkeyPatch


class TestOpenaiModule:
    ENV_VARS: dict[str, str] = {
        "OPENROUTER_APIKEY": "di-test-key",
        "OPENROUTER_BASE_URL": "https://di-test.api/v1",
        "OPENROUTER_MODEL": "di/model:free",
        "OPENROUTER_MAX_TOKENS": "1024",
        "OPENROUTER_TEMPERATURE": "0.3",
        "OPENAI_SDK_SYSTEM_PROMPT": "di system prompt",
    }

    @pytest.fixture(autouse=True)
    def _setup_env(self, monkeypatch: MonkeyPatch) -> None:
        for key, value in self.ENV_VARS.items():
            monkeypatch.setenv(key, value)

    def test_openai_agent_instance_is_agent(self) -> None:
        config = importlib.import_module("core.config.src.main.config")
        importlib.reload(config)
        module = importlib.import_module("core.openai.src.main.di.openai_module")
        importlib.reload(module)
        from core.model.src.main.agent import Agent

        assert isinstance(module.OpenAIAgentInstance, Agent)

    def test_openai_agent_instance_delegates_model(self) -> None:
        config = importlib.import_module("core.config.src.main.config")
        importlib.reload(config)
        module = importlib.import_module("core.openai.src.main.di.openai_module")
        importlib.reload(module)

        assert module.OpenAIAgentInstance.get_model() == "di/model:free"
