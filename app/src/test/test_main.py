from __future__ import annotations

import importlib
import runpy
import sys
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator

    from pytest import MonkeyPatch


@pytest.fixture(autouse=True)
def _env(monkeypatch: MonkeyPatch) -> Generator[None]:
    monkeypatch.setenv("OPENROUTER_APIKEY", "main-test-key")
    monkeypatch.setenv("OPENROUTER_BASE_URL", "https://main.api/v1")
    monkeypatch.setenv("OPENROUTER_MODEL", "main/model:free")
    monkeypatch.setenv("OPENROUTER_MAX_TOKENS", "100")
    monkeypatch.setenv("OPENROUTER_TEMPERATURE", "0.0")
    monkeypatch.setenv("OPENAI_SDK_SYSTEM_PROMPT", "")
    config = importlib.import_module("core.config.src.main.config")
    importlib.reload(config)
    openai_module = importlib.import_module("core.openai.src.main.di.openai_module")
    importlib.reload(openai_module)
    data_module = importlib.import_module("core.data.src.main.di.data_module")
    importlib.reload(data_module)
    yield


class TestMain:
    def test_main_prints_summary(self, tmp_path: Path) -> None:
        filepath = tmp_path / "test.txt"
        filepath.write_text("hello")

        with patch(
            "core.data.src.main.openai_agent_repository.OpenAIAgentRepository.summarize_file"
        ) as mock_summarize:
            mock_summarize.return_value = "mock summary output"
            from app.src.main.main import main

            testargs = ["prog", str(filepath)]
            with patch.object(sys, "argv", testargs):
                main()

            mock_summarize.assert_called_once_with(filepath)

    def test_main_exits_on_missing_file(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        from app.src.main.main import main

        missing = Path("/nonexistent/file.txt")
        testargs = ["prog", str(missing)]
        with (
            patch.object(sys, "argv", testargs),
            pytest.raises(SystemExit) as exc_info,
        ):
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error: file not found" in captured.err

    def test_main_module_runs_via_name_main(self, tmp_path: Path) -> None:
        filepath = tmp_path / "module_test.txt"
        filepath.write_text("module run")

        with (
            patch.object(sys, "argv", ["prog", str(filepath)]),
            patch(
                "core.data.src.main.openai_agent_repository.OpenAIAgentRepository.summarize_file"
            ) as mock_summarize,
        ):
            mock_summarize.return_value = "module output"
            sys.modules.pop("app.src.main.main", None)
            runpy.run_module("app.src.main.main", run_name="__main__")

            mock_summarize.assert_called_once_with(filepath)
