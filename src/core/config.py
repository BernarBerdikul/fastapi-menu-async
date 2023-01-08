from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseSettings, PostgresDsn
from yaml import Loader


class App(BaseSettings):
    project_name: str
    description: str
    version: str
    api_doc_prefix: str
    debug: bool
    db_exclude_tables: list[str]


class Postgres(BaseSettings):
    host: str
    port: int
    dbname: str
    user: str
    password: str
    async_dsn: PostgresDsn


class Redis(BaseSettings):
    host: str
    port: int
    db: int
    encoding: str
    cache_expire_time: int
    max_connections: int


class Settings(BaseSettings):
    app: App
    postgres: Postgres
    redis: Redis


settings_path = Path(__file__).parent / 'config.yaml'
with settings_path.open('r') as f:
    yaml_settings = yaml.load(f, Loader=Loader)


@lru_cache
async def get_settings() -> Settings:
    return Settings(**yaml_settings)
