"""Tests for LLM models and schemas."""

import pytest
from pydantic import ValidationError

from langchain_template.models.schemas import ContentGeneration, TextAnalysis


def test_text_analysis_schema():
    """Test TextAnalysis schema validation."""
    # Valid data
    data = {
        "sentiment": "positive",
        "confidence": 0.95,
        "key_points": ["point1", "point2"],
        "summary": "Test summary",
    }
    analysis = TextAnalysis(**data)
    assert analysis.sentiment == "positive"
    assert analysis.confidence == 0.95
    assert len(analysis.key_points) == 2
    assert analysis.summary == "Test summary"

    # Invalid confidence score
    with pytest.raises(ValidationError):
        TextAnalysis(
            sentiment="positive",
            confidence=1.5,  # Should be between 0 and 1
            key_points=["point1"],
        )


def test_content_generation_schema():
    """Test ContentGeneration schema validation."""
    # Valid data
    data = {
        "title": "Test Title",
        "content": "Test content",
        "tags": ["tag1", "tag2"],
        "metadata": {"author": "test"},
    }
    content = ContentGeneration(**data)
    assert content.title == "Test Title"
    assert content.content == "Test content"
    assert len(content.tags) == 2
    assert content.metadata["author"] == "test"

    # Missing required fields
    with pytest.raises(ValidationError):
        ContentGeneration(
            tags=["tag1"],
            metadata={},
        ) 