import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str | None = os.environ.get("ENVIRONMENT", None)

    DATABASE_URL: str | None = os.environ.get("DATABASE_URL", None)

    CELERY_BROKER_URL: str | None = os.environ.get("CELERY_BROKER_URL", None)
    CELERY_RESULT_BACKEND: str | None = os.environ.get("CELERY_RESULT_BACKEND", None)

    class Config:
        env_file = ".env"
        case_sensitive = True
        from_attributes = True


settings = Settings()
