"""Configuration management for the application."""

from functools import lru_cache
from typing import Optional, List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets

from .logger import get_logger

logger = get_logger(__name__)

class Settings(BaseSettings):
    """Application settings."""
    
    # LLM Configuration
    openai_api_key: str = Field(..., description="OpenAI API Key")
    model_name: str = Field("gpt-3.5-turbo", description="LLM model name")
    temperature: float = Field(0.7, description="LLM temperature")
    
    # Application Configuration
    debug: bool = Field(False, description="Debug mode")
    log_level: str = Field("INFO", description="Logging level")
    
    # API Configuration
    api_host: str = Field("0.0.0.0", description="API host")
    api_port: int = Field(8000, description="API port")
    api_workers: int = Field(1, description="Number of API workers")
    
    # Database Configuration
    database_url: Optional[str] = Field(None, description="Database URL")
    
    # Custom Model Configuration
    max_tokens: int = Field(2000, description="Maximum tokens for LLM response")
    response_format: str = Field("json", description="Response format")
    
    # Segurança
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Configurações de API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LangChain Template"
    
    # Segurança de CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:3000"]
    
    # Configurações de Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None
    
    # Validações de Segurança
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    def validate_cors_origins(self, origin: str) -> bool:
        return any(
            origin.startswith(allowed_origin) 
            for allowed_origin in self.BACKEND_CORS_ORIGINS
        )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info("Settings initialized with configuration:")
        logger.info(f"Model: {self.model_name} (temp={self.temperature})")
        logger.info(f"API: {self.api_host}:{self.api_port} (workers={self.api_workers})")
        logger.info(f"Debug mode: {self.debug}")
        logger.debug(f"Database URL: {self.database_url}")
        logger.debug(f"Max tokens: {self.max_tokens}")
        logger.debug(f"Response format: {self.response_format}")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    logger.debug("Retrieving settings instance from cache")
    return Settings()

settings = Settings() 