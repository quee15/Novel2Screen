import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "mysql+mysqlconnector://root:26210@localhost:3306/yudada"

    # File storage
    UPLOAD_DIR: str = "./uploads"
    EXPORT_DIR: str = "./exports"

    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8080
    DEBUG: bool = True

    # CORS
    CORS_ORIGINS: list[str] = ["*"]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


@lru_cache()
def get_settings() -> Settings:
    return Settings()
