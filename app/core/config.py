from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    ENVIRONMENT: Literal["development", "production"] = "development"
    PROJECT_NAME: str = "nava"
    VERSION: str = "0.1.0"

    OPENAI_API_KEY: str

    WEBSOCKET_MAX_SIZE: int = 10_000_000

    LOG_LEVEL: str = "DEBUG"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


settings = Settings()