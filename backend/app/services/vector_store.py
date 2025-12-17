import logging
from typing import List, Optional
from app.config.qdrant import get_qdrant_client, get_collection_name
from app.utils.embeddings import EmbeddingGenerator
from app.models.retrieved_chunk import RetrievedChunk
from app.core.exceptions import RetrievalError


logger = logging.getLogger(__name__)


class VectorStoreService:
    """
    Service for handling vector store operations with Qdrant.
    """

    def __init__(self):
        self.client = get_qdrant_client()
        self.collection_name = get_collection_name()
        self.embedding_generator = EmbeddingGenerator()

    async def search(
        self,
        query_text: str,
        limit: int = 5,
        filters: Optional[dict] = None
    ) -> List[RetrievedChunk]:
        """
        Search for relevant chunks in the vector store based on the query.

        Args:
            query_text: The text to search for
            limit: Maximum number of results to return
            filters: Optional filters to apply to the search

        Returns:
            List of retrieved chunks with relevance scores
        """
        try:
            # Generate embedding for the query
            query_embedding = await self.embedding_generator.generate_embedding(query_text)

            # Prepare search filters if provided
            qdrant_filters = None
            if filters:
                from qdrant_client.http import models
                filter_conditions = []
                for key, value in filters.items():
                    filter_conditions.append(
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        )
                    )

                if filter_conditions:
                    qdrant_filters = models.Filter(
                        must=filter_conditions
                    )

            # Search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                with_payload=True,
                query_filter=qdrant_filters
            )

            # Convert search results to RetrievedChunk objects
            retrieved_chunks = []
            for result in search_results:
                payload = result.payload or {}
                chunk = RetrievedChunk(
                    id=result.id,
                    content=payload.get("content", ""),
                    source=payload.get("source", ""),
                    relevance_score=result.score,
                    page_number=payload.get("page_number"),
                    section_title=payload.get("section_title"),
                    chunk_metadata=payload.get("metadata", {}),
                    session_id="temp"  # Will be set properly when storing to DB
                )
                retrieved_chunks.append(chunk)

            logger.info(f"Vector search returned {len(retrieved_chunks)} results")

            return retrieved_chunks

        except Exception as e:
            logger.error(f"Error performing vector search: {str(e)}")
            raise RetrievalError(f"Failed to perform vector search: {str(e)}")

    async def add_document(
        self,
        doc_id: str,
        content: str,
        metadata: Optional[dict] = None,
        vector: Optional[List[float]] = None
    ) -> bool:
        """
        Add a document to the vector store.

        Args:
            doc_id: Unique identifier for the document
            content: Content of the document
            metadata: Additional metadata for the document
            vector: Pre-computed vector (if None, will be computed)

        Returns:
            True if successful
        """
        try:
            # Generate embedding if not provided
            if vector is None:
                vector = await self.embedding_generator.generate_embedding(content)

            # Prepare payload
            payload = {
                "content": content,
                "source": metadata.get("source", "") if metadata else "",
                "page_number": metadata.get("page_number") if metadata else None,
                "section_title": metadata.get("section_title") if metadata else None,
                "metadata": metadata or {},
                **(metadata or {})
            }

            # Upload to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    {
                        "id": doc_id,
                        "vector": vector,
                        "payload": payload
                    }
                ]
            )

            logger.info(f"Document {doc_id} added to vector store")

            return True

        except Exception as e:
            logger.error(f"Error adding document to vector store: {str(e)}")
            raise RetrievalError(f"Failed to add document to vector store: {str(e)}")

    async def batch_add_documents(
        self,
        documents: List[dict]  # Each dict should have 'id', 'content', and optional 'metadata'
    ) -> bool:
        """
        Add multiple documents to the vector store in a batch.

        Args:
            documents: List of documents, each with id, content, and optional metadata

        Returns:
            True if successful
        """
        try:
            # Prepare points for Qdrant
            points = []
            for doc in documents:
                doc_id = doc["id"]
                content = doc["content"]
                metadata = doc.get("metadata", {})

                # Generate embedding
                vector = await self.embedding_generator.generate_embedding(content)

                # Prepare payload
                payload = {
                    "content": content,
                    "source": metadata.get("source", ""),
                    "page_number": metadata.get("page_number") if metadata else None,
                    "section_title": metadata.get("section_title") if metadata else None,
                    "metadata": metadata or {},
                    **metadata
                }

                points.append({
                    "id": doc_id,
                    "vector": vector,
                    "payload": payload
                })

            # Upload to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Batch added {len(points)} documents to vector store")

            return True

        except Exception as e:
            logger.error(f"Error batch adding documents to vector store: {str(e)}")
            raise RetrievalError(f"Failed to batch add documents to vector store: {str(e)}")

    async def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document from the vector store.

        Args:
            doc_id: ID of the document to delete

        Returns:
            True if successful
        """
        try:
            # Delete from Qdrant
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[doc_id]
            )

            logger.info(f"Document {doc_id} deleted from vector store")

            return True

        except Exception as e:
            logger.error(f"Error deleting document from vector store: {str(e)}")
            raise RetrievalError(f"Failed to delete document from vector store: {str(e)}")

    async def get_document(self, doc_id: str) -> Optional[RetrievedChunk]:
        """
        Retrieve a specific document by ID.

        Args:
            doc_id: ID of the document to retrieve

        Returns:
            RetrievedChunk if found, None otherwise
        """
        try:
            # Retrieve from Qdrant
            records = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[doc_id],
                with_payload=True,
                with_vectors=False
            )

            if not records:
                return None

            record = records[0]
            payload = record.payload or {}

            chunk = RetrievedChunk(
                id=record.id,
                content=payload.get("content", ""),
                source=payload.get("source", ""),
                relevance_score=1.0,  # Not a search result, so relevance is 1.0
                session_id="temp"
            )

            return chunk

        except Exception as e:
            logger.error(f"Error retrieving document from vector store: {str(e)}")
            raise RetrievalError(f"Failed to retrieve document from vector store: {str(e)}")


# Default vector store service instance
vector_store_service = VectorStoreService()