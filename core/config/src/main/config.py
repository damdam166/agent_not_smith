"""Application configuration loaded from environment variables.

This module wraps python-dotenv to load a ``.env`` file and expose typed
configuration constants for the rest of the application.  Every public
name has a corresponding ``OPENROUTER_*`` environment variable.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# <Openrouter>
OPENROUTER_APIKEY: str = os.environ.get("OPENROUTER_APIKEY", "")
"""OpenRouter API key.  Required – no default."""

OPENROUTER_BASE_URL: str = os.environ.get(
    "OPENROUTER_BASE_URL",
    "",
)
"""Base URL of the API endpoint."""

OPENROUTER_MODEL: str = os.environ.get(
    "OPENROUTER_MODEL",
    "",
)
"""Default model identifier to use for completions."""

OPENROUTER_MAX_TOKENS: int = int(
    os.environ.get("OPENROUTER_MAX_TOKENS", "0"),
)
"""Maximum number of tokens in the generated response."""

OPENROUTER_TEMPERATURE: float = float(
    os.environ.get("OPENROUTER_TEMPERATURE", "0.0"),
)
"""Sampling temperature (0.0 = deterministic)."""
# </Openrouter>

# <Openai>
OPENAI_SDK_SYSTEM_PROMPT: str = os.environ.get(
    "OPENAI_SDK_SYSTEM_PROMPT",
    "",
)
"""System prompt prepended to every conversation."""
# </Openai>
