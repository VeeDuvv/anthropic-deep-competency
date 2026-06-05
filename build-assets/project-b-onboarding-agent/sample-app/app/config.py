"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "TaskFlow API"
    debug: bool = False
    database_url: str = "sqlite:///./taskflow.db"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "change-me-in-production-use-openssl-rand-hex-32"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    allowed_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_prefix": "TASKFLOW_"}


settings = Settings()
