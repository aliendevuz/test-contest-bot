from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    telegram_token: str
    admin_id: int
    database_url: str = "sqlite:///./data.db"
    supported_languages: list[str] = ["uz", "ru", "en"]
    default_language: str = "uz"

    class Config:
        env_file = ".env"


settings = Settings()
