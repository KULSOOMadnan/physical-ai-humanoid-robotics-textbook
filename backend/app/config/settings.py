from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str

    # Qdrant
    QDRANT_URL: str
    QDRANT_API_KEY: str

    # OpenAI (for compatibility)
    OPENAI_API_KEY: Optional[str] = None

    # Google Gemini
    GEMINI_API_KEY: str

    # Application
    API_KEY: Optional[str] = None
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()