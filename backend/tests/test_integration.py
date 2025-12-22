import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.query_processor import QueryMode
from app.services.session_manager import session_manager
from app.models.query_session import QuerySession
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from unittest.mock import patch


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


def test_integration_global_query_mode(client):
    """Integration test for global query mode across all components."""
    # Mock the LLM service since we don't have API keys
    with patch('app.services.llm_service.LLMService') as mock_llm:
        mock_instance = mock_llm.return_value
        mock_instance.generate_response_with_sources.return_value = (
            "This is a test response based on the book content.",
            []
        )

        # Make a query in global mode
        response = client.post("/api/v1/query/", json={
            "query": "What is retrieval augmented generation?",
            "mode": "global"
        })

        # Should get a successful response
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "sources" in data
        assert data["mode"] == "global"


def test_integration_selected_text_mode(client):
    """Integration test for selected-text-only mode across all components."""
    # Mock the LLM service since we don't have API keys
    with patch('app.services.llm_service.LLMService') as mock_llm:
        mock_instance = mock_llm.return_value
        mock_instance.generate_response_with_sources.return_value = (
            "Based on the selected text, the concept is about RAG.",
            []
        )

        # Make a query in selected-text-only mode
        response = client.post("/api/v1/query/", json={
            "query": "Explain this concept?",
            "mode": "selected-text-only",
            "selected_text": "The concept is retrieval augmented generation which combines information retrieval with text generation."
        })

        # Should get a successful response
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "sources" in data
        assert data["mode"] == "selected-text-only"


def test_integration_session_management(client):
    """Integration test for session management functionality."""
    # Test creating and retrieving a session through the API
    with patch('app.services.llm_service.LLMService') as mock_llm:
        mock_instance = mock_llm.return_value
        mock_instance.generate_response_with_sources.return_value = (
            "This is a test response.",
            []
        )

        # Make a query that creates a session
        response = client.post("/api/v1/query/", json={
            "query": "What is RAG?",
            "mode": "global",
            "session_id": "test-session-123"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "test-session-123"

        # Verify session was created in the database
        from app.utils.database import get_db_session
        async with get_db_session() as db:
            session = db.query(QuerySession).filter(QuerySession.id == "test-session-123").first()
            assert session is not None
            assert session.query_mode == QueryMode.GLOBAL


def test_integration_context_insufficient_error(client):
    """Integration test for context insufficiency handling."""
    # Mock the query processor to return no chunks, triggering the error
    with patch('app.services.query_processor.QueryProcessor._retrieve_from_book_content') as mock_retrieve:
        mock_retrieve.return_value = []  # Return no chunks to trigger ContextInsufficientError

        response = client.post("/api/v1/query/", json={
            "query": "What is the answer to this question?",
            "mode": "global"
        })

        # Should return 404 for context insufficient
        assert response.status_code == 404
        data = response.json()
        assert "response" in data
        assert "No relevant context found to answer the query" in data["response"]


def test_integration_error_handling(client):
    """Integration test for error handling across components."""
    # Test with invalid query to trigger validation error
    response = client.post("/api/v1/query/", json={
        "query": "",  # Empty query should fail validation
        "mode": "global"
    })

    # Should return validation error (422)
    assert response.status_code == 422


def test_integration_all_user_stories_flow(client):
    """Integration test that exercises all user stories in sequence."""
    # Mock the LLM service
    with patch('app.services.llm_service.LLMService') as mock_llm:
        mock_instance = mock_llm.return_value
        mock_instance.generate_response_with_sources.return_value = (
            "This is a response based on the provided context.",
            [
                {
                    "content": "Test content",
                    "source": "test_source",
                    "relevance_score": 0.9,
                    "page_number": 1,
                    "section_title": "Test Section",
                    "citation": "[Test Source, Page 1]"
                }
            ]
        )

        # User Story 1: Global book content querying
        global_response = client.post("/api/v1/query/", json={
            "query": "Explain the main concept?",
            "mode": "global"
        })
        assert global_response.status_code == 200
        global_data = global_response.json()
        assert global_data["mode"] == "global"
        assert "response" in global_data
        assert len(global_data["sources"]) > 0

        # User Story 2: Selected text-only querying
        selected_response = client.post("/api/v1/query/", json={
            "query": "What does this text mean?",
            "mode": "selected-text-only",
            "selected_text": "This text explains the fundamental concept of the system."
        })
        assert selected_response.status_code == 200
        selected_data = selected_response.json()
        assert selected_data["mode"] == "selected-text-only"
        assert "response" in selected_data

        # User Story 3: Context attribution (verified through sources in responses)
        assert "sources" in global_data and "sources" in selected_data
        for source in global_data["sources"] + selected_data["sources"]:
            assert "content" in source
            assert "source" in source
            assert "relevance_score" in source


if __name__ == "__main__":
    pytest.main([__file__])