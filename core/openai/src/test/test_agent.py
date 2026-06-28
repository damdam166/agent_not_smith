from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

from core.model.src.main.provider import Provider
from core.openai.src.main.agent import OpenAIAgent

if TYPE_CHECKING:
    pass


class TestOpenAIAgent:
    FAKE_CONTENT = "mock summary text"

    @patch("core.openai.src.main.agent.OpenAI", autospec=True)
    def test_goal_returns_content_from_response(
        self, mock_openai: MagicMock, tmp_path: Path
    ) -> None:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content=self.FAKE_CONTENT))
        ]

        provider = Provider(
            api_key="sk-test",
            model="test-model",
            base_url="https://test.api/v1",
            max_tokens=100,
            temperature=0.0,
            system_prompt="test prompt",
        )
        agent = OpenAIAgent(provider)

        filepath = tmp_path / "input.txt"
        filepath.write_text("hello world")

        result = agent.goal(filepath)
        assert result == self.FAKE_CONTENT

    @patch("core.openai.src.main.agent.OpenAI", autospec=True)
    def test_goal_sends_correct_messages(
        self, mock_openai: MagicMock, tmp_path: Path
    ) -> None:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="ok"))
        ]

        provider = Provider(
            api_key="sk-test",
            model="test-model",
            base_url="https://test.api/v1",
            max_tokens=100,
            temperature=0.0,
            system_prompt="system prompt value",
        )
        agent = OpenAIAgent(provider)

        filepath = tmp_path / "input.txt"
        filepath.write_text("file content here")

        agent.goal(filepath)

        mock_client.chat.completions.create.assert_called_once()
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        messages = call_kwargs["messages"]
        assert messages[0] == {
            "role": "system",
            "content": "system prompt value",
        }
        assert "file content here" in messages[1]["content"]

    @patch("core.openai.src.main.agent.OpenAI", autospec=True)
    def test_goal_passes_model_and_params(
        self, mock_openai: MagicMock, tmp_path: Path
    ) -> None:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="ok"))
        ]

        provider = Provider(
            api_key="sk-test",
            model="custom-model",
            base_url="https://test.api/v1",
            max_tokens=500,
            temperature=0.8,
            system_prompt="",
        )
        agent = OpenAIAgent(provider)

        filepath = tmp_path / "input.txt"
        filepath.write_text("data")

        agent.goal(filepath)

        call_kwargs = mock_client.chat.completions.create.call_args[1]
        assert call_kwargs["model"] == "custom-model"
        assert call_kwargs["max_tokens"] == 500
        assert call_kwargs["temperature"] == 0.8

    @patch("core.openai.src.main.agent.OpenAI", autospec=True)
    def test_goal_handles_empty_response(
        self, mock_openai: MagicMock, tmp_path: Path
    ) -> None:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content=None))
        ]

        provider = Provider(
            api_key="sk-test",
            model="m",
            base_url="u",
            max_tokens=1,
            temperature=0.0,
            system_prompt="",
        )
        agent = OpenAIAgent(provider)

        filepath = tmp_path / "input.txt"
        filepath.write_text("data")

        result = agent.goal(filepath)
        assert result == ""
