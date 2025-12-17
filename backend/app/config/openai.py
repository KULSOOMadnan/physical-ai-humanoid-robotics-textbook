from openai import AsyncOpenAI
import logging
from app.config.settings import settings


logger = logging.getLogger(__name__)


class OpenAIConfig:
    """
    Configuration and setup for OpenAI client.
    """

    def __init__(self):
        """
        Initialize OpenAI client with settings from configuration.
        """
        # Initialize OpenAI client
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        # Default model for responses
        self.default_model = "gpt-4o"  # Using the latest efficient model

        logger.info("OpenAI client initialized")

    def get_client(self) -> AsyncOpenAI:
        """
        Get the configured OpenAI client.

        Returns:
            AsyncOpenAI instance
        """
        return self.client

    def get_default_model(self) -> str:
        """
        Get the default model name.

        Returns:
            Model name string
        """
        return self.default_model


# Global OpenAI configuration instance
openai_config = OpenAIConfig()


def get_openai_client() -> AsyncOpenAI:
    """
    Get the configured OpenAI client instance.

    Returns:
        AsyncOpenAI instance
    """
    return openai_config.get_client()


def get_default_model() -> str:
    """
    Get the default OpenAI model.

    Returns:
        Model name string
    """
    return openai_config.get_default_model()