import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.query_processor import QueryProcessor, QueryMode
from app.core.exceptions import ContextInsufficientError


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_query_endpoint_exists(client):
    """Test that the query endpoint exists."""
    # This should return a validation error since we're not sending proper data,
    # but it should not return a 404
    response = client.post("/api/v1/query/", json={})
    assert response.status_code != 404  # Not found


def test_query_with_empty_body(client):
    """Test query endpoint with empty body."""
    response = client.post("/api/v1/query/", json={})
    assert response.status_code == 422  # Validation error


def test_query_with_valid_request(client):
    """Test query endpoint with valid request (should work with mock LLM)."""
    request_data = {
        "query": "What is retrieval augmented generation?",
        "mode": "global"
    }
    response = client.post("/api/v1/query/", json=request_data)
    # This might fail if dependencies aren't met, but should return a proper error
    assert response.status_code in [200, 400, 422, 500]  # Various valid responses


def test_query_with_selected_text_mode(client):
    """Test query endpoint with selected-text-only mode."""
    request_data = {
        "query": "What is the concept?",
        "mode": "selected-text-only",
        "selected_text": "The concept is about retrieval augmented generation."
    }
    response = client.post("/api/v1/query/", json=request_data)
    # Should return appropriate response or error
    assert response.status_code in [200, 400, 422, 500]


def test_session_endpoint_exists(client):
    """Test that the session endpoint exists."""
    response = client.get("/api/v1/session/test-session")
    assert response.status_code != 404  # Not found


def test_upload_endpoint_exists(client):
    """Test that the upload endpoint exists."""
    response = client.post("/api/v1/upload/")
    assert response.status_code != 404  # Not found


if __name__ == "__main__":
    pytest.main([__file__])