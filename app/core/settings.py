from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    GEMINI_MODEL_NAME: str = "gemini-2.0-flash"
    GITHUB_TOKEN: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

