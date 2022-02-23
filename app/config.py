import logging
import os
from functools import lru_cache

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT")
    testing: bool = os.getenv("TESTING")
    home_url: str = os.getenv("HOME_URL")


@lru_cache()
def get_settings() -> BaseSettings:
    return Settings()
