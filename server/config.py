from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    class config:
        env_file = str(Path(__file__).resolve().parent / ".env")

settings = Settings()