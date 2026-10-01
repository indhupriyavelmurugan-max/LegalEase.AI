from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    gemini_api_key: str = Field(
        default="",
        validation_alias="GEMINI_API_KEY"
    )

    gemini_model: str = Field(
        default="gemini-2.5-flash",
        validation_alias="GEMINI_MODEL"
    )

    backend_url: str = Field(
        default="http://127.0.0.1:8000",
        validation_alias="BACKEND_URL"
    )

    app_env: str = Field(
        default="development",
        validation_alias="APP_ENV"
    )

    max_document_chars: int = Field(
        default=30000,
        validation_alias="MAX_DOCUMENT_CHARS"
    )

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def demo_mode(self) -> bool:

        return not bool(
            self.gemini_api_key.strip()
        )


@lru_cache
def get_settings() -> Settings:

    return Settings()