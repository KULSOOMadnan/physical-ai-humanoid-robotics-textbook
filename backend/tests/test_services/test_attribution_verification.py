import pytest
from app.utils.citations import verify_attribution_accuracy, validate_all_response_attributions
from app.models.retrieved_chunk import RetrievedChunk


def test_single_source_attribution_accuracy():
    """Test attribution accuracy for responses with a single source."""
    response = "The capital of France is Paris, which is located in the northern part of the country."
    sources = [
        RetrievedChunk(
            id="chunk_1",
            content="Paris is the capital of France and is located in the northern part of the country.",
            source="book:123#page:45",
            relevance_score=0.9
        )
    ]

    result = verify_attribution_accuracy(response, sources)

    assert result['is_accurate'] == True
    assert result['confidence_score'] > 0.5
    assert len(result['missing_attributions']) == 0
    assert len(result['excessive_attributions']) == 0


def test_multi_source_attribution_accuracy():
    """Test attribution accuracy for responses with multiple sources."""
    response = "The Eiffel Tower is in Paris, France. Paris is the capital of France."
    sources = [
        RetrievedChunk(
            id="chunk_1",
            content="The Eiffel Tower is located in Paris, France.",
            source="book:123#page:45",
            relevance_score=0.8
        ),
        RetrievedChunk(
            id="chunk_2",
            content="Paris is the capital of France.",
            source="book:123#page:46",
            relevance_score=0.9
        )
    ]

    result = verify_attribution_accuracy(response, sources)

    assert result['is_accurate'] == True
    assert result['confidence_score'] > 0.5
    assert len(result['missing_attributions']) == 0
    assert len(result['excessive_attributions']) == 0


def test_no_sources_with_response():
    """Test when a response is generated without any sources."""
    response = "The capital of France is Paris."
    sources = []

    result = verify_attribution_accuracy(response, sources)

    assert result['is_accurate'] == False
    assert result['confidence_score'] == 0.0
    assert len(result['details']) > 0


def test_empty_response_with_sources():
    """Test when sources exist but response is empty."""
    response = ""
    sources = [
        RetrievedChunk(
            id="chunk_1",
            content="Paris is the capital of France.",
            source="book:123#page:45",
            relevance_score=0.9
        )
    ]

    result = verify_attribution_accuracy(response, sources)

    assert result['is_accurate'] == False
    assert result['confidence_score'] == 0.0
    assert len(result['details']) > 0


def test_low_overlap_response():
    """Test when response has low overlap with sources."""
    response = "The capital of Japan is Tokyo, which is located in the eastern part of the country."
    sources = [
        RetrievedChunk(
            id="chunk_1",
            content="Paris is the capital of France and is located in the northern part of the country.",
            source="book:123#page:45",
            relevance_score=0.9
        )
    ]

    result = verify_attribution_accuracy(response, sources)

    assert result['is_accurate'] == False
    assert result['confidence_score'] < 0.1
    assert len(result['details']) > 0


def test_valid_response_attributions():
    """Test validation of response attributions structure."""
    response = "The capital of France is Paris."
    sources = [
        {
            'content': 'Paris is the capital of France.',
            'source': 'book:123#page:45',
            'relevance_score': 0.9
        }
    ]

    is_valid = validate_all_response_attributions(response, sources)
    assert is_valid == True


def test_invalid_response_attributions_missing_fields():
    """Test validation when source attributions are missing required fields."""
    response = "The capital of France is Paris."
    sources = [
        {
            'content': 'Paris is the capital of France.',
            'source': 'book:123#page:45'
            # Missing 'relevance_score'
        }
    ]

    is_valid = validate_all_response_attributions(response, sources)
    assert is_valid == False


def test_invalid_response_attributions_wrong_type():
    """Test validation when sources is not a list."""
    response = "The capital of France is Paris."
    sources = "This is not a list"

    is_valid = validate_all_response_attributions(response, sources)
    assert is_valid == False


if __name__ == "__main__":
    pytest.main([__file__])