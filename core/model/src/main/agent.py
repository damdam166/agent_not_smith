"""Abstract base class for all agents."""

from abc import ABC, abstractmethod
from pathlib import Path

from core.model.src.main.provider import Provider


class Agent(ABC):
    """Defines the contract every agent must implement.

    Attributes:
        provider: Configuration dataclass with API key, model, etc.
    """

    def __init__(self, provider: Provider) -> None:
        self._provider = provider

    def get_model(self) -> str:
        """Return the model identifier configured for this agent.

        Returns:
            The model string (e.g. ``"cohere/north-mini-code:free"``).
        """
        return self._provider.model

    @abstractmethod
    def goal(self, filepath: Path) -> str:
        """Execute the agent's primary task.

        Args:
            filepath: Path to the input file.

        Returns:
            The agent's output (e.g. a summary).
        """
