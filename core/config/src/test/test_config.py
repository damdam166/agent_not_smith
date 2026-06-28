from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest import MonkeyPatch


class TestConfig:
    ENV_DEFAULTS: dict[str, str] = {
        "OPENROUTER_APIKEY": "test-key",
        "OPENROUTER_BASE_URL": "https://test.api/v1",
        "OPENROUTER_MODEL": "test/model:free",
        "OPENROUTER_MAX_TOKENS": "2048",
        "OPENROUTER_TEMPERATURE": "0.5",
        "OPENAI_SDK_SYSTEM_PROMPT": "test prompt",
    }

    @pytest.fixture(autouse=True)
    def _setup_env(self, monkeypatch: MonkeyPatch) -> None:
        for key, value in self.ENV_DEFAULTS.items():
            monkeypatch.setenv(key, value)
        importlib.reload(importlib.import_module("core.config.src.main.config"))

    def test_apikey(self) -> None:
        from core.config.src.main.config import OPENROUTER_APIKEY

        assert OPENROUTER_APIKEY == "test-key"

    def test_base_url(self) -> None:
        from core.config.src.main.config import OPENROUTER_BASE_URL

        assert OPENROUTER_BASE_URL == "https://test.api/v1"

    def test_model(self) -> None:
        from core.config.src.main.config import OPENROUTER_MODEL

        assert OPENROUTER_MODEL == "test/model:free"

    def test_max_tokens(self) -> None:
        from core.config.src.main.config import OPENROUTER_MAX_TOKENS

        assert OPENROUTER_MAX_TOKENS == 2048

    def test_temperature(self) -> None:
        from core.config.src.main.config import OPENROUTER_TEMPERATURE

        assert OPENROUTER_TEMPERATURE == 0.5

    def test_system_prompt(self) -> None:
        from core.config.src.main.config import OPENAI_SDK_SYSTEM_PROMPT

        assert OPENAI_SDK_SYSTEM_PROMPT == "test prompt"
