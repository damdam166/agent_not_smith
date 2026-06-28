"""Data classes that describe how an agent should be configured."""

from dataclasses import dataclass


@dataclass
class Provider:
    """Aggregates all parameters required to configure an LLM agent.

    Attributes:
        api_key: Authentication token for the LLM provider.
        model: Model identifier (e.g. ``"cohere/north-mini-code:free"``).
        base_url: Base URL of the OpenAI-compatible API endpoint.
        max_tokens: Maximum number of tokens to generate.
        temperature: Sampling temperature (``0.0`` = greedy/deterministic).
        system_prompt: System-level instruction prepended before every user message.
    """

    api_key: str
    model: str
    base_url: str
    max_tokens: int
    temperature: float
    system_prompt: str
