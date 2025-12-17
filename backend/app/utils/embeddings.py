import asyncio
import logging
from typing import List, Union
import numpy as np
import tiktoken
from openai import AsyncOpenAI
from app.config.settings import settings


logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """
    Utility class for generating embeddings using OpenAI's embedding models.
    """

    def __init__(self):
        """
        Initialize the embedding generator with OpenAI client.
        """
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"  # Using the smaller, more efficient model
        self.encoding = tiktoken.encoding_for_model(self.model)

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Input text to embed

        Returns:
            Embedding vector as a list of floats
        """
        try:
            response = await self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise

    async def generate_embeddings(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Generate embeddings for a list of texts in batches.

        Args:
            texts: List of input texts to embed
            batch_size: Number of texts to process in each batch

        Returns:
            List of embedding vectors
        """
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                response = await self.client.embeddings.create(
                    input=batch,
                    model=self.model
                )
                batch_embeddings = [data.embedding for data in response.data]
                all_embeddings.extend(batch_embeddings)
            except Exception as e:
                logger.error(f"Error generating embeddings for batch {i//batch_size + 1}: {str(e)}")
                raise

        return all_embeddings

    def get_text_token_count(self, text: str) -> int:
        """
        Get the number of tokens in a text.

        Args:
            text: Input text

        Returns:
            Number of tokens in the text
        """
        return len(self.encoding.encode(text))

    def get_texts_token_count(self, texts: List[str]) -> int:
        """
        Get the total number of tokens in a list of texts.

        Args:
            texts: List of input texts

        Returns:
            Total number of tokens
        """
        total_tokens = 0
        for text in texts:
            total_tokens += len(self.encoding.encode(text))
        return total_tokens


# Default embedding generator instance
default_embedding_generator = EmbeddingGenerator()


async def generate_embedding(text: str) -> List[float]:
    """
    Convenience function to generate embedding for a single text.

    Args:
        text: Input text to embed

    Returns:
        Embedding vector as a list of floats
    """
    return await default_embedding_generator.generate_embedding(text)


async def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Convenience function to generate embeddings for a list of texts.

    Args:
        texts: List of input texts to embed

    Returns:
        List of embedding vectors
    """
    return await default_embedding_generator.generate_embeddings(texts)