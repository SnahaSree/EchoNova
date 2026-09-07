from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    project_name: str = Field(default="EchoNova")
    environment: str = Field(default="development")

    mongodb_uri: str
    database_name: str = Field(default="echonova")

    jwt_secret_key: str
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30, gt=0)

    cors_origins: str = Field(default="http://localhost:5173")

    ai_api_key: str = Field(default="")

    log_level: str = Field(default="INFO")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Get application settings."""
    return Settings()