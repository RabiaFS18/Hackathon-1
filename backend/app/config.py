"""
Configuration management for the Technical Book RAG Chatbot.

This module defines all configuration parameters using Pydantic Settings,
with validation for required environment variables and defaults for optional ones.
"""

from pydantic import BaseSettings, Field, validator
from typing import Optional
import sys


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    
    Required variables will cause startup failure if missing.
    Optional variables have sensible defaults.
    """
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., env='OPENAI_API_KEY')
    openai_embedding_model: str = Field(
        default='text-embedding-3-small',
        env='OPENAI_EMBEDDING_MODEL'
    )
    openai_chat_model: str = Field(
        default='gpt-3.5-turbo',
        env='OPENAI_CHAT_MODEL'
    )
    openai_temperature: float = Field(
        default=0.7,
        env='OPENAI_TEMPERATURE',
        ge=0.0,
        le=2.0
    )
    openai_max_tokens: int = Field(
        default=4096,
        env='OPENAI_MAX_TOKENS',
        gt=0
    )
    
    # Qdrant Configuration
    qdrant_url: str = Field(..., env='QDRANT_URL')
    qdrant_api_key: str = Field(..., env='QDRANT_API_KEY')
    qdrant_collection_name: str = Field(
        default='book_chunks',
        env='QDRANT_COLLECTION_NAME'
    )
    
    # RAG Configuration
    chunk_size: int = Field(
        default=512,
        env='CHUNK_SIZE',
        gt=0,
        le=2048
    )
    chunk_overlap: int = Field(
        default=50,
        env='CHUNK_OVERLAP',
        ge=0
    )
    top_k_results: int = Field(
        default=5,
        env='TOP_K_RESULTS',
        gt=0,
        le=20
    )
    
    # Retry Configuration
    max_retries: int = Field(
        default=3,
        env='MAX_RETRIES',
        ge=0,
        le=10
    )
    retry_backoff_factor: float = Field(
        default=2.0,
        env='RETRY_BACKOFF_FACTOR',
        gt=0.0
    )
    
    # Logging Configuration
    log_level: str = Field(
        default='INFO',
        env='LOG_LEVEL'
    )
    
    @validator('log_level')
    def validate_log_level(cls, v):
        """Validate that log level is one of the standard Python logging levels."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(
                f'log_level must be one of {valid_levels}, got: {v}'
            )
        return v_upper
    
    @validator('openai_api_key', 'qdrant_url', 'qdrant_api_key')
    def validate_not_empty(cls, v, field):
        """Validate that required string fields are not empty."""
        if not v or not v.strip():
            raise ValueError(f'{field.name} cannot be empty')
        return v.strip()
    
    @validator('chunk_overlap')
    def validate_chunk_overlap(cls, v, values):
        """Validate that chunk overlap is less than chunk size."""
        if 'chunk_size' in values and v >= values['chunk_size']:
            raise ValueError(
                f'chunk_overlap ({v}) must be less than chunk_size ({values["chunk_size"]})'
            )
        return v
    
    class Config:
        env_file = '.env'
        case_sensitive = False


def load_settings() -> Settings:
    """
    Load and validate application settings.
    
    This function attempts to load settings from environment variables
    and provides clear error messages if required variables are missing.
    
    Returns:
        Settings: Validated configuration object
        
    Raises:
        SystemExit: If required configuration is missing or invalid
    """
    try:
        settings = Settings()
        return settings
    except Exception as e:
        # Parse the error to provide clear feedback about missing variables
        error_msg = str(e)
        
        # Check for missing required fields
        if 'field required' in error_msg.lower():
            missing_fields = []
            if 'openai_api_key' in error_msg.lower():
                missing_fields.append('OPENAI_API_KEY')
            if 'qdrant_url' in error_msg.lower():
                missing_fields.append('QDRANT_URL')
            if 'qdrant_api_key' in error_msg.lower():
                missing_fields.append('QDRANT_API_KEY')
            
            if missing_fields:
                print(
                    f"ERROR: Missing required environment variables: {', '.join(missing_fields)}",
                    file=sys.stderr
                )
                print(
                    "\nPlease set the following required environment variables:",
                    file=sys.stderr
                )
                for field in missing_fields:
                    print(f"  - {field}", file=sys.stderr)
                print(
                    "\nYou can set them in a .env file or as environment variables.",
                    file=sys.stderr
                )
                sys.exit(1)
        
        # Handle validation errors
        print(
            f"ERROR: Configuration validation failed: {error_msg}",
            file=sys.stderr
        )
        sys.exit(1)


# Global settings instance
# This will be initialized when the module is imported
settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the global settings instance.
    
    This function ensures settings are loaded only once and reused.
    
    Returns:
        Settings: The global configuration object
    """
    global settings
    if settings is None:
        settings = load_settings()
    return settings
