"""Tests for FastAPI endpoints."""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from langchain_template.api import app
from langchain_template.models.schemas import ContentGeneration, TextAnalysis

client = TestClient(app)


@pytest.fixture
def mock_llm_manager():
    """Fixture for mocking LLMManager."""
    with patch("langchain_template.api.LLMManager") as mock:
        manager_instance = AsyncMock()
        mock.return_value = manager_instance
        yield manager_instance


def test_analyze_text(mock_llm_manager):
    """Test text analysis endpoint."""
    # Mock response
    mock_response = TextAnalysis(
        sentiment="positive",
        confidence=0.95,
        key_points=["point1", "point2"],
        summary="Test summary",
    )
    mock_llm_manager.generate_response.return_value = mock_response

    # Test request
    response = client.post("/analyze", json={"text": "Test text"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["sentiment"] == "positive"
    assert data["confidence"] == 0.95
    assert len(data["key_points"]) == 2
    assert data["summary"] == "Test summary"


def test_generate_content(mock_llm_manager):
    """Test content generation endpoint."""
    # Mock response
    mock_response = ContentGeneration(
        title="Test Title",
        content="Generated content",
        tags=["tag1", "tag2"],
        metadata={"author": "test"},
    )
    mock_llm_manager.generate_response.return_value = mock_response

    # Test request
    response = client.post(
        "/generate",
        json={
            "prompt": "Generate test content",
            "context": {"type": "test"},
        },
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Test Title"
    assert data["content"] == "Generated content"
    assert len(data["tags"]) == 2
    assert data["metadata"]["author"] == "test"


def test_analyze_text_error(mock_llm_manager):
    """Test error handling in text analysis endpoint."""
    mock_llm_manager.generate_response.side_effect = Exception("Test error")
    
    response = client.post("/analyze", json={"text": "Test text"})
    assert response.status_code == 500
    assert "Test error" in response.json()["detail"] 