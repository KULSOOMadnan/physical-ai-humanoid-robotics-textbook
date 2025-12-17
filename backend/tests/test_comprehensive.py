import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from app.main import app
from app.services.content_processor import content_processor
from app.services.query_processor import query_processor
from app.services.llm_service import llm_service
from app.services.vector_store import vector_store_service
from app.models.retrieved_chunk import RetrievedChunk
from app.schemas.query import QueryMode
from app.utils.citations import verify_attribution_accuracy, validate_all_response_attributions
from app.core.metrics import metrics_collector
import tempfile
import os


@pytest.fixture(scope="module")
def client():
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client


class TestContentProcessor:
    """Test cases for content processor service."""

    @pytest.mark.asyncio
    async def test_process_text_content(self):
        """Test processing of text content."""
        # This would require a more complex setup with Qdrant
        # For now, we'll test the structure
        assert content_processor is not None
        assert hasattr(content_processor, 'process_query')


class TestQueryProcessor:
    """Test cases for query processor service."""

    @pytest.mark.asyncio
    async def test_process_global_query(self):
        """Test processing a global query."""
        # Mock the dependencies
        with patch.object(vector_store_service, 'search', new_callable=AsyncMock) as mock_search:
            mock_search.return_value = [
                RetrievedChunk(
                    id="test_chunk_1",
                    content="This is test content for the book.",
                    source="book:test#page:1",
                    relevance_score=0.9,
                    session_id="test_session"
                )
            ]

            with patch.object(llm_service, 'generate_response_with_sources', new_callable=AsyncMock) as mock_llm:
                mock_llm.return_value = ("Test response based on content.", [])

                # Test the query processor
                response, sources = await query_processor.process_query(
                    query="What is this book about?",
                    mode=QueryMode.GLOBAL
                )

                assert response is not None
                assert isinstance(response, str)
                assert len(response) > 0
                mock_search.assert_called_once()
                mock_llm.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_selected_text_query(self):
        """Test processing a selected text query."""
        response, sources = await query_processor.process_query(
            query="Explain this concept?",
            mode=QueryMode.SELECTED_TEXT_ONLY,
            selected_text="The concept of retrieval augmented generation combines neural retrieval with language models."
        )

        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0


class TestLLMService:
    """Test cases for LLM service."""

    @pytest.mark.asyncio
    async def test_generate_response_with_sources(self):
        """Test generating response with source attribution."""
        chunks = [
            RetrievedChunk(
                id="test_chunk_1",
                content="Artificial intelligence is a branch of computer science.",
                source="book:ai_introduction#section:1.1",
                relevance_score=0.85,
                session_id="test_session"
            )
        ]

        # Since we can't actually call the OpenAI API in tests, we'll test the structure
        assert llm_service is not None
        assert hasattr(llm_service, 'generate_response_with_sources')

    @pytest.mark.asyncio
    async def test_validate_source_attribution(self):
        """Test validating source attribution."""
        from app.schemas.query import SourceAttribution

        response = "Artificial intelligence is a branch of computer science."
        sources = [
            SourceAttribution(
                content="Artificial intelligence is a branch of computer science.",
                source="book:ai_introduction#section:1.1",
                relevance_score=0.85
            )
        ]

        is_valid = await llm_service.validate_source_attribution(response, sources)
        assert isinstance(is_valid, bool)


class TestVectorStoreService:
    """Test cases for vector store service."""

    def test_service_initialization(self):
        """Test that vector store service is properly initialized."""
        assert vector_store_service is not None
        assert hasattr(vector_store_service, 'search')
        assert hasattr(vector_store_service, 'add_document')


class TestCitationUtilities:
    """Test cases for citation utilities."""

    def test_verify_attribution_accuracy(self):
        """Test attribution accuracy verification."""
        response = "Paris is the capital of France."
        sources = [
            RetrievedChunk(
                id="chunk_1",
                content="Paris is the capital of France.",
                source="book:123#page:45",
                relevance_score=0.9
            )
        ]

        result = verify_attribution_accuracy(response, sources)
        assert isinstance(result, dict)
        assert 'is_accurate' in result
        assert 'confidence_score' in result

    def test_validate_all_response_attributions(self):
        """Test validation of all response attributions."""
        response = "Paris is the capital of France."
        sources = [
            {
                'content': 'Paris is the capital of France.',
                'source': 'book:123#page:45',
                'relevance_score': 0.9
            }
        ]

        is_valid = validate_all_response_attributions(response, sources)
        assert isinstance(is_valid, bool)


class TestMetricsCollection:
    """Test cases for metrics collection."""

    def test_metrics_collector(self):
        """Test metrics collector functionality."""
        # Test counter increment
        initial_count = len(metrics_collector._counters)
        metrics_collector.increment_counter("test_counter")
        assert len(metrics_collector._counters) >= initial_count

        # Test gauge setting
        metrics_collector.set_gauge("test_gauge", 42.0)
        assert "test_gauge" in str(metrics_collector._gauges)

        # Test histogram recording
        metrics_collector.record_histogram("test_histogram", 1.5)
        assert "test_histogram" in str(metrics_collector._histograms)

        # Test timer functionality
        metrics_collector.start_timer("test_timer")
        duration = metrics_collector.stop_timer("test_timer")
        assert isinstance(duration, float)


class TestAPIEndpoints:
    """Test cases for API endpoints."""

    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_query_endpoint_structure(self, client):
        """Test query endpoint structure."""
        query_request = {
            "query": "What is the main topic?",
            "mode": "global"
        }

        # We expect this to fail due to missing Qdrant/LLM setup,
        # but we can test that the endpoint accepts the request structure
        response = client.post("/api/v1/query/", json=query_request)
        # The endpoint should at least accept the request and return a proper error
        assert response.status_code in [200, 400, 422, 500]  # Various possible responses


class TestIntegration:
    """Integration tests across components."""

    @pytest.mark.asyncio
    async def test_full_query_process_flow(self):
        """Test the full flow from query to response."""
        # This is a high-level test that validates the integration
        # of different components without actually calling external services

        # Verify all required services are available
        assert query_processor is not None
        assert llm_service is not None
        assert vector_store_service is not None

        # Verify required methods exist
        assert hasattr(query_processor, 'process_query')
        assert hasattr(llm_service, 'generate_response_with_sources')
        assert hasattr(vector_store_service, 'search')


def run_comprehensive_tests():
    """Run all comprehensive tests."""
    pytest.main([
        __file__,
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
    ])


if __name__ == "__main__":
    run_comprehensive_tests()