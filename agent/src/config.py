import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Configuration(BaseSettings):
    NAME: Optional[str] = "Doki"
    PORT: Optional[str] = None
    ENDPOINT: Optional[str] = None
    MAILBOX: Optional[bool] = False
    SEED: Optional[str] = None
    LLM_API_KEY: Optional[str] = None
    LLM_API_URL: Optional[str] = None
    MODEL: Optional[str] = "mistral-large-latest"
    COMPOSER_HOME_DIR: str

    class Config:
        env_file = env_file = os.getenv(
            "ENV_FILE", os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        )
        validate_assignment = True


@lru_cache
def get_config() -> Configuration:
    return Configuration()
