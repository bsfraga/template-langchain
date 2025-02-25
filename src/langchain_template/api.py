"""FastAPI implementation for the LLM service."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Union

from .config import get_settings
from .models.base import LLMManager
from .models.schemas import ContentGeneration, TextAnalysis
from .logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="LangChain Template API",
    description="API for LLM-powered text analysis and generation",
    version="0.1.0",
)

settings = get_settings()
logger.info(f"API initialized with settings: host={settings.api_host}, port={settings.api_port}")


class AnalysisRequest(BaseModel):
    """Request model for text analysis."""
    text: str


class GenerationRequest(BaseModel):
    """Request model for content generation."""
    prompt: str
    context: Union[dict, None] = None


@app.post("/analyze", response_model=TextAnalysis)
async def analyze_text(request: AnalysisRequest) -> TextAnalysis:
    """Analyze text using the LLM."""
    logger.info("Received text analysis request")
    logger.debug(f"Analysis text: {request.text[:100]}...")  # Log first 100 chars
    
    try:
        manager = LLMManager[TextAnalysis](TextAnalysis)
        logger.debug("LLM manager initialized for text analysis")
        
        result = manager.generate_response(
            f"Analyze the following text: {request.text}"
        )
        logger.info("Text analysis completed successfully")
        logger.debug(f"Analysis result: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error during text analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate", response_model=ContentGeneration)
async def generate_content(request: GenerationRequest) -> ContentGeneration:
    """Generate content using the LLM."""
    logger.info("Received content generation request")
    logger.debug(f"Generation prompt: {request.prompt}")
    logger.debug(f"Context provided: {request.context}")
    
    try:
        manager = LLMManager[ContentGeneration](ContentGeneration)
        logger.debug("LLM manager initialized for content generation")
        
        context = request.context or {}
        prompt = f"Generate content based on: {request.prompt}\nContext: {context}"
        
        result = manager.generate_response(prompt)
        logger.info("Content generation completed successfully")
        logger.debug(f"Generated content: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error during content generation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) 