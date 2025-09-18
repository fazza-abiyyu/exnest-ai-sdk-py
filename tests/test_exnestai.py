"""
Test suite for the ExnestAI Python SDK
"""

import pytest
import asyncio
from unittest.mock import Mock, patch

from exnestai.client import ExnestAI
from exnestai.wrapper import ExnestAIWrapper
from exnestai.models import ExnestClientOptions, ExnestMessage


class TestExnestAIWrapper:
    """Test cases for the ExnestAIWrapper class"""
    
    def test_wrapper_initialization(self):
        """Test that the wrapper initializes correctly"""
        api_key = "test-api-key"
        wrapper = ExnestAIWrapper(api_key)
        
        assert wrapper.api_key == api_key
        # The actual base URL is exnest.app, not exnest.ai
        assert wrapper.base_url == "https://api.exnest.app/v1"
    
    def test_wrapper_initialization_with_custom_base_url(self):
        """Test that the wrapper initializes with custom base URL"""
        api_key = "test-api-key"
        custom_url = "https://custom.api.exnest.app/v1"
        wrapper = ExnestAIWrapper(api_key, custom_url)
        
        assert wrapper.api_key == api_key
        assert wrapper.base_url == custom_url
    
    @pytest.mark.asyncio
    async def test_wrapper_close(self):
        """Test that the wrapper can close connections"""
        wrapper = ExnestAIWrapper("test-api-key")
        
        # This should not raise an exception
        await wrapper.close()

    def test_get_base_url(self):
        """Test getting the base URL"""
        api_key = "test-api-key"
        wrapper = ExnestAIWrapper(api_key)
        
        assert wrapper.get_base_url() == "https://api.exnest.app/v1"


class TestExnestAI:
    """Test cases for the ExnestAI client"""
    
    def test_client_initialization(self):
        """Test that the client initializes correctly"""
        options = ExnestClientOptions(
            api_key="test-api-key",
            timeout=30,
            retries=3,
            debug=True
        )
        
        client = ExnestAI(options)
        
        assert client.api_key == options.api_key
        assert client.base_url == "https://api.exnest.app/v1"
        assert client.timeout == options.timeout
        assert client.retries == options.retries
        assert client.debug == options.debug
    
    def test_client_initialization_without_required_api_key(self):
        """Test that the client requires API key"""
        options = ExnestClientOptions(api_key="")  # Empty API key
        
        with pytest.raises(ValueError, match="API key is required"):
            ExnestAI(options)
    
    @pytest.mark.asyncio
    async def test_client_close(self):
        """Test that the client can close connections"""
        options = ExnestClientOptions(api_key="test-api-key")
        client = ExnestAI(options)
        
        # This should not raise an exception
        await client.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])