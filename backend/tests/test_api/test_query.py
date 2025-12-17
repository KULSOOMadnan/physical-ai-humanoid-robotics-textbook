import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.config.qdrant import qdrant_config


@pytest.fixture(scope="module")
def client():
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.asyncio
async def test_global_query_functionality(client):
    """
    Test global book content querying functionality.
    This test verifies that users can ask questions about book content
    and receive responses grounded in the book's information.
    """
    # Sample query request for global mode
    query_request = {
        "query": "What is the main concept discussed in the book?",
        "mode": "global",
        "session_id": "test-session-123"
    }

    # Make the query request
    response = client.post("/api/v1/query/", json=query_request)

    # Check that the response is successful
    assert response.status_code == 200

    # Parse the response
    data = response.json()

    # Verify response structure
    assert "response" in data
    assert "sources" in data
    assert "session_id" in data
    assert "timestamp" in data
    assert "mode" in data

    # Verify the mode is global as requested
    assert data["mode"] == "global"

    # Verify that sources are provided (even if empty, they should be present)
    assert isinstance(data["sources"], list)

    # The response should not be empty
    assert len(data["response"]) > 0


@pytest.mark.asyncio
async def test_query_with_session_management(client):
    """
    Test that query functionality properly manages sessions.
    """
    # First query to create a session
    query_request_1 = {
        "query": "What is the book about?",
        "mode": "global",
        "session_id": "test-session-456"
    }

    response_1 = client.post("/api/v1/query/", json=query_request_1)
    assert response_1.status_code == 200

    data_1 = response_1.json()
    assert data_1["session_id"] == "test-session-456"

    # Second query using the same session
    query_request_2 = {
        "query": "Can you elaborate on the main topic?",
        "mode": "global",
        "session_id": "test-session-456"  # Same session
    }

    response_2 = client.post("/api/v1/query/", json=query_request_2)
    assert response_2.status_code == 200

    data_2 = response_2.json()
    assert data_2["session_id"] == "test-session-456"


@pytest.mark.asyncio
async def test_query_without_session_id(client):
    """
    Test that a session ID is generated when not provided.
    """
    query_request = {
        "query": "What are the key points?",
        "mode": "global"
        # No session_id provided - should be generated
    }

    response = client.post("/api/v1/query/", json=query_request)
    assert response.status_code == 200

    data = response.json()
    assert "session_id" in data
    assert data["session_id"] is not None
    assert len(data["session_id"]) > 0  # Should have a generated session ID


@pytest.mark.asyncio
async def test_source_attribution(client):
    """
    Test that responses include proper source attribution.
    """
    query_request = {
        "query": "Give me some information from the book",
        "mode": "global",
        "session_id": "test-session-789"
    }

    response = client.post("/api/v1/query/", json=query_request)
    assert response.status_code == 200

    data = response.json()

    # Even if no sources are found, the structure should be valid
    assert "sources" in data
    assert isinstance(data["sources"], list)

    # If sources exist, they should have the required fields
    for source in data["sources"]:
        assert "content" in source
        assert "source" in source
        assert "relevance_score" in source


if __name__ == "__main__":
    pytest.main([__file__])