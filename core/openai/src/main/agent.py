from pathlib import Path

from openai import OpenAI

from core.model.src.main.agent import Agent
from core.model.src.main.provider import Provider


class OpenAIAgent(Agent):
    def __init__(self, provider: Provider) -> None:
        super().__init__(provider)
        self._client = OpenAI(
            base_url=provider.base_url,
            api_key=provider.api_key,
        )

    def goal(self, filepath: Path) -> str:
        content = filepath.read_text(encoding="utf-8")
        response = self._client.chat.completions.create(
            model=self._provider.model,
            messages=[
                {"role": "system", "content": self._provider.system_prompt},
                {
                    "role": "user",
                    "content": f"Summarize the following file concisely:\n\n{content}",
                },
            ],
            max_tokens=self._provider.max_tokens,
            temperature=self._provider.temperature,
        )
        return response.choices[0].message.content or ""
