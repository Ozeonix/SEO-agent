from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'SEO & Ads Optimization Agent'
    env: str = 'dev'
    backend_cors_origins: list[str] = Field(default_factory=lambda: ['http://localhost:5173'])

    database_url: str = 'sqlite:///./seo_agent.db'

    llm_provider: str = 'openai'
    llm_model: str = 'gpt-4o-mini'

    demo_mode: bool = True
    approval_default_mode: str = 'manual'

    scheduler_daily_cron: str = '0 6 * * *'
    scheduler_weekly_cron: str = '0 7 * * 1'

    oauth_token_encryption_key: str = 'change-me-with-32-char-key'


@lru_cache
def get_settings() -> Settings:
    return Settings()
