from pathlib import Path
from unittest.mock import create_autospec

from core.data.src.main.openai_agent_repository import OpenAIAgentRepository
from core.model.src.main.agent import Agent


class TestOpenAIAgentRepository:
    def test_summarize_file_delegates_to_agent(self, tmp_path: Path) -> None:
        mock_agent = create_autospec(Agent, instance=True)
        mock_agent.goal.return_value = "mock summary"

        repo = OpenAIAgentRepository(agent=mock_agent)
        filepath = tmp_path / "test.txt"
        filepath.write_text("content")

        result = repo.summarize_file(filepath)

        assert result == "mock summary"
        mock_agent.goal.assert_called_once_with(filepath)

    def test_get_model_delegates_to_agent(self) -> None:
        mock_agent = create_autospec(Agent, instance=True)
        mock_agent.get_model.return_value = "test-model"

        repo = OpenAIAgentRepository(agent=mock_agent)
        result = repo.get_model()

        assert result == "test-model"
        mock_agent.get_model.assert_called_once()

    def test_default_agent_is_wired(self) -> None:
        repo = OpenAIAgentRepository()
        assert repo._agent is not None
        assert callable(repo._agent.goal)
