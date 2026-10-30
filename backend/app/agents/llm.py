from dataclasses import dataclass

from app.core.config import get_settings


@dataclass
class LLMConfig:
    provider: str
    model: str


def get_llm_config() -> LLMConfig:
    settings = get_settings()
    return LLMConfig(provider=settings.llm_provider.lower(), model=settings.llm_model)
