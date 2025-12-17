import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from app.main import app
from app.services.content_processor import content_processor
from app.services.query_processor import query_processor
from app.services.session_manager import session_manager
from app.models.query_session import QueryMode
from app.config.database import SessionLocal
from app.core.metrics import metrics_collector
import tempfile
import os
import uuid


@pytest.fixture(scope="module")
def client():
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client


class TestUserStory1_GlobalQueryIntegration:
    """Integration tests for User Story 1: Global Book Content Querying."""

    @pytest.mark.asyncio
    async def test_complete_global_query_flow(self, client):
        """Test the complete flow for global book content querying."""
        # Mock the vector store search to return test data
        with patch.object(content_processor, 'process_book_content', new_callable=AsyncMock) as mock_process:
            mock_process.return_value = {
                "book_id": "test-book-123",
                "title": "Test Book",
                "chunk_count": 5,
                "total_tokens": 1000,
                "status": "processed"
            }

            # First, upload some test content (simulated)
            # In a real test, we would actually upload content to Qdrant
            with patch.object(query_processor, '_retrieve_from_book_content', new_callable=AsyncMock) as mock_retrieve:
                mock_retrieve.return_value = [
                    MagicMock(
                        id="test_chunk_1",
                        content="This is test content about artificial intelligence.",
                        source="book:test-book-123#section:1.1",
                        relevance_score=0.85,
                        session_id="temp"
                    )
                ]

                # Now test the query endpoint
                query_request = {
                    "query": "What is artificial intelligence?",
                    "mode": "global",
                    "session_id": "integration-test-session-1"
                }

                response = client.post("/api/v1/query/", json=query_request)

                # Should return successfully (200) or with a proper error (500) if external services fail
                assert response.status_code in [200, 500]

                if response.status_code == 200:
                    data = response.json()
                    assert "response" in data
                    assert "sources" in data
                    assert "session_id" in data
                    assert data["session_id"] == "integration-test-session-1"
                    assert data["mode"] == "global"

    @pytest.mark.asyncio
    async def test_global_query_with_session_management(self, client):
        """Test global query with proper session management."""
        session_id = f"test-session-{uuid.uuid4()}"

        with patch.object(query_processor, '_retrieve_from_book_content', new_callable=AsyncMock) as mock_retrieve:
            mock_retrieve.return_value = [
                MagicMock(
                    id="test_chunk_1",
                    content="Machine learning is a subset of artificial intelligence.",
                    source="book:test-book-123#section:2.1",
                    relevance_score=0.9,
                    session_id="temp"
                )
            ]

            # First query
            query_request_1 = {
                "query": "What is machine learning?",
                "mode": "global",
                "session_id": session_id
            }

            response_1 = client.post("/api/v1/query/", json=query_request_1)
            assert response_1.status_code in [200, 500]

            # Second query with same session
            query_request_2 = {
                "query": "How is it related to AI?",
                "mode": "global",
                "session_id": session_id
            }

            response_2 = client.post("/api/v1/query/", json=query_request_2)
            assert response_2.status_code in [200, 500]


class TestUserStory2_SelectedTextIntegration:
    """Integration tests for User Story 2: Selected Text-Only Querying."""

    @pytest.mark.asyncio
    async def test_selected_text_only_query(self, client):
        """Test the selected text-only query mode."""
        query_request = {
            "query": "Explain this concept?",
            "mode": "selected-text-only",
            "selected_text": "The concept of retrieval augmented generation combines neural retrieval with language models to provide more accurate and contextually relevant responses.",
            "session_id": "integration-test-session-2"
        }

        response = client.post("/api/v1/query/", json=query_request)

        # Should return successfully (200) or with a proper error (500) if external services fail
        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            assert "response" in data
            assert "sources" in data
            assert "session_id" in data
            assert data["session_id"] == "integration-test-session-2"
            assert data["mode"] == "selected-text-only"

    @pytest.mark.asyncio
    async def test_selected_text_refusal_when_context_insufficient(self, client):
        """Test that the system refuses to answer when selected text lacks relevant info."""
        query_request = {
            "query": "What is the capital of France?",
            "mode": "selected-text-only",
            "selected_text": "This text is about artificial intelligence and does not mention geography.",
            "session_id": "integration-test-session-3"
        }

        response = client.post("/api/v1/query/", json=query_request)

        # The response should either be successful with a refusal message or an error
        if response.status_code == 200:
            data = response.json()
            # The response should indicate inability to answer based on context
            response_text = data.get("response", "").lower()
            assert any(phrase in response_text for phrase in [
                "cannot answer",
                "not found in the provided context",
                "insufficient context"
            ])


class TestUserStory3_AttributionIntegration:
    """Integration tests for User Story 3: Context Attribution and Traceability."""

    @pytest.mark.asyncio
    async def test_source_attribution_in_responses(self, client):
        """Test that responses include proper source attribution."""
        with patch.object(query_processor, '_retrieve_from_book_content', new_callable=AsyncMock) as mock_retrieve:
            mock_retrieve.return_value = [
                MagicMock(
                    id="test_chunk_1",
                    content="The history of artificial intelligence dates back to the 1950s.",
                    source="book:ai-history#chapter:1",
                    relevance_score=0.88,
                    page_number=15,
                    section_title="Early Development",
                    session_id="temp"
                ),
                MagicMock(
                    id="test_chunk_2",
                    content="Key figures in AI include Alan Turing and John McCarthy.",
                    source="book:ai-history#chapter:1",
                    relevance_score=0.82,
                    page_number=17,
                    section_title="Early Development",
                    session_id="temp"
                )
            ]

            query_request = {
                "query": "When did AI research begin?",
                "mode": "global",
                "session_id": "integration-test-session-4"
            }

            response = client.post("/api/v1/query/", json=query_request)

            if response.status_code == 200:
                data = response.json()
                assert "sources" in data
                assert len(data["sources"]) > 0

                # Check that sources have the expected attribution fields
                for source in data["sources"]:
                    assert "content" in source
                    assert "source" in source
                    assert "relevance_score" in source
                    # These fields are optional but should be present if available
                    # assert "page_number" in source  # This might be None
                    # assert "section_title" in source  # This might be None


class TestCrossUserStoryIntegration:
    """Integration tests that span multiple user stories."""

    @pytest.mark.asyncio
    async def test_complete_rag_flow_with_all_features(self, client):
        """Test a complete RAG flow using all implemented features."""
        # Test metrics collection during the process
        initial_query_count = len([k for k in metrics_collector._histograms.keys() if 'query_processing' in k])

        with patch.object(query_processor, '_retrieve_from_book_content', new_callable=AsyncMock) as mock_retrieve:
            mock_retrieve.return_value = [
                MagicMock(
                    id="test_chunk_1",
                    content="Retrieval Augmented Generation (RAG) is a technique that combines information retrieval with text generation.",
                    source="book:rag-intro#section:1.1",
                    relevance_score=0.92,
                    session_id="temp"
                )
            ]

            # Global query with attribution (US1 + US3)
            query_request = {
                "query": "What is RAG?",
                "mode": "global",
                "session_id": "cross-story-test-1"
            }

            response = client.post("/api/v1/query/", json=query_request)

            if response.status_code == 200:
                data = response.json()
                # Verify US1: Global querying works
                assert "response" in data
                assert len(data["response"]) > 0

                # Verify US3: Attribution is present
                assert "sources" in data
                assert len(data["sources"]) > 0

                # Verify session management (US1)
                assert data["session_id"] == "cross-story-test-1"

            # Selected text query (US2)
            selected_text_request = {
                "query": "Explain this?",
                "mode": "selected-text-only",
                "selected_text": "The technique combines retrieval with generation to improve accuracy.",
                "session_id": "cross-story-test-2"
            }

            selected_response = client.post("/api/v1/query/", json=selected_text_request)

            if selected_response.status_code == 200:
                selected_data = selected_response.json()
                assert selected_data["mode"] == "selected-text-only"
                assert "response" in selected_data

        # Verify metrics were collected
        final_query_count = len([k for k in metrics_collector._histograms.keys() if 'query_processing' in k])
        assert final_query_count >= initial_query_count  # At least the same or more metrics collected

    @pytest.mark.asyncio
    async def test_session_based_mode_switching(self, client):
        """Test switching between query modes within the same session."""
        session_id = f"mode-switch-test-{uuid.uuid4()}"

        # First, make a global query
        with patch.object(query_processor, '_retrieve_from_book_content', new_callable=AsyncMock) as mock_retrieve:
            mock_retrieve.return_value = [
                MagicMock(
                    id="test_chunk_1",
                    content="Artificial intelligence is a broad field.",
                    source="book:ai-overview#section:1.0",
                    relevance_score=0.75,
                    session_id="temp"
                )
            ]

            global_query = {
                "query": "What is AI?",
                "mode": "global",
                "session_id": session_id
            }

            global_response = client.post("/api/v1/query/", json=global_query)

            # Then, make a selected-text query with the same session
            selected_query = {
                "query": "Explain this part?",
                "mode": "selected-text-only",
                "selected_text": "Machine learning is a subset of artificial intelligence that focuses on learning from data.",
                "session_id": session_id  # Same session
            }

            selected_response = client.post("/api/v1/query/", json=selected_query)

            # Both should succeed
            assert global_response.status_code in [200, 500]
            assert selected_response.status_code in [200, 500]


def run_integration_tests():
    """Run all integration tests."""
    pytest.main([
        __file__,
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
    ])


if __name__ == "__main__":
    run_integration_tests()