from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path

ENV_FILE = Path(__file__).resolve().parent / ".env"


class Settings(BaseSettings):
    app_name: str = "Attendomatic"
    database_url: str
    metadata_json_response: str
    scalekit_environment_url: str
    scalekit_client_id: str
    scalekit_client_secret: str
    scalekit_resource_metadata_url: str
    scalekit_audience_name: str = ""
    scalekit_resource_name: str = ""
    model_config = SettingsConfigDict(env_file=ENV_FILE)


@lru_cache()
def get_settings():
    return Settings()
