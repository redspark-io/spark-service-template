import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str | None = os.environ.get("ENVIRONMENT", None)

    DATABASE_URL: str = os.environ.get("DATABASE_URL", "")

    CELERY_BROKER_URL: str | None = os.environ.get("CELERY_BROKER_URL", None)
    CELERY_RESULT_BACKEND: str | None = os.environ.get("CELERY_RESULT_BACKEND", None)

    HOST_URL: str = "https://c8c1-2804-7f0-6540-737-a5a7-9835-70c0-3dd.ngrok-free.app"

    REGISTRY_PASSWORD: str | None = os.environ.get("REGISTRY_PASSWORD", None)
    AZURE_CREDENTIALS: str | None = os.environ.get("AZURE_CREDENTIALS", None)

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, from_attributes=True
    )


settings = Settings()
