from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import BaseSettings, RedisDsn

basedir = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    REDIS_URL: RedisDsn

    #  environment variables will always take priority over values loaded from a dotenv file
    class Config:
        env_file = f'{basedir / ".env"}'


@lru_cache()
def get_settings(**kwargs: Any) -> Settings:
    return Settings(**kwargs)
