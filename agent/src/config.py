from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Configuration(BaseSettings):
    NAME: str = "Doki"
    PORT: str = "5000"
    ENDPOINT: str = "https://forge-api.daimones.xyz/submit"
    MAILBOX: bool = False
    SEED: Optional[str] = None
    LLM_API_KEY: Optional[str] = None
    LLM_API_URL: Optional[str] = None
    MODEL: Optional[str] = "mistral-large-latest"

    class Config:
        env_file = "../.env"
        validate_assignment = True


@lru_cache
def get_config() -> Configuration:
    return Configuration()
