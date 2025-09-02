
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_DEFAULT_MODEL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
