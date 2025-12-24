from pydantic_settings import BaseSettings
from pydantic import BaseModel
from typing import Optional


class Settings(BaseModel):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str

    # Qdrant
    QDRANT_URL: str
    QDRANT_API_KEY: str

    # OpenAI (for compatibility)
    OPENAI_API_KEY: Optional[str] = None

    # Google Gemini (deprecated - using OpenRouter instead)
    GEMINI_API_KEY: Optional[str] = None

    # OpenRouter
    OPENROUTER_API_KEY: str

    # Cohere (for embeddings)
    COHERE_API_KEY: Optional[str] = None

    # Default LLM Model
    DEFAULT_LLM_MODEL: str = "openai/gpt-4o-mini"

    # Application
    API_KEY: Optional[str] = None
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"

# Create a single instance of settings
_settings = None

def get_settings():
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
