from core.config.src.main.config import (
    OPENAI_SDK_SYSTEM_PROMPT,
    OPENROUTER_APIKEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_MAX_TOKENS,
    OPENROUTER_MODEL,
    OPENROUTER_TEMPERATURE,
)
from core.model.src.main.agent import Agent
from core.model.src.main.provider import Provider
from core.openai.src.main.agent import OpenAIAgent

provider = Provider(
    api_key=OPENROUTER_APIKEY,
    base_url=OPENROUTER_BASE_URL,
    model=OPENROUTER_MODEL,
    max_tokens=OPENROUTER_MAX_TOKENS,
    temperature=OPENROUTER_TEMPERATURE,
    system_prompt=OPENAI_SDK_SYSTEM_PROMPT,
)

openAIAgentInstance: Agent = OpenAIAgent(provider)  # noqa: N816
