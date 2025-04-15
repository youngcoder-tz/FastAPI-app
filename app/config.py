from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str 

    class Config:
        env_file = Path(__file__).parent.parent / ".env"

settings = Settings()
