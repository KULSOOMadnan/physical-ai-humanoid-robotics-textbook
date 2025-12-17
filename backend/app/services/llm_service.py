import logging
from typing import List, Optional
from agents import Agent, RunContextWrapper, Runner, function_tool, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig
from app.config.gemini import model, run_config
from app.models.retrieved_chunk import RetrievedChunk
from app.schemas.query import SourceAttribution
from app.core.exceptions import GenerationError
from app.utils.citations import format_citation, extract_quote_highlights
import asyncio


logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for handling LLM interactions using Google Gemini via OpenAI-compatible API.
    """

    def __init__(self):
        # Create an agent for RAG purposes using Gemini
        self.agent = Agent(
            name="RAG Book Assistant",
            instructions="You are a helpful assistant that answers questions based on provided book content. Only use information from the provided context to answer questions. If the context doesn't contain enough information, say that you cannot answer based on the provided context. Be concise but thorough in your responses.",
            model=model
        )

    async def generate_response(
        self,
        query: str,
        retrieved_chunks: List[RetrievedChunk],
        include_attribution: bool = True
    ) -> str:
        """
        Generate a response using OpenAI Agents SDK based on the query and retrieved context.

        Args:
            query: The user's question
            retrieved_chunks: List of relevant context chunks
            include_attribution: Whether to include source attribution in the response

        Returns:
            Generated response string
        """
        try:
            # Format the context from retrieved chunks
            context_parts = []
            for i, chunk in enumerate(retrieved_chunks):
                context_parts.append(f"[Source {i+1}]: {chunk.content}")

            context = "\n\n".join(context_parts)

            # Create the full prompt with context
            full_prompt = f"""
            Context:
            {context}

            Question: {query}

            Answer:
            """

            # Use the agent to generate response
            response = await self.agent.run(
                messages=[{"role": "user", "content": full_prompt}],
                config=run_config
            )

            # Extract the response content from the Gemini response
            if hasattr(response, 'choices') and response.choices:
                response_text = response.choices[0].message.content if response.choices[0].message.content else ""
            elif hasattr(response, 'content'):
                response_text = response.content
            else:
                response_text = str(response)

            logger.info("Response generated successfully using Google Gemini via OpenAI-compatible API")

            return response_text

        except Exception as e:
            logger.error(f"Error generating response with OpenAI Agents SDK: {str(e)}")
            raise GenerationError(f"Failed to generate response: {str(e)}")

    async def generate_response_with_sources(
        self,
        query: str,
        retrieved_chunks: List[RetrievedChunk]
    ) -> tuple[str, List[SourceAttribution]]:
        """
        Generate a response and return both the response and enhanced source attributions.

        Args:
            query: The user's question
            retrieved_chunks: List of relevant context chunks

        Returns:
            Tuple of (generated response, list of source attributions)
        """
        try:
            # Generate the response
            response = await self.generate_response(query, retrieved_chunks, include_attribution=True)

            # Create enhanced source attributions
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

        except Exception as e:
            logger.error(f"Error generating response with sources: {str(e)}")
            raise GenerationError(f"Failed to generate response with sources: {str(e)}")

    async def validate_response_accuracy(
        self,
        query: str,
        response: str,
        retrieved_chunks: List[RetrievedChunk]
    ) -> bool:
        """
        Validate that the response is grounded in the retrieved context.
        This is a basic implementation - in a production system, you might use more sophisticated validation.

        Args:
            query: The original query
            response: The generated response
            retrieved_chunks: The chunks used to generate the response

        Returns:
            True if the response appears to be grounded in the context, False otherwise
        """
        try:
            # Basic validation: check if the response contains information from the chunks
            response_lower = response.lower()
            context_parts = [chunk.content.lower() for chunk in retrieved_chunks]

            # Check if there's overlap between response and context
            overlap_score = 0
            for context_part in context_parts:
                # Simple keyword overlap check
                words_in_context = set(context_part.split())
                words_in_response = set(response_lower.split())
                overlap = len(words_in_context.intersection(words_in_response))
                if len(words_in_context) > 0:
                    overlap_score += overlap / len(words_in_context)

            # If there's sufficient overlap, consider it grounded
            is_valid = overlap_score > 0.1  # At least 10% overlap threshold

            return is_valid

        except Exception as e:
            logger.error(f"Error validating response accuracy: {str(e)}")
            # In case of validation error, return True to not block the response
            return True

    async def validate_source_attribution(
        self,
        response: str,
        sources: List[SourceAttribution]
    ) -> bool:
        """
        Validate that all responses include proper source attribution.

        Args:
            response: The generated response
            sources: List of source attributions

        Returns:
            True if all attributions are valid, False otherwise
        """
        try:
            # Convert SourceAttribution objects to dictionaries for validation
            sources_dicts = []
            for source in sources:
                source_dict = {
                    'content': source.content,
                    'source': source.source,
                    'relevance_score': source.relevance_score
                }
                if source.page_number is not None:
                    source_dict['page_number'] = source.page_number
                if source.section_title is not None:
                    source_dict['section_title'] = source.section_title
                if source.citation is not None:
                    source_dict['citation'] = source.citation

                sources_dicts.append(source_dict)

            # Use the utility function to validate attributions
            from app.utils.citations import validate_all_response_attributions
            is_valid = validate_all_response_attributions(response, sources_dicts)

            return is_valid

        except Exception as e:
            logger.error(f"Error validating source attribution: {str(e)}")
            return False


# Global LLM service instance
llm_service = LLMService()