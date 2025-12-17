import logging
from typing import List
from app.models.retrieved_chunk import RetrievedChunk
from app.schemas.query import SourceAttribution
from app.utils.citations import format_citation
import random


logger = logging.getLogger(__name__)


class MockLLMService:
    """
    Mock LLM service for testing without API keys.
    Simulates LLM responses based on the provided context.
    """

    def __init__(self):
        logger.info("Initialized Mock LLM Service for testing purposes")

    async def generate_response(
        self,
        query: str,
        retrieved_chunks: List[RetrievedChunk],
        include_attribution: bool = True
    ) -> str:
        """
        Generate a mock response based on the query and retrieved context.
        """
        if not retrieved_chunks:
            return "I cannot answer this question based on the provided context. No relevant information was found."

        # Create a mock response based on the query and context
        query_lower = query.lower()

        # Simple heuristic to create relevant response
        if any(word in query_lower for word in ["what", "how", "explain", "describe"]):
            # Extract key information from the context
            context_snippets = [chunk.content[:200] for chunk in retrieved_chunks[:2]]  # Take first 2 chunks
            context_preview = " ".join(context_snippets)

            response = f"Based on the provided context: {context_preview}... The document discusses topics related to your question about '{query}'. For more detailed information, please refer to the specific sections mentioned in the sources."
        else:
            response = f"According to the book content, I found information related to your query '{query}'. The relevant sections indicate that this topic is covered in the provided context."

        return response

    async def generate_response_with_sources(
        self,
        query: str,
        retrieved_chunks: List[RetrievedChunk]
    ) -> tuple[str, List[SourceAttribution]]:
        """
        Generate a mock response and return both the response and source attributions.
        """
        response = await self.generate_response(query, retrieved_chunks)

        # Create source attributions from the retrieved chunks
        sources = []
        for chunk in retrieved_chunks:
            # Extract page number and section title from source if available
            page_number = None
            section_title = None

            # Parse source to extract page and section info
            if "page:" in chunk.source:
                import re
                page_match = re.search(r'page:(\d+)', chunk.source)
                if page_match:
                    page_number = int(page_match.group(1))

            if "section:" in chunk.source:
                import re
                section_match = re.search(r'section:([^#]+)', chunk.source)
                if section_match:
                    section_title = section_match.group(1)

            # Create formatted citation
            citation = format_citation(chunk.source, str(page_number) if page_number else None)

            source_attr = SourceAttribution(
                content=chunk.content,
                source=chunk.source,
                relevance_score=chunk.relevance_score,
                page_number=page_number,
                section_title=section_title,
                citation=citation
            )
            sources.append(source_attr)

        return response, sources

    async def validate_response_accuracy(
        self,
        query: str,
        response: str,
        retrieved_chunks: List[RetrievedChunk]
    ) -> bool:
        """
        Mock validation - always return True for testing purposes.
        """
        return True