from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from types import ModuleType

    from pytest import MonkeyPatch


_MODULE_PREFIXES = ("core.config", "core.model", "core.openai", "core.data")


def _fresh_import(module_name: str) -> ModuleType:
    """Purge cached modules under ``core.*`` and do a clean import."""
    for name in list(sys.modules):
        if any(name.startswith(p) for p in _MODULE_PREFIXES):
            del sys.modules[name]
    __import__(module_name)
    return sys.modules[module_name]


class TestDataModule:
    @pytest.fixture(autouse=True)
    def _setup_env(self, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv("OPENROUTER_APIKEY", "data-module-key")
        monkeypatch.setenv("OPENROUTER_BASE_URL", "https://data-module.api/v1")
        monkeypatch.setenv("OPENROUTER_MODEL", "data/model:free")
        monkeypatch.setenv("OPENROUTER_MAX_TOKENS", "512")
        monkeypatch.setenv("OPENROUTER_TEMPERATURE", "0.0")
        monkeypatch.setenv("OPENAI_SDK_SYSTEM_PROMPT", "data prompt")

    def test_repository_instance_exists(self) -> None:
        data_module = _fresh_import("core.data.src.main.di.data_module")
        from core.data.src.main.openai_agent_repository import (
            OpenAIAgentRepository,
        )

        assert isinstance(
            data_module.openai_agent_repository_instance,
            OpenAIAgentRepository,
        )

    def test_repository_instance_has_model(self) -> None:
        data_module = _fresh_import("core.data.src.main.di.data_module")

        assert (
            data_module.openai_agent_repository_instance.get_model()
            == "data/model:free"
        )
