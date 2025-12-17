import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from app.services.query_processor import QueryProcessor, query_processor
from app.models.query_session import QueryMode
from app.core.exceptions import ContextInsufficientError


@pytest.mark.asyncio
async def test_selected_text_only_mode_with_valid_content():
    """Test that selected-text-only mode works with valid selected text."""
    query = "What is the main concept?"
    selected_text = "The main concept is that retrieval-augmented generation combines information retrieval with text generation to provide accurate answers based on specific sources."
    mode = QueryMode.SELECTED_TEXT_ONLY

    # This should not raise an exception and should return a response with sources
    response, sources = await query_processor.process_query(
        query=query,
        mode=mode,
        selected_text=selected_text
    )

    assert isinstance(response, str)
    assert len(response) > 0
    assert isinstance(sources, list)
    # The response should be generated based on the selected text


@pytest.mark.asyncio
async def test_selected_text_only_mode_with_empty_text():
    """Test that selected-text-only mode fails with empty selected text."""
    query = "What is the main concept?"
    selected_text = ""
    mode = QueryMode.SELECTED_TEXT_ONLY

    with pytest.raises(ContextInsufficientError):
        await query_processor.process_query(
            query=query,
            mode=mode,
            selected_text=selected_text
        )


@pytest.mark.asyncio
async def test_selected_text_only_mode_with_short_text():
    """Test that selected-text-only mode fails with very short selected text."""
    query = "What is the main concept?"
    selected_text = "Hi."
    mode = QueryMode.SELECTED_TEXT_ONLY

    # With the updated validation, very short text should return an empty list
    # which should trigger ContextInsufficientError
    with pytest.raises(ContextInsufficientError):
        await query_processor.process_query(
            query=query,
            mode=mode,
            selected_text=selected_text
        )


@pytest.mark.asyncio
async def test_selected_text_only_mode_without_selected_text():
    """Test that selected-text-only mode fails when no selected text is provided."""
    query = "What is the main concept?"
    selected_text = None
    mode = QueryMode.SELECTED_TEXT_ONLY

    with pytest.raises(ContextInsufficientError):
        await query_processor.process_query(
            query=query,
            mode=mode,
            selected_text=selected_text
        )


@pytest.mark.asyncio
async def test_global_mode_still_works():
    """Test that global mode still works normally."""
    query = "What is the main concept?"
    mode = QueryMode.GLOBAL

    # Mock the _retrieve_from_book_content method to return some test data
    original_method = query_processor._retrieve_from_book_content
    query_processor._retrieve_from_book_content = AsyncMock(return_value=[
        MagicMock(content="Test content", source="test_source", relevance_score=0.9, session_id="test")
    ])

    try:
        response, sources = await query_processor.process_query(
            query=query,
            mode=mode
        )

        assert isinstance(response, str)
        assert len(response) > 0
        assert isinstance(sources, list)
    finally:
        # Restore original method
        query_processor._retrieve_from_book_content = original_method


@pytest.mark.asyncio
async def test_selected_text_refusal_when_irrelevant():
    """Test refusal behavior when selected text lacks relevant information for the query."""
    query = "What is the mathematical formula for gravitational force?"
    # This selected text is about a completely different topic
    selected_text = "The weather today is sunny and warm. The sky is blue. Birds are singing."
    mode = QueryMode.SELECTED_TEXT_ONLY

    # The validation should detect that the selected text doesn't contain relevant info
    # and return an empty list, which should trigger ContextInsufficientError
    with pytest.raises(ContextInsufficientError):
        await query_processor.process_query(
            query=query,
            mode=mode,
            selected_text=selected_text
        )


if __name__ == "__main__":
    pytest.main([__file__])