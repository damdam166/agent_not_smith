from pathlib import Path

import pytest

from core.model.src.main.agent import Agent
from core.model.src.main.provider import Provider


class TestAgent:
    def test_abc_cannot_be_instantiated(self) -> None:
        with pytest.raises(TypeError):
            Agent(  # type: ignore[abstract]
                provider=Provider(
                    api_key="k",
                    model="m",
                    base_url="u",
                    max_tokens=1,
                    temperature=0.0,
                    system_prompt="",
                )
            )

    def test_subclass_must_implement_goal(self) -> None:
        class MissingGoal(Agent):
            pass

        with pytest.raises(TypeError):
            MissingGoal(  # type: ignore[abstract]
                provider=Provider(
                    api_key="k",
                    model="m",
                    base_url="u",
                    max_tokens=1,
                    temperature=0.0,
                    system_prompt="",
                )
            )

    def test_get_model_returns_provider_model(self) -> None:
        class ConcreteAgent(Agent):
            def goal(self, filepath: Path) -> str:
                return "done"

        agent = ConcreteAgent(
            provider=Provider(
                api_key="k",
                model="test-model",
                base_url="u",
                max_tokens=1,
                temperature=0.0,
                system_prompt="",
            )
        )
        assert agent.get_model() == "test-model"
