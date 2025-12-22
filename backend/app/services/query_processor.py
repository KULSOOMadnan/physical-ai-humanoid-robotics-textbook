import logging
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.services.session_manager import session_manager
from app.services.vector_store import vector_store_service
from app.services.llm_service import llm_service
from app.models.query_session import QuerySession, QueryMode
from app.models.retrieved_chunk import RetrievedChunk
from app.schemas.query import SourceAttribution
from app.core.exceptions import RetrievalError, GenerationError, ContextInsufficientError
from app.config.database import SessionLocal
from app.utils.performance import perf_monitor
import asyncio


logger = logging.getLogger(__name__)


class QueryProcessor:
    """
    Service for processing queries: retrieval and generation.
    """

    def __init__(self):
        # Use the LLM service that handles OpenAI Agents SDK
        pass

    @perf_monitor.measure_time("query_processor.process_query")
    async def process_query(
        self,
        query: str,
        session_id: Optional[str] = None,
        mode: QueryMode = QueryMode.GLOBAL,
        selected_text: Optional[str] = None
    ) -> Tuple[str, List[SourceAttribution]]:
        """
        Process a query by retrieving relevant context and generating a response.

        Args:
            query: The user's question
            session_id: Session identifier to maintain context
            mode: Query mode (global or selected-text-only)
            selected_text: Text selected by user for selected-text-only mode

        Returns:
            Tuple of (response, list of sources used)
        """
        try:
            # Check if this is a general greeting or conversation that doesn't require book context
            greeting_keywords = ["hello", "hi", "hey", "greetings", "how are you", "good morning", "good afternoon", "good evening"]
            is_greeting = any(keyword in query.lower() for keyword in greeting_keywords)

            if is_greeting:
                # For greetings, return a friendly response without book content
                return f"Hello! I'm your AI assistant for the Physical AI & Humanoid Robotics Textbook. You can ask me questions about humanoid robotics, the textbook content, or the four modules covered in the book.", []

            # Get or create session
            db = SessionLocal()
            try:
                session = await session_manager.get_or_create_session(db, session_id, mode, selected_text)
                session_id = session.id
            finally:
                db.close()

            # Retrieve context based on mode
            if mode == QueryMode.SELECTED_TEXT_ONLY:
                if not selected_text or not selected_text.strip():
                    raise ContextInsufficientError("Selected text is required for selected-text-only mode")

                # Use only the selected text as context
                retrieved_chunks = await self._retrieve_from_selected_text(query, selected_text)
            else:
                # Retrieve from the entire book content
                retrieved_chunks = await self._retrieve_from_book_content(query)

            # If no relevant context found, raise an exception
            if not retrieved_chunks:
                raise ContextInsufficientError("No relevant context found to answer the query")

            # Generate response using the retrieved context
            response = await self._generate_response(query, retrieved_chunks)

            # Create source attributions
            sources = [
                SourceAttribution(
                    content=chunk.content,
                    source=chunk.source,
                    relevance_score=chunk.relevance_score
                )
                for chunk in retrieved_chunks
            ]

            # Store the query and response in session history (future enhancement)
            # For now, just return the response and sources

            return response, sources

        except ContextInsufficientError:
            # Re-raise context errors as they are meaningful to the user
            raise
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise RetrievalError(f"Failed to process query: {str(e)}")

    async def _retrieve_from_book_content(self, query: str) -> List[RetrievedChunk]:
        """
        Retrieve relevant chunks from book content using vector search.

        Args:
            query: The query to search for

        Returns:
            List of retrieved chunks with relevance scores
        """
        try:
            # Use the vector store service to search
            retrieved_chunks = await vector_store_service.search(
                query_text=query,
                limit=5  # Retrieve top 5 most relevant chunks
            )

            logger.info(f"Retrieved {len(retrieved_chunks)} chunks from book content")

            return retrieved_chunks

        except Exception as e:
            logger.error(f"Error retrieving from book content: {str(e)}")
            raise RetrievalError(f"Failed to retrieve from book content: {str(e)}")

    async def _retrieve_from_selected_text(self, query: str, selected_text: str) -> List[RetrievedChunk]:
        """
        Retrieve relevant parts from selected text (for selected-text-only mode).
        In this mode, we validate the selected text for relevance to the query.

        Args:
            query: The query to match against selected text
            selected_text: The text selected by the user

        Returns:
            List containing the selected text as a single chunk, or empty list if validation fails
        """
        try:
            # Validate that the selected text contains relevant information for the query
            # This is a simple validation - in a more sophisticated implementation,
            # we could do semantic matching within the selected text
            if not selected_text or len(selected_text.strip()) == 0:
                logger.warning("Selected text is empty")
                return []

            # Check if the selected text is too short to contain relevant information
            if len(selected_text.strip()) < 10:
                logger.warning("Selected text is too short to contain relevant information")
                return []

            # Simple keyword matching to check if the selected text might be relevant
            query_lower = query.lower()
            text_lower = selected_text.lower()

            # Look for basic semantic relevance (keywords from query in selected text)
            query_words = query_lower.split()
            matching_words = [word for word in query_words if word in text_lower]

            # If less than 30% of query words are found in the selected text,
            # it might not be relevant, but we still return the text since the user selected it
            # We'll let the LLM determine if it can answer the question
            logger.info(f"Selected text validation: {len(matching_words)}/{len(query_words)} query words found in selected text")

            chunk = RetrievedChunk(
                id="selected_text_chunk",
                content=selected_text,
                source="user_selected_text",
                relevance_score=0.8,  # High relevance since user selected it, but not perfect
                session_id="temp"  # Will be set properly when storing to DB
            )

            logger.info("Retrieved selected text for selected-text-only mode")

            return [chunk]

        except Exception as e:
            logger.error(f"Error retrieving from selected text: {str(e)}")
            raise RetrievalError(f"Failed to retrieve from selected text: {str(e)}")

    async def _generate_response(self, query: str, retrieved_chunks: List[RetrievedChunk]) -> str:
        """
        Generate a response using OpenAI Agents SDK based on the query and retrieved context.

        Args:
            query: The user's question
            retrieved_chunks: List of relevant context chunks

        Returns:
            Generated response string
        """
        try:
            # Use the LLM service which handles OpenAI Agents SDK
            response, _ = await llm_service.generate_response_with_sources(query, retrieved_chunks)

            logger.info("Response generated successfully using OpenAI Agents SDK")

            return response

        except Exception as e:
            logger.error(f"Error generating response with OpenAI Agents SDK: {str(e)}")
            raise GenerationError(f"Failed to generate response: {str(e)}")


# Default query processor instance
query_processor = QueryProcessor()