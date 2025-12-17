import re
from typing import List, Dict, Any, Optional
from app.models.retrieved_chunk import RetrievedChunk


def format_citation(source: str, page_info: Optional[str] = None) -> str:
    """
    Format a citation for a retrieved source.

    Args:
        source: The source identifier (e.g., "book:123#section:456")
        page_info: Optional page information

    Returns:
        Formatted citation string
    """
    # Extract book ID and section from source if in format "book:ID#section:SECTION"
    if source.startswith("book:"):
        parts = source.split("#")
        book_part = parts[0] if len(parts) > 0 else source
        section_part = parts[1] if len(parts) > 1 else ""

        book_id = book_part.replace("book:", "")
        section = section_part.replace("section:", "") if "section:" in section_part else section_part
        page = page_info or ""

        if section and page:
            return f"[Book {book_id}, Section {section}, Page {page}]"
        elif section:
            return f"[Book {book_id}, Section {section}]"
        elif page:
            return f"[Book {book_id}, Page {page}]"
        else:
            return f"[Book {book_id}]"
    elif source == "user_selected_text":
        return "[Selected Text]"
    else:
        # For other source formats, return as is
        return f"[{source}]"


def format_multiple_citations(sources: List[Dict[str, Any]]) -> str:
    """
    Format multiple citations into a single string.

    Args:
        sources: List of source dictionaries

    Returns:
        Formatted citations string
    """
    if not sources:
        return ""

    citations = []
    for i, source in enumerate(sources, 1):
        source_ref = source.get('source', f'Unknown Source {i}')
        content = source.get('content', '')[:100] + "..." if len(source.get('content', '')) > 100 else source.get('content', '')
        citations.append(f"{i}. {format_citation(source_ref)}: {content}")

    return "\n".join(citations)


def extract_quote_highlights(content: str, query: str) -> List[str]:
    """
    Extract relevant quote highlights from content based on the query.

    Args:
        content: The content to extract quotes from
        query: The query to match against

    Returns:
        List of relevant quote highlights
    """
    # Simple keyword-based extraction - in a real implementation,
    # this could use more sophisticated NLP techniques
    query_words = set(re.findall(r'\w+', query.lower()))

    sentences = re.split(r'[.!?]+', content)
    highlights = []

    for sentence in sentences:
        sentence_lower = sentence.lower()
        sentence_words = set(re.findall(r'\w+', sentence_lower))

        # If there's overlap between query words and sentence words
        if query_words.intersection(sentence_words):
            clean_sentence = sentence.strip()
            if clean_sentence:
                highlights.append(clean_sentence)

    return highlights


def format_context_attribution(retrieved_chunks: List[RetrievedChunk], query: str) -> str:
    """
    Format comprehensive context attribution for a response.

    Args:
        retrieved_chunks: List of retrieved chunks with sources
        query: The original query

    Returns:
        Formatted attribution string
    """
    if not retrieved_chunks:
        return "No sources used."

    attribution_parts = ["Sources used for this response:"]

    for i, chunk in enumerate(retrieved_chunks, 1):
        citation = format_citation(chunk.source)
        highlights = extract_quote_highlights(chunk.content, query)

        attribution_parts.append(f"{i}. {citation}")

        if highlights:
            attribution_parts.append(f"   Excerpt: {'; '.join(highlights[:2])}")  # Limit to first 2 highlights

        # Add relevance score if available
        if hasattr(chunk, 'relevance_score'):
            attribution_parts.append(f"   Relevance: {chunk.relevance_score:.2f}")

    return "\n".join(attribution_parts)


def validate_citation_format(citation: str) -> bool:
    """
    Validate that a citation is in the expected format.

    Args:
        citation: The citation string to validate

    Returns:
        True if valid, False otherwise
    """
    # Check if citation starts and ends with brackets
    if not citation.startswith("[") or not citation.endswith("]"):
        return False

    # Check if there's content between brackets
    content = citation[1:-1].strip()
    if not content:
        return False

    return True


def verify_attribution_accuracy(response: str, sources: List[RetrievedChunk]) -> Dict[str, Any]:
    """
    Verify that the response is properly attributed to the provided sources.

    Args:
        response: The generated response
        sources: List of sources used to generate the response

    Returns:
        Dictionary with verification results:
        - 'is_accurate': Whether the response accurately reflects the sources
        - 'missing_attributions': List of sources not properly attributed
        - 'excessive_attributions': List of attributions not supported by sources
        - 'confidence_score': Confidence level in attribution accuracy (0.0-1.0)
    """
    # Initialize verification results
    results = {
        'is_accurate': True,
        'missing_attributions': [],
        'excessive_attributions': [],
        'confidence_score': 1.0,
        'details': []
    }

    # If no sources were provided but a response was generated, that's a problem
    if not sources and response.strip():
        results['is_accurate'] = False
        results['confidence_score'] = 0.0
        results['details'].append("Response generated without any sources")
        return results

    # If sources were provided but response is empty, that's also a problem
    if sources and not response.strip():
        results['is_accurate'] = False
        results['confidence_score'] = 0.0
        results['details'].append("No response generated despite having sources")
        return results

    # Check if the response contains information that can be traced back to sources
    response_lower = response.lower()
    source_contents = [chunk.content.lower() for chunk in sources]

    # Calculate overlap between response and sources
    total_overlap_score = 0
    for source_content in source_contents:
        # Simple word overlap calculation
        response_words = set(response_lower.split())
        source_words = set(source_content.split())

        if response_words and source_words:
            overlap = len(response_words.intersection(source_words))
            max_possible = min(len(response_words), len(source_words))
            if max_possible > 0:
                overlap_score = overlap / max_possible
                total_overlap_score += overlap_score

    # Normalize the overlap score based on number of sources
    if sources:
        avg_overlap_score = total_overlap_score / len(sources)
    else:
        avg_overlap_score = 0

    # Set confidence based on overlap
    results['confidence_score'] = avg_overlap_score

    # If overlap is very low, mark as potentially inaccurate
    if avg_overlap_score < 0.1:  # Less than 10% overlap
        results['is_accurate'] = False
        results['details'].append(f"Low content overlap between response and sources ({avg_overlap_score:.2f})")

    # Check if all sources were appropriately referenced in the response
    for i, source in enumerate(sources):
        source_in_response = any(word in response_lower for word in source.content.lower().split()[:10])  # Check first 10 words
        if not source_in_response and len(source.content) > 20:  # Only for substantial content
            results['missing_attributions'].append(f"Source {i+1}: {source.source}")

    return results


def validate_all_response_attributions(response: str, sources: List[Dict[str, Any]]) -> bool:
    """
    Validate that all responses include proper source attribution.

    Args:
        response: The generated response
        sources: List of source attributions

    Returns:
        True if all attributions are valid, False otherwise
    """
    # Check if sources list is properly structured
    if not isinstance(sources, list):
        return False

    # Validate each source attribution
    for source in sources:
        if not isinstance(source, dict):
            return False

        # Check required fields
        required_fields = ['content', 'source', 'relevance_score']
        for field in required_fields:
            if field not in source:
                return False

    # If we have sources but the response doesn't acknowledge them,
    # this may indicate missing attribution in the response itself
    if sources and len(sources) > 0:
        # In a real implementation, we might check if the response text
        # explicitly mentions source information or follows a format that
        # indicates attribution has been properly incorporated
        pass  # For now, we validate the structure of the attributions

    return True