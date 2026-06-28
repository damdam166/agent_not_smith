from dataclasses import fields

from core.model.src.main.provider import Provider


class TestProvider:
    def test_constructor_sets_all_fields(self) -> None:
        provider = Provider(
            api_key="key-123",
            model="gpt-4",
            base_url="https://api.openai.com/v1",
            max_tokens=4096,
            temperature=0.7,
            system_prompt="You are helpful.",
        )
        assert provider.api_key == "key-123"
        assert provider.model == "gpt-4"
        assert provider.base_url == "https://api.openai.com/v1"
        assert provider.max_tokens == 4096
        assert provider.temperature == 0.7
        assert provider.system_prompt == "You are helpful."

    def test_is_dataclass(self) -> None:
        assert fields(Provider)

    def test_default_temperature_matches_config_default(self) -> None:
        p = Provider(
            api_key="k",
            model="m",
            base_url="u",
            max_tokens=1,
            temperature=0.0,
            system_prompt="",
        )
        assert p.temperature == 0.0
