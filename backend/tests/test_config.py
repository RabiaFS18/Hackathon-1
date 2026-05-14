"""
Unit tests for configuration management.

Tests cover:
- Required environment variable validation
- Default values for optional parameters
- Validation rules for configuration fields
- Startup validation with clear error messages
"""

import pytest
import os
from unittest.mock import patch
from pydantic import ValidationError
from app.config import Settings, load_settings


class TestConfigurationValidation:
    """Test configuration validation and required fields."""
    
    def test_all_required_fields_present(self):
        """Test that configuration loads successfully with all required fields."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            assert settings.openai_api_key == 'sk-test-key-123'
            assert settings.qdrant_url == 'https://test.qdrant.io'
            assert settings.qdrant_api_key == 'test-qdrant-key'
    
    def test_missing_openai_api_key(self):
        """Test that missing OPENAI_API_KEY raises validation error."""
        env_vars = {
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(ValidationError) as exc_info:
                Settings()
            assert 'openai_api_key' in str(exc_info.value).lower()
    
    def test_missing_qdrant_url(self):
        """Test that missing QDRANT_URL raises validation error."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_API_KEY': 'test-qdrant-key'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(ValidationError) as exc_info:
                Settings()
            assert 'qdrant_url' in str(exc_info.value).lower()
    
    def test_missing_qdrant_api_key(self):
        """Test that missing QDRANT_API_KEY raises validation error."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(ValidationError) as exc_info:
                Settings()
            assert 'qdrant_api_key' in str(exc_info.value).lower()
    
    def test_empty_required_fields(self):
        """Test that empty required fields raise validation error."""
        env_vars = {
            'OPENAI_API_KEY': '   ',  # Empty/whitespace
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(ValidationError) as exc_info:
                Settings()
            assert 'cannot be empty' in str(exc_info.value).lower()


class TestDefaultValues:
    """Test default values for optional configuration parameters."""
    
    def test_openai_defaults(self):
        """Test OpenAI configuration defaults."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            assert settings.openai_embedding_model == 'text-embedding-3-small'
            assert settings.openai_chat_model == 'gpt-3.5-turbo'
            assert settings.openai_temperature == 0.7
            assert settings.openai_max_tokens == 4096
    
    def test_qdrant_defaults(self):
        """Test Qdrant configuration defaults."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            assert settings.qdrant_collection_name == 'book_chunks'
    
    def test_rag_defaults(self):
        """Test RAG configuration defaults."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            assert settings.chunk_size == 512
            assert settings.chunk_overlap == 50
            assert settings.top_k_results == 5
    
    def test_retry_defaults(self):
        """Test retry configuration defaults."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            assert settings.max_retries == 3
            assert settings.retry_backoff_factor == 2.0
    
    def test_logging_defaults(self):
        """Test logging configuration defaults."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            assert settings.log_level == 'INFO'


class TestConfigurationOverrides:
    """Test that environment variables override default values."""
    
    def test_override_openai_settings(self):
        """Test overriding OpenAI configuration."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'OPENAI_EMBEDDING_MODEL': 'text-embedding-ada-002',
            'OPENAI_CHAT_MODEL': 'gpt-4',
            'OPENAI_TEMPERATURE': '0.5',
            'OPENAI_MAX_TOKENS': '2048',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            assert settings.openai_embedding_model == 'text-embedding-ada-002'
            assert settings.openai_chat_model == 'gpt-4'
            assert settings.openai_temperature == 0.5
            assert settings.openai_max_tokens == 2048
    
    def test_override_rag_settings(self):
        """Test overriding RAG configuration."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key',
            'CHUNK_SIZE': '1024',
            'CHUNK_OVERLAP': '100',
            'TOP_K_RESULTS': '10'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            assert settings.chunk_size == 1024
            assert settings.chunk_overlap == 100
            assert settings.top_k_results == 10
    
    def test_override_logging_level(self):
        """Test overriding log level."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key',
            'LOG_LEVEL': 'DEBUG'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            assert settings.log_level == 'DEBUG'


class TestValidationRules:
    """Test validation rules for configuration fields."""
    
    def test_temperature_range_validation(self):
        """Test that temperature must be between 0.0 and 2.0."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'OPENAI_TEMPERATURE': '3.0',  # Invalid: > 2.0
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(ValidationError) as exc_info:
                Settings()
            assert 'openai_temperature' in str(exc_info.value).lower()
    
    def test_max_tokens_positive(self):
        """Test that max_tokens must be positive."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'OPENAI_MAX_TOKENS': '0',  # Invalid: must be > 0
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(ValidationError) as exc_info:
                Settings()
            assert 'openai_max_tokens' in str(exc_info.value).lower()
    
    def test_chunk_size_validation(self):
        """Test that chunk_size must be positive and within limits."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key',
            'CHUNK_SIZE': '3000'  # Invalid: > 2048
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(ValidationError) as exc_info:
                Settings()
            assert 'chunk_size' in str(exc_info.value).lower()
    
    def test_chunk_overlap_less_than_size(self):
        """Test that chunk_overlap must be less than chunk_size."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key',
            'CHUNK_SIZE': '512',
            'CHUNK_OVERLAP': '512'  # Invalid: must be < chunk_size
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(ValidationError) as exc_info:
                Settings()
            assert 'chunk_overlap' in str(exc_info.value).lower()
            assert 'less than chunk_size' in str(exc_info.value).lower()
    
    def test_top_k_results_validation(self):
        """Test that top_k_results must be positive and within limits."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key',
            'TOP_K_RESULTS': '25'  # Invalid: > 20
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(ValidationError) as exc_info:
                Settings()
            assert 'top_k_results' in str(exc_info.value).lower()
    
    def test_log_level_validation(self):
        """Test that log_level must be a valid Python logging level."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key',
            'LOG_LEVEL': 'INVALID'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(ValidationError) as exc_info:
                Settings()
            assert 'log_level' in str(exc_info.value).lower()
    
    def test_log_level_case_insensitive(self):
        """Test that log_level is case-insensitive."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key',
            'LOG_LEVEL': 'debug'  # lowercase
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            assert settings.log_level == 'DEBUG'  # Should be normalized to uppercase


class TestStartupValidation:
    """Test startup validation with clear error messages."""
    
    def test_load_settings_success(self):
        """Test that load_settings returns valid settings."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = load_settings()
            assert settings.openai_api_key == 'sk-test-key-123'
    
    def test_load_settings_missing_required_exits(self):
        """Test that load_settings exits with clear error for missing required vars."""
        env_vars = {
            'QDRANT_URL': 'https://test.qdrant.io'
            # Missing OPENAI_API_KEY and QDRANT_API_KEY
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(SystemExit) as exc_info:
                load_settings()
            assert exc_info.value.code == 1
    
    def test_load_settings_validation_error_exits(self):
        """Test that load_settings exits with clear error for validation failures."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key',
            'OPENAI_TEMPERATURE': '5.0'  # Invalid value
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(SystemExit) as exc_info:
                load_settings()
            assert exc_info.value.code == 1


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_whitespace_trimming(self):
        """Test that whitespace is trimmed from required string fields."""
        env_vars = {
            'OPENAI_API_KEY': '  sk-test-key-123  ',
            'QDRANT_URL': '  https://test.qdrant.io  ',
            'QDRANT_API_KEY': '  test-qdrant-key  '
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            assert settings.openai_api_key == 'sk-test-key-123'
            assert settings.qdrant_url == 'https://test.qdrant.io'
            assert settings.qdrant_api_key == 'test-qdrant-key'
    
    def test_minimum_valid_values(self):
        """Test minimum valid values for numeric fields."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key',
            'OPENAI_TEMPERATURE': '0.0',
            'OPENAI_MAX_TOKENS': '1',
            'CHUNK_SIZE': '1',
            'CHUNK_OVERLAP': '0',
            'TOP_K_RESULTS': '1',
            'MAX_RETRIES': '0',
            'RETRY_BACKOFF_FACTOR': '0.1'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            assert settings.openai_temperature == 0.0
            assert settings.openai_max_tokens == 1
            assert settings.chunk_size == 1
            assert settings.chunk_overlap == 0
            assert settings.top_k_results == 1
            assert settings.max_retries == 0
            assert settings.retry_backoff_factor == 0.1
    
    def test_maximum_valid_values(self):
        """Test maximum valid values for numeric fields."""
        env_vars = {
            'OPENAI_API_KEY': 'sk-test-key-123',
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-qdrant-key',
            'OPENAI_TEMPERATURE': '2.0',
            'CHUNK_SIZE': '2048',
            'TOP_K_RESULTS': '20',
            'MAX_RETRIES': '10'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            assert settings.openai_temperature == 2.0
            assert settings.chunk_size == 2048
            assert settings.top_k_results == 20
            assert settings.max_retries == 10
