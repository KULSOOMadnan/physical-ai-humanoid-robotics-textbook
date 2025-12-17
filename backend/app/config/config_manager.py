import os
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel, ValidationError
from .settings import settings


logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Centralized configuration management for the application.
    Handles environment-specific configuration loading and validation.
    """

    def __init__(self):
        self.config = {}
        self._load_config()

    def _load_config(self):
        """Load configuration from various sources."""
        # Load from settings (environment variables)
        self.config = {
            "database": {
                "url": settings.DATABASE_URL,
                "pool_size": int(os.getenv("DB_POOL_SIZE", "5")),
                "pool_timeout": int(os.getenv("DB_POOL_TIMEOUT", "30")),
            },
            "qdrant": {
                "url": settings.QDRANT_URL,
                "api_key": settings.QDRANT_API_KEY,
                "collection_name": os.getenv("QDRANT_COLLECTION_NAME", "book_content"),
            },
            "llm": {
                "provider": os.getenv("LLM_PROVIDER", "gemini").lower(),
                "gemini_api_key": settings.GEMINI_API_KEY,
                "openai_api_key": settings.OPENAI_API_KEY,
                "default_model": os.getenv("DEFAULT_LLM_MODEL", "gemini-pro"),
            },
            "app": {
                "debug": settings.DEBUG,
                "host": settings.HOST,
                "port": settings.PORT,
                "api_key": settings.API_KEY,
                "cors_origins": os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else [],
            },
            "logging": {
                "level": os.getenv("LOG_LEVEL", "INFO").upper(),
                "format": os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            },
            "performance": {
                "timeout": int(os.getenv("REQUEST_TIMEOUT", "30")),
                "max_concurrent_requests": int(os.getenv("MAX_CONCURRENT_REQUESTS", "100")),
                "cache_ttl": int(os.getenv("CACHE_TTL", "3600")),  # 1 hour default
            }
        }

        logger.info("Configuration loaded successfully")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.

        Args:
            key: Configuration key in dot notation (e.g., "database.url")
            default: Default value if key is not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """
        Set a configuration value using dot notation.

        Args:
            key: Configuration key in dot notation
            value: Value to set
        """
        keys = key.split(".")
        config_ref = self.config

        for k in keys[:-1]:
            if k not in config_ref:
                config_ref[k] = {}
            config_ref = config_ref[k]

        config_ref[keys[-1]] = value

    def validate_config(self) -> bool:
        """
        Validate the loaded configuration.

        Returns:
            True if configuration is valid, False otherwise
        """
        required_keys = [
            "database.url",
            "qdrant.url",
            "qdrant.api_key",
            "llm.gemini_api_key"
        ]

        missing_keys = []
        for key in required_keys:
            if self.get(key) is None:
                missing_keys.append(key)

        if missing_keys:
            logger.error(f"Missing required configuration keys: {missing_keys}")
            return False

        # Validate database URL
        db_url = self.get("database.url")
        if not db_url or not db_url.strip():
            logger.error("Database URL is empty")
            return False

        # Validate Qdrant settings
        qdrant_url = self.get("qdrant.url")
        qdrant_api_key = self.get("qdrant.api_key")
        if not qdrant_url or not qdrant_api_key:
            logger.error("Qdrant URL or API key is missing")
            return False

        # Validate LLM provider settings
        llm_provider = self.get("llm.provider")
        if llm_provider == "gemini":
            gemini_key = self.get("llm.gemini_api_key")
            if not gemini_key:
                logger.error("Gemini API key is required when LLM provider is set to 'gemini'")
                return False
        elif llm_provider == "openai":
            openai_key = self.get("llm.openai_api_key")
            if not openai_key:
                logger.error("OpenAI API key is required when LLM provider is set to 'openai'")
                return False

        logger.info("Configuration validation passed")
        return True

    def get_database_config(self) -> Dict[str, Any]:
        """Get database-specific configuration."""
        return self.get("database", {})

    def get_qdrant_config(self) -> Dict[str, Any]:
        """Get Qdrant-specific configuration."""
        return self.get("qdrant", {})

    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM-specific configuration."""
        return self.get("llm", {})

    def get_app_config(self) -> Dict[str, Any]:
        """Get application-specific configuration."""
        return self.get("app", {})

    def get_performance_config(self) -> Dict[str, Any]:
        """Get performance-specific configuration."""
        return self.get("performance", {})


# Global configuration manager instance
config_manager = ConfigManager()


def get_config() -> ConfigManager:
    """
    Get the global configuration manager instance.

    Returns:
        ConfigManager instance
    """
    return config_manager


def validate_deployment_config() -> bool:
    """
    Validate configuration specifically for deployment.

    Returns:
        True if deployment configuration is valid, False otherwise
    """
    return config_manager.validate_config()