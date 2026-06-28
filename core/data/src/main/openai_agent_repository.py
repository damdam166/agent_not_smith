"""Repository layer for OpenAI-powered agent interactions."""

from pathlib import Path

from core.model.src.main.agent import Agent
from core.openai.src.main.di.openai_module import openAIAgentInstance


class OpenAIAgentRepository:
    """Provides high-level access to an :class:`~core.model.src.main.Agent.Agent`.

    Args:
        agent: The agent to delegate to. Defaults to the globally
            configured ``OpenAIAgent`` singleton from the DI module.
    """

    def __init__(self, agent: Agent = openAIAgentInstance) -> None:
        self._agent = agent

    def summarize_file(self, filepath: Path) -> str:
        """Summarise the contents of a file.

        Args:
            filepath: Path to the file to summarise.

        Returns:
            The agent's summary as a string.
        """
        return self._agent.goal(filepath)

    def get_model(self) -> str:
        """Return the model identifier currently used by the wrapped agent.

        Returns:
            Model string (e.g. ``"cohere/north-mini-code:free"``).
        """
        return self._agent.get_model()
