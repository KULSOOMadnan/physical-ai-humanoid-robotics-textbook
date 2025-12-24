import logging
from typing import List, Optional
import asyncio
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from app.config.settings import get_settings
from app.models.retrieved_chunk import RetrievedChunk
from app.schemas.query import SourceAttribution
from app.core.exceptions import GenerationError
from app.utils.citations import format_citation
from app.utils.performance import perf_monitor

# Disable tracing
set_tracing_disabled(disabled=True)


logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for handling LLM interactions using OpenAI Agents SDK with OpenRouter.
    """

    def __init__(self):
        # Create AsyncOpenAI client for OpenRouter
        self.client = AsyncOpenAI(
            api_key=get_settings().OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )

        # Create an agent for RAG purposes using OpenRouter
        self.agent = Agent(
            name="RAG Book Assistant",
            instructions="You are an expert AI assistant for the Physical AI & Humanoid Robotics \n Textbook. Your role is to answer user questions by synthesizing information from the provided context into clear, well-structured responses.\n\nBEHAVIOR:\n1. For greetings (hello, hi, hey, good morning, etc.) and general conversation: respond with a friendly greeting and invite questions about the textbook content.\n2. For content-related questions: synthesize information into comprehensive, well-formatted answers.\n\nGUIDELINES:\n1. Always format responses clearly with proper structure (introduction, body, conclusion when appropriate)\n2. NEVER return raw textbook content with phrases like 'Based on the textbook content:', 'According to the book:', 'Source:', or similar.\n3. Instead, synthesize the information into a comprehensive answer that directly addresses the user's question\n4. Use proper formatting: bullet points, numbered lists, or sections when appropriate\n5. If multiple sources are provided, integrate the information cohesively rather than listing sources\n6. If the context doesn't contain sufficient information to answer the question, clearly state this\n7. Maintain a professional, educational tone appropriate for academic content\n8. Focus on providing valuable insights rather than just copying text\n\nYour responses should be informative, well-organized, and directly address what the user asked.",
            model=OpenAIChatCompletionsModel(
                model=get_settings().DEFAULT_LLM_MODEL,  # Use model from settings
                openai_client=self.client
            )
        )

    @perf_monitor.measure_time("llm_service.generate_response")
    async def generate_response(
        self,
        query: str,
        retrieved_chunks: List[RetrievedChunk]
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

            # Run the agent with the prompt using Runner with timeout
            import asyncio
            try:
                response = await asyncio.wait_for(
                    Runner.run(self.agent, full_prompt),
                    timeout=30.0  # 30 second timeout
                )
            except Exception as runner_error:
                logger.error(f"Error running agent with Runner: {str(runner_error)}")
                # Return a properly formatted response based on the context even if the agent fails
                if retrieved_chunks:
                    # Format the context and ask the agent to synthesize a proper response
                    context_parts = []
                    for i, chunk in enumerate(retrieved_chunks[:3]):  # Use top 3 chunks
                        context_parts.append(f"Source {i+1}: {chunk.content}")

                    context = "\n\n".join(context_parts)

                    # Create a prompt asking for a synthesized response
                    fallback_prompt = f"""
                    Context:
                    {context}

                    Question: {query}

                    Please provide a comprehensive, well-formatted answer based on the provided context that directly addresses the question. Format your response clearly with proper structure.

                    Answer:
                    """

                    # Try to run the agent with the fallback prompt
                    try:
                        response = Runner.run(self.agent, fallback_prompt)
                        if hasattr(response, 'final_output'):
                            return response.final_output
                        elif hasattr(response, 'content'):
                            return response.content
                        elif hasattr(response, 'text'):
                            return response.text
                        elif isinstance(response, str):
                            return response
                        else:
                            # If agent fails completely, return formatted context
                            most_relevant = max(retrieved_chunks, key=lambda x: x.relevance_score)
                            return f"I found relevant information about '{query}': {most_relevant.content[:600]}..."
                    except:
                        # If agent fails, return formatted context
                        most_relevant = max(retrieved_chunks, key=lambda x: x.relevance_score)
                        return f"I found information about '{query}' in the textbook: {most_relevant.content[:600]}..."
                else:
                    return "I cannot provide a detailed answer without sufficient context."

            # Extract the response content from the agents response
            if hasattr(response, 'final_output'):
                response_text = response.final_output
            elif hasattr(response, 'content'):
                response_text = response.content
            elif hasattr(response, 'text'):
                response_text = response.text
            elif isinstance(response, str):
                response_text = response
            else:
                response_text = str(response)

            logger.info("Response generated successfully using OpenAI Agents SDK with OpenRouter")

            # Check if the response contains problematic formatting and fix it
            if ("based on the textbook content" in response_text.lower() or
                "according to the book" in response_text.lower() or
                "based on the provided context" in response_text.lower() or
                response_text.strip().startswith("based on")):

                # Format the context and ask the agent to synthesize a proper response
                context_parts = []
                for i, chunk in enumerate(retrieved_chunks[:3]):  # Use top 3 chunks
                    context_parts.append(f"Source {i+1}: {chunk.content}")

                context = "\n\n".join(context_parts)

                # Create a prompt asking for a synthesized response
                fallback_prompt = f"""
                Context:
                {context}

                Question: {query}

                Please provide a comprehensive, well-formatted answer based on the provided context that directly addresses the question. Format your response clearly with proper structure. Do NOT start your response with phrases like "Based on the textbook content:" or "According to the provided context:". Instead, directly answer the question with well-structured information.

                Answer:
                """

                # Try to run the agent with the fallback prompt to get properly formatted response
                try:
                    formatted_response = Runner.run(self.agent, fallback_prompt)
                    if hasattr(formatted_response, 'final_output'):
                        return formatted_response.final_output
                    elif hasattr(formatted_response, 'content'):
                        return formatted_response.content
                    elif hasattr(formatted_response, 'text'):
                        return formatted_response.text
                    elif isinstance(formatted_response, str):
                        return formatted_response
                    else:
                        # If the formatted response also fails, return the original but cleaned up
                        return response_text.replace("Based on the textbook content:", "").strip()
                except:
                    # If fallback also fails, return the original but cleaned up
                    return response_text.replace("Based on the textbook content:", "").strip()

            return response_text

        except asyncio.TimeoutError:
            logger.error("Request timed out when generating response with OpenAI Agents SDK")
            # Provide a fallback response
            return "I'm sorry, but the request took too long to process. Please try again later."
        except Exception as e:
            logger.error(f"Error generating response with OpenAI Agents SDK: {str(e)}")
            # Check if it's a known API error and provide a more user-friendly response
            error_msg = str(e)
            if "402" in error_msg or "Insufficient credits" in error_msg or "credits" in error_msg.lower() or "quota" in error_msg.lower():
                logger.warning("OpenRouter API key has insufficient credits or quota exceeded, returning context-based response")
                # Return a properly formatted response based on the context even if model is not available
                if retrieved_chunks:
                    # Format the context and ask the agent to synthesize a proper response
                    context_parts = []
                    for i, chunk in enumerate(retrieved_chunks[:3]):  # Use top 3 chunks
                        context_parts.append(f"Source {i+1}: {chunk.content}")

                    context = "\n\n".join(context_parts)

                    # Create a prompt asking for a synthesized response
                    fallback_prompt = f"""
                    Context:
                    {context}

                    Question: {query}

                    Please provide a comprehensive, well-formatted answer based on the provided context that directly addresses the question. Format your response clearly with proper structure.

                    Answer:
                    """

                    # Try to run the agent with the fallback prompt
                    try:
                        response = await Runner.run(self.agent, fallback_prompt)
                        if hasattr(response, 'final_output'):
                            return response.final_output
                        elif hasattr(response, 'content'):
                            return response.content
                        elif hasattr(response, 'text'):
                            return response.text
                        elif isinstance(response, str):
                            return response
                        else:
                            # If agent fails completely, return formatted context
                            most_relevant = max(retrieved_chunks, key=lambda x: x.relevance_score)
                            return f"I found relevant information about '{query}': {most_relevant.content[:600]}..."
                    except:
                        # If agent fails, return formatted context
                        most_relevant = max(retrieved_chunks, key=lambda x: x.relevance_score)
                        return f"I found information about '{query}' in the textbook: {most_relevant.content[:600]}..."
                else:
                    return "I cannot provide a detailed answer without sufficient context."
            elif "404" in error_msg or "No endpoints found" in error_msg or "model" in error_msg.lower():
                logger.error("Model not available on OpenRouter")
                # Return a properly formatted response based on the context even if model is not available
                if retrieved_chunks:
                    # Format the context and ask the agent to synthesize a proper response
                    context_parts = []
                    for i, chunk in enumerate(retrieved_chunks[:3]):  # Use top 3 chunks
                        context_parts.append(f"Source {i+1}: {chunk.content}")

                    context = "\n\n".join(context_parts)

                    # Create a prompt asking for a synthesized response
                    fallback_prompt = f"""
                    Context:
                    {context}

                    Question: {query}

                    Please provide a comprehensive, well-formatted answer based on the provided context that directly addresses the question. Format your response clearly with proper structure.

                    Answer:
                    """

                    # Try to run the agent with the fallback prompt
                    try:
                        response = await Runner.run(self.agent, fallback_prompt)
                        if hasattr(response, 'final_output'):
                            return response.final_output
                        elif hasattr(response, 'content'):
                            return response.content
                        elif hasattr(response, 'text'):
                            return response.text
                        elif isinstance(response, str):
                            return response
                        else:
                            # If agent fails completely, return formatted context
                            most_relevant = max(retrieved_chunks, key=lambda x: x.relevance_score)
                            return f"I found relevant information about '{query}': {most_relevant.content[:600]}..."
                    except:
                        # If agent fails, return formatted context
                        most_relevant = max(retrieved_chunks, key=lambda x: x.relevance_score)
                        return f"I found information about '{query}' in the textbook: {most_relevant.content[:600]}..."
                else:
                    return "I cannot provide a detailed answer without sufficient context."
            elif "interrupted" in error_msg.lower() or "user" in error_msg.lower():
                logger.warning("Request was interrupted")
                return "The request was interrupted. Please try asking your question again."
            elif "API key" in error_msg or "authentication" in error_msg.lower() or "unauthorized" in error_msg.lower():
                logger.error("API authentication failed")
                # Return a properly formatted response based on the context even if authentication fails
                if retrieved_chunks:
                    # Format the context and ask the agent to synthesize a proper response
                    context_parts = []
                    for i, chunk in enumerate(retrieved_chunks[:3]):  # Use top 3 chunks
                        context_parts.append(f"Source {i+1}: {chunk.content}")

                    context = "\n\n".join(context_parts)

                    # Create a prompt asking for a synthesized response
                    fallback_prompt = f"""
                    Context:
                    {context}

                    Question: {query}

                    Please provide a comprehensive, well-formatted answer based on the provided context that directly addresses the question. Format your response clearly with proper structure.

                    Answer:
                    """

                    # Try to run the agent with the fallback prompt
                    try:
                        response = await Runner.run(self.agent, fallback_prompt)
                        if hasattr(response, 'final_output'):
                            return response.final_output
                        elif hasattr(response, 'content'):
                            return response.content
                        elif hasattr(response, 'text'):
                            return response.text
                        elif isinstance(response, str):
                            return response
                        else:
                            # If agent fails completely, return formatted context
                            most_relevant = max(retrieved_chunks, key=lambda x: x.relevance_score)
                            return f"I found relevant information about '{query}': {most_relevant.content[:600]}..."
                    except:
                        # If agent fails, return formatted context
                        most_relevant = max(retrieved_chunks, key=lambda x: x.relevance_score)
                        return f"I found information about '{query}' in the textbook: {most_relevant.content[:600]}..."
                else:
                    return "I cannot provide a detailed answer without sufficient context."
            else:
                logger.error(f"Unexpected error: {str(e)}")
                # As a fallback, return properly formatted context-based response
                if retrieved_chunks:
                    # Format the context and ask the agent to synthesize a proper response
                    context_parts = []
                    for i, chunk in enumerate(retrieved_chunks[:3]):  # Use top 3 chunks
                        context_parts.append(f"Source {i+1}: {chunk.content}")

                    context = "\n\n".join(context_parts)

                    # Create a prompt asking for a synthesized response
                    fallback_prompt = f"""
                    Context:
                    {context}

                    Question: {query}

                    Please provide a comprehensive, well-formatted answer based on the provided context that directly addresses the question. Format your response clearly with proper structure.

                    Answer:
                    """

                    # Try to run the agent with the fallback prompt
                    try:
                        response = await Runner.run(self.agent, fallback_prompt)
                        if hasattr(response, 'final_output'):
                            return response.final_output
                        elif hasattr(response, 'content'):
                            return response.content
                        elif hasattr(response, 'text'):
                            return response.text
                        elif isinstance(response, str):
                            return response
                        else:
                            # If agent fails completely, return formatted context
                            most_relevant = max(retrieved_chunks, key=lambda x: x.relevance_score)
                            return f"I found relevant information about '{query}': {most_relevant.content[:600]}..."
                    except:
                        # If agent fails, return formatted context
                        most_relevant = max(retrieved_chunks, key=lambda x: x.relevance_score)
                        return f"I found information about '{query}' in the textbook: {most_relevant.content[:600]}..."
                else:
                    return "I'm sorry, but I encountered an error while processing your request. Please try again later."

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
            response = await self.generate_response(query, retrieved_chunks)

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