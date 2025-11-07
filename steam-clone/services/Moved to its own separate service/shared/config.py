"""Centralised configuration for Steam Clone services."""
from functools import lru_cache
from typing import List, Union

from pydantic import BaseSettings, Field, field_validator


class Settings(BaseSettings):
    """Application configuration shared across microservices."""

    # Security
    SECRET_KEY: str = Field(
        "dev-secret-key-change-me",
        description="Secret key used for signing JWT access tokens.",
    )
    JWT_ALGORITHM: str = Field("HS256", description="Algorithm used for JWT encoding.")

    # Frontend integration / CORS
    ALLOWED_ORIGINS: List[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5173",
        ],
        description=(
            "List of frontend origins allowed to make cross-origin requests to the API. "
            "By default development ports for Create React App and Vite are enabled."
        ),
    )

    # Service ports – keep defaults aligned with docker-compose expectations
    USER_SERVICE_PORT: int = 8001
    GAME_CATALOG_SERVICE_PORT: int = 8002
    REVIEW_SERVICE_PORT: int = 8003
    SHOPPING_SERVICE_PORT: int = 8004
    PURCHASE_SERVICE_PORT: int = 8005
    PAYMENT_SERVICE_SERVICE_PORT: int = 8006
    ONLINE_SERVICE_SERVICE_PORT: int = 8007
    SOCIAL_SERVICE_SERVICE_PORT: int = 8008
    NOTIFICATION_SERVICE_SERVICE_PORT: int = 8009
    RECOMMENDATION_SERVICE_SERVICE_PORT: int = 8010
    ACHIEVEMENT_SERVICE_SERVICE_PORT: int = 8011
    MONITORING_SERVICE_SERVICE_PORT: int = 8012

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def _split_origins(cls, value: Union[str, List[str]]) -> List[str]:
        """Allow comma separated strings or JSON lists for origins."""
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance."""

    return Settings()


settings = get_settings()
