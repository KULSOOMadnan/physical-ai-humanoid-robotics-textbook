import asyncio
import logging
from typing import List, Union
import numpy as np
import tiktoken
import httpx
from app.config.settings import settings


logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """
    Utility class for generating embeddings using Cohere API.
    """

    def __init__(self):
        """
        Initialize the embedding generator with Cohere client.
        """
        self.api_key = settings.COHERE_API_KEY  # Need to add COHERE_API_KEY to settings
        self.model = "embed-english-v3.0"  # Using Cohere's free embedding model
        # Use a common encoding; tiktoken encoding might need to be adjusted based on the model
        self.encoding = tiktoken.get_encoding("cl100k_base")
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            timeout=30.0
        )

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text using Cohere API.

        Args:
            text: Input text to embed

        Returns:
            Embedding vector as a list of floats
        """
        try:
            url = "https://api.cohere.ai/v1/embed"
            payload = {
                "texts": [text],
                "model": self.model,
                "input_type": "search_document"  # Using search_document for content to be searched
            }

            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result['embeddings'][0]  # Return the first embedding
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error generating embedding with Cohere: {str(e)}")
            error_msg = str(e)
            if "401" in error_msg or "403" in error_msg or "invalid API key" in error_msg.lower():
                logger.error("Cohere API key is invalid or unauthorized")
                raise
            elif "429" in error_msg or "rate limit" in error_msg.lower():
                logger.warning("Cohere rate limit exceeded, returning mock embedding")
                # Return a mock embedding vector (1024 dimensions for Cohere's model)
                import hashlib
                hash_object = hashlib.md5(text.encode())
                hex_dig = hash_object.hexdigest()
                # Create a 1024-dim vector based on the hash (Cohere's embed-english-v3.0 returns 1024-dim vectors)
                embedding = []
                for i in range(0, 1024*2, 2):
                    if i+1 < len(hex_dig):
                        val = int(hex_dig[i:i+2], 16) / 255.0  # Convert hex to 0-1 range
                        embedding.append(val)
                    else:
                        embedding.append(0.0)
                if len(embedding) < 1024:
                    embedding.extend([0.0] * (1024 - len(embedding)))
                return embedding[:1024]  # Ensure exactly 1024 dimensions
            else:
                logger.error(f"Error generating embedding: {str(e)}")
                raise
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            error_msg = str(e)
            if "401" in error_msg or "403" in error_msg or "invalid API key" in error_msg.lower():
                logger.error("Cohere API key is invalid or unauthorized")
                raise
            elif "429" in error_msg or "rate limit" in error_msg.lower():
                logger.warning("Cohere rate limit exceeded, returning mock embedding")
                # Return a mock embedding vector (1024 dimensions for Cohere's model)
                import hashlib
                hash_object = hashlib.md5(text.encode())
                hex_dig = hash_object.hexdigest()
                # Create a 1024-dim vector based on the hash
                embedding = []
                for i in range(0, 1024*2, 2):
                    if i+1 < len(hex_dig):
                        val = int(hex_dig[i:i+2], 16) / 255.0  # Convert hex to 0-1 range
                        embedding.append(val)
                    else:
                        embedding.append(0.0)
                if len(embedding) < 1024:
                    embedding.extend([0.0] * (1024 - len(embedding)))
                return embedding[:1024]  # Ensure exactly 1024 dimensions
            else:
                raise

    async def generate_embeddings(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Generate embeddings for a list of texts in batches using Cohere API.

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
                url = "https://api.cohere.ai/v1/embed"
                payload = {
                    "texts": batch,
                    "model": self.model,
                    "input_type": "search_document"  # Using search_document for content to be searched
                }

                response = await self.client.post(url, json=payload)
                response.raise_for_status()
                result = response.json()
                batch_embeddings = result['embeddings']
                all_embeddings.extend(batch_embeddings)
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error generating embeddings for batch {i//batch_size + 1}: {str(e)}")
                error_msg = str(e)
                if "401" in error_msg or "403" in error_msg or "invalid API key" in error_msg.lower():
                    logger.error("Cohere API key is invalid or unauthorized")
                    raise
                elif "429" in error_msg or "rate limit" in error_msg.lower():
                    logger.warning("Cohere rate limit exceeded for batch, returning mock embeddings")
                    # Generate mock embeddings for the batch (1024 dimensions for Cohere's model)
                    for text in batch:
                        import hashlib
                        hash_object = hashlib.md5(text.encode())
                        hex_dig = hash_object.hexdigest()
                        # Create a 1024-dim vector based on the hash
                        embedding = []
                        for j in range(0, 1024*2, 2):
                            if j+1 < len(hex_dig):
                                val = int(hex_dig[j:j+2], 16) / 255.0  # Convert hex to 0-1 range
                                embedding.append(val)
                            else:
                                embedding.append(0.0)
                        if len(embedding) < 1024:
                            embedding.extend([0.0] * (1024 - len(embedding)))
                        all_embeddings.append(embedding[:1024])  # Ensure exactly 1024 dimensions
                else:
                    logger.error(f"Error generating embeddings for batch: {str(e)}")
                    raise
            except Exception as e:
                logger.error(f"Error generating embeddings for batch {i//batch_size + 1}: {str(e)}")
                error_msg = str(e)
                if "401" in error_msg or "403" in error_msg or "invalid API key" in error_msg.lower():
                    logger.error("Cohere API key is invalid or unauthorized")
                    raise
                elif "429" in error_msg or "rate limit" in error_msg.lower():
                    logger.warning("Cohere rate limit exceeded for batch, returning mock embeddings")
                    # Generate mock embeddings for the batch (1024 dimensions for Cohere's model)
                    for text in batch:
                        import hashlib
                        hash_object = hashlib.md5(text.encode())
                        hex_dig = hash_object.hexdigest()
                        # Create a 1024-dim vector based on the hash
                        embedding = []
                        for j in range(0, 1024*2, 2):
                            if j+1 < len(hex_dig):
                                val = int(hex_dig[j:j+2], 16) / 255.0  # Convert hex to 0-1 range
                                embedding.append(val)
                            else:
                                embedding.append(0.0)
                        if len(embedding) < 1024:
                            embedding.extend([0.0] * (1024 - len(embedding)))
                        all_embeddings.append(embedding[:1024])  # Ensure exactly 1024 dimensions
                else:
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