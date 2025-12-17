from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import Optional
import logging
from app.config.settings import settings


logger = logging.getLogger(__name__)


class QdrantConfig:
    """
    Configuration and setup for Qdrant vector database client.
    """

    def __init__(self):
        """
        Initialize Qdrant client with settings from configuration.
        """
        # Initialize Qdrant client
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=False  # Using HTTP for better compatibility
        )

        # Collection name for book content embeddings
        self.collection_name = "book_content_embeddings"

        logger.info(f"Qdrant client initialized with URL: {settings.QDRANT_URL}")

    def get_client(self) -> QdrantClient:
        """
        Get the configured Qdrant client.

        Returns:
            QdrantClient instance
        """
        return self.client

    def get_collection_name(self) -> str:
        """
        Get the name of the collection used for book content.

        Returns:
            Collection name string
        """
        return self.collection_name

    async def initialize_collection(self, vector_size: int = 1536):
        """
        Initialize the collection with appropriate vector configuration.
        This should be called during application startup.

        Args:
            vector_size: Size of the embedding vectors (default 1536 for text-embedding-3-small)
        """
        try:
            # Check if collection already exists
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection with cosine similarity
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=vector_size,
                        distance=models.Distance.COSINE  # Using cosine similarity as per plan
                    ),
                    # Enable hybrid search capabilities
                    hnsw_config=models.HnswConfigDiff(
                        ef_construct=100,
                        m=16
                    ),
                    optimizers_config=models.OptimizersConfigDiff(
                        deleted_threshold=0.2,
                        vacuum_min_vector_number=1000
                    )
                )

                # Create payload index for efficient filtering
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="book_id",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                logger.info(f"Collection '{self.collection_name}' created successfully")
            else:
                logger.info(f"Collection '{self.collection_name}' already exists")

        except Exception as e:
            logger.error(f"Error initializing collection: {str(e)}")
            raise

    async def close(self):
        """
        Close the Qdrant client connection.
        """
        if self.client:
            # QdrantClient doesn't have a close method in the current version
            logger.info("Qdrant client connection closed")


# Global Qdrant configuration instance
qdrant_config = QdrantConfig()


def get_qdrant_client() -> QdrantClient:
    """
    Get the configured Qdrant client instance.

    Returns:
        QdrantClient instance
    """
    return qdrant_config.get_client()


def get_collection_name() -> str:
    """
    Get the configured collection name.

    Returns:
        Collection name string
    """
    return qdrant_config.get_collection_name()