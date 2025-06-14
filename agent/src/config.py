import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Configuration(BaseSettings):
    NAME: Optional[str] = "Forge"
    PORT: Optional[str] = None
    ENDPOINT: Optional[str] = None
    MAILBOX: Optional[bool] = False
    SEED: Optional[str] = None
    LLM_API_KEY: Optional[str] = None
    LLM_API_URL: Optional[str] = None
    MODEL: Optional[str] = "mistral-large-latest"
    RATE_LIMIT_CALLS: Optional[int] = 20
    RATE_LIMIT_PERIOD: Optional[int] = 60
    HOME_PATH: str
    GEM_PATH: str
    GEM_HOME: str
    RUBY_PATH: str
    NODE_PATH: str

    class Config:
        env_file = env_file = os.getenv(
            "ENV_FILE", os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        )
        validate_assignment = True


@lru_cache
def get_config() -> Configuration:
    return Configuration()
