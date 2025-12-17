import pytest
from app.utils.citations import verify_attribution_accuracy, validate_all_response_attributions
from app.models.retrieved_chunk import RetrievedChunk


def test_attribution_verification_with_matching_content():
    """Test attribution verification when response matches sources."""
    response = "The main concept is retrieval-augmented generation, which combines information retrieval with text generation to provide accurate answers based on specific sources."

    sources = [
        RetrievedChunk(
            id="chunk1",
            content="Retrieval-augmented generation combines information retrieval with text generation to provide accurate answers based on specific sources.",
            source="book:123#section:456",
            relevance_score=0.9,
            session_id="test"
        )
    ]

    results = verify_attribution_accuracy(response, sources)

    assert results['is_accurate'] == True
    assert results['confidence_score'] > 0.5  # Should have good overlap
    assert len(results['missing_attributions']) == 0


def test_attribution_verification_with_no_sources():
    """Test attribution verification when no sources are provided."""
    response = "This is a response without any sources."
    sources = []

    results = verify_attribution_accuracy(response, sources)

    assert results['is_accurate'] == False
    assert results['confidence_score'] == 0.0
    assert "Response generated without any sources" in results['details']


def test_attribution_verification_with_empty_response():
    """Test attribution verification when response is empty but sources exist."""
    response = ""
    sources = [
        RetrievedChunk(
            id="chunk1",
            content="This is some content that should be used in the response.",
            source="book:123#section:456",
            relevance_score=0.9,
            session_id="test"
        )
    ]

    results = verify_attribution_accuracy(response, sources)

    assert results['is_accurate'] == False
    assert results['confidence_score'] == 0.0
    assert "No response generated despite having sources" in results['details']


def test_attribution_verification_with_mismatched_content():
    """Test attribution verification when response doesn't match sources."""
    response = "The weather is sunny today and the sky is blue."

    sources = [
        RetrievedChunk(
            id="chunk1",
            content="Retrieval-augmented generation combines information retrieval with text generation.",
            source="book:123#section:456",
            relevance_score=0.9,
            session_id="test"
        )
    ]

    results = verify_attribution_accuracy(response, sources)

    assert results['is_accurate'] == False
    assert results['confidence_score'] < 0.1  # Very low overlap
    assert "Low content overlap between response and sources" in results['details']


def test_validate_response_attributions_valid():
    """Test validation of properly structured response attributions."""
    response = "Based on the book content, the answer is..."
    sources = [
        {
            'content': 'Retrieval-augmented generation combines information retrieval with text generation.',
            'source': 'book:123#section:456',
            'relevance_score': 0.9
        }
    ]

    is_valid = validate_all_response_attributions(response, sources)

    assert is_valid == True


def test_validate_response_attributions_invalid_missing_fields():
    """Test validation of response attributions with missing fields."""
    response = "Based on the book content, the answer is..."
    sources = [
        {
            'content': 'Retrieval-augmented generation combines information retrieval with text generation.',
            'source': 'book:123#section:456'
            # Missing 'relevance_score' field
        }
    ]

    is_valid = validate_all_response_attributions(response, sources)

    assert is_valid == False


def test_validate_response_attributions_invalid_not_list():
    """Test validation of response attributions when sources is not a list."""
    response = "Based on the book content, the answer is..."
    sources = "not a list"  # Invalid type

    is_valid = validate_all_response_attributions(response, sources)

    assert is_valid == False


def test_validate_response_attributions_empty_list():
    """Test validation of response attributions with empty list."""
    response = "Based on the book content, the answer is..."
    sources = []

    is_valid = validate_all_response_attributions(response, sources)

    assert is_valid == True  # Empty list is valid structure-wise


if __name__ == "__main__":
    pytest.main([__file__])