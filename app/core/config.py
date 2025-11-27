from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    ENVIRONMENT: Literal["development", "production"] = "development"
    PROJECT_NAME: str = "nava"
    VERSION: str = "0.1.0"

    OPENAI_API_KEY: str

    WEBSOCKET_MAX_SIZE: int = 10_000_000
    LOG_LEVEL: str = "DEBUG"

    # JWT + AUTH
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days

    # DATABASE
    DATABASE_URL: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


settings = Settings()
