from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    NAME: str = "doki"
    PORT: str = "8000"
    ENDPOINT: str = "http://localhost:8000/submit"
    MAILBOX: bool = False
    SEED: Optional[str] = None
    LLM_API_KEY: Optional[str] = None
    LLM_API_URL: Optional[str] = None
    MODEL: Optional[str] = "mistral-large-latest"

    class Config:
        env_file = "../.env"
        validate_assignment = True


@lru_cache
def get_config() -> Config:
    return Config()
