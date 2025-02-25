"""Schema definitions for LLM responses."""

from typing import List, Optional

from pydantic import BaseModel, Field, model_validator

from ..logger import get_logger

logger = get_logger(__name__)


class TextAnalysis(BaseModel):
    """Example schema for text analysis response."""
    
    sentiment: str = Field(..., description="Sentiment of the text")
    confidence: float = Field(..., description="Confidence score", ge=0, le=1)
    key_points: List[str] = Field(default_factory=list, description="Key points from the text")
    summary: Optional[str] = Field(None, description="Optional summary of the text")
    
    @model_validator(mode='after')
    def log_validation(self) -> 'TextAnalysis':
        """Log the validation of the model."""
        logger.debug(f"Validated TextAnalysis: sentiment={self.sentiment}, confidence={self.confidence}")
        logger.debug(f"Key points count: {len(self.key_points)}")
        if self.summary:
            logger.debug(f"Summary length: {len(self.summary)}")
        return self


class ContentGeneration(BaseModel):
    """Example schema for content generation response."""
    
    title: str = Field(..., description="Generated content title")
    content: str = Field(..., description="Generated content body")
    tags: List[str] = Field(default_factory=list, description="Content tags")
    metadata: dict = Field(default_factory=dict, description="Additional metadata")
    
    @model_validator(mode='after')
    def log_validation(self) -> 'ContentGeneration':
        """Log the validation of the model."""
        logger.debug(f"Validated ContentGeneration: title='{self.title}'")
        logger.debug(f"Content length: {len(self.content)} chars")
        logger.debug(f"Tags: {self.tags}")
        logger.debug(f"Metadata keys: {list(self.metadata.keys())}")
        return self 