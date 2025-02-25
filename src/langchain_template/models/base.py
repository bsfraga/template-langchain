"""Base model integration with LangChain and Instructor."""

from typing import Any, Generic, Type, TypeVar, Union

import instructor
from langchain_core.messages import HumanMessage, SystemMessage
from openai import OpenAI
from pydantic import BaseModel

from ..config import Settings, get_settings
from ..logger import get_logger

logger = get_logger(__name__)

T = TypeVar("T", bound=BaseModel)

class LLMManager(Generic[T]):
    """Base LLM manager for handling model interactions."""
    
    def __init__(
        self,
        response_model: Type[T],
        settings: Union[Settings, None] = None,
    ):
        """Initialize the LLM manager.
        
        Args:
            response_model: Pydantic model for response validation
            settings: Application settings
        """
        logger.info(f"Initializing LLM manager with response model: {response_model.__name__}")
        self.settings = settings or get_settings()
        self.response_model = response_model
        
        # Initialize OpenAI client with instructor patch
        logger.debug(f"Setting up OpenAI client with model: {self.settings.model_name}")
        openai_client = OpenAI(
            api_key=self.settings.openai_api_key,
            base_url="https://api.openai.com/v1",  # Default OpenAI base URL
        )
        self.llm = instructor.patch(openai_client)
        logger.info("LLM manager initialization completed")
    
    def _get_message_role(self, message: Union[SystemMessage, HumanMessage]) -> str:
        """Get the appropriate role for the message type."""
        if isinstance(message, SystemMessage):
            return "system"
        return "user"  # HumanMessage maps to 'user' in OpenAI's API
    
    def generate_response(self, prompt: str, **kwargs: Any) -> T:
        """Generate a response from the LLM.
        
        Args:
            prompt: Input prompt for the LLM
            **kwargs: Additional arguments for the LLM
        
        Returns:
            Validated response using the response model
        """
        logger.info("Generating LLM response")
        logger.debug(f"Prompt: {prompt[:100]}...")  # Log first 100 chars
        logger.debug(f"Additional arguments: {kwargs}")
        
        messages = [
            SystemMessage(content="You are a helpful AI assistant that provides structured responses."),
            HumanMessage(content=prompt)
        ]
        
        try:
            logger.debug(f"Sending request to {self.settings.model_name}")
            response = self.llm.chat.completions.create(
                model=self.settings.model_name,
                messages=[{"role": self._get_message_role(m), "content": m.content} for m in messages],
                response_model=self.response_model,
                max_tokens=self.settings.max_tokens,
                temperature=self.settings.temperature,
                **kwargs,
            )
            logger.info("Successfully generated and validated response")
            logger.debug(f"Response: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}", exc_info=True)
            raise 