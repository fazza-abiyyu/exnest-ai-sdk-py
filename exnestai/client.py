"""
ExnestAI Client Service
Advanced client with full configuration options, error handling, and retry logic
"""

import json
import time
import os
import asyncio
from typing import List, Optional, Dict, Any, AsyncGenerator
import httpx
from .models import (
    ExnestMessage, ExnestResponse, ExnestStreamChunk, 
    ExnestClientOptions, ExnestChatOptions
)


class ExnestAI:
    """Advanced ExnestAI client with full configuration options"""

    def __init__(self, options: ExnestClientOptions):
        """
        Initialize the ExnestAI client
        
        Args:
            options: Configuration options for the client
        """
        self.api_key = options.api_key
        self.base_url = options.base_url or os.getenv("EXNEST_API_URL") or "https://api.exnest.app/v1"
        self.timeout = options.timeout
        self.retries = options.retries
        self.retry_delay = options.retry_delay
        self.debug = options.debug

        if not self.api_key:
            raise ValueError("API key is required")

        # Create HTTP client
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.timeout),
            headers={
                "User-Agent": "ExnestAI-Python-Client/1.0.0",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
        )

    async def chat(
        self,
        model: str,
        messages: List[ExnestMessage],
        options: Optional[ExnestChatOptions] = None
    ) -> ExnestResponse:
        """
        Advanced chat completion with full options
        
        Args:
            model: Model identifier (e.g., "gpt-4", "claude-3")
            messages: Array of chat messages
            options: Chat options (temperature, max_tokens, timeout)
            
        Returns:
            ExnestResponse: The API response
        """
        self._validate_inputs(model, messages)
        
        if options is None:
            options = ExnestChatOptions()

        # Build request body
        request_body = {
            "model": model,
            "messages": [msg.__dict__ for msg in messages],
            "api_key": self.api_key,
        }

        # Add optional parameters
        if options.temperature is not None:
            request_body["temperature"] = options.temperature
        if options.max_tokens is not None:
            request_body["max_tokens"] = options.max_tokens
        if options.openai_compatible is not None:
            request_body["openai_compatible"] = options.openai_compatible
        if options.stream is not None:
            request_body["stream"] = options.stream

        request_timeout = options.timeout or self.timeout
        return await self._execute_request("/completions", request_body, request_timeout)

    async def stream(
        self,
        model: str,
        messages: List[ExnestMessage],
        options: Optional[ExnestChatOptions] = None
    ) -> AsyncGenerator[ExnestStreamChunk, None]:
        """
        Stream chat completion responses
        
        Args:
            model: Model identifier
            messages: Array of chat messages
            options: Chat options
            
        Yields:
            ExnestStreamChunk: Stream chunks
        """
        self._validate_inputs(model, messages)
        
        if options is None:
            options = ExnestChatOptions()

        # Build request body
        request_body = {
            "model": model,
            "messages": [msg.__dict__ for msg in messages],
            "api_key": self.api_key,
            "stream": True,
        }

        # Add optional parameters
        if options.temperature is not None:
            request_body["temperature"] = options.temperature
        if options.max_tokens is not None:
            request_body["max_tokens"] = options.max_tokens
        if options.openai_compatible is not None:
            request_body["openai_compatible"] = options.openai_compatible

        request_timeout = options.timeout or self.timeout
        async for chunk in self._execute_stream_request("/completions", request_body, request_timeout):
            yield chunk

    async def responses(
        self,
        model: str,
        input_text: str,
        max_tokens: int = 200
    ) -> ExnestResponse:
        """
        Simple response method for single-turn conversations
        
        Args:
            model: Model identifier
            input_text: User input string
            max_tokens: Maximum tokens to generate
            
        Returns:
            ExnestResponse: The API response
        """
        if not input_text or not isinstance(input_text, str):
            raise ValueError("Input must be a non-empty string")

        return await self.chat(
            model, 
            [ExnestMessage(role="user", content=input_text)], 
            ExnestChatOptions(max_tokens=max_tokens)
        )

    async def get_models(
        self, 
        openai_compatible: Optional[bool] = None, 
        timeout: Optional[int] = None
    ) -> ExnestResponse:
        """
        Get all available models
        
        Args:
            openai_compatible: Return OpenAI-compatible format
            timeout: Request timeout in seconds
            
        Returns:
            ExnestResponse: The API response
        """
        params = {}
        if openai_compatible:
            params["openai_compatible"] = "true"

        endpoint = "/models"
        if params:
            endpoint += "?" + "&".join([f"{k}={v}" for k, v in params.items()])

        request_timeout = timeout or self.timeout
        return await self._execute_request(endpoint, None, request_timeout, method="GET")

    async def get_model(
        self,
        model_name: str,
        openai_compatible: Optional[bool] = None,
        timeout: Optional[int] = None
    ) -> ExnestResponse:
        """
        Get a specific model by name
        
        Args:
            model_name: Name of the model to retrieve
            openai_compatible: Return OpenAI-compatible format
            timeout: Request timeout in seconds
            
        Returns:
            ExnestResponse: The API response
        """
        params = {}
        if openai_compatible:
            params["openai_compatible"] = "true"

        endpoint = f"/models/{model_name}"
        if params:
            endpoint += "?" + "&".join([f"{k}={v}" for k, v in params.items()])

        request_timeout = timeout or self.timeout
        return await self._execute_request(endpoint, None, request_timeout, method="GET")

    async def get_models_by_provider(
        self,
        provider: str,
        openai_compatible: Optional[bool] = None,
        timeout: Optional[int] = None
    ) -> ExnestResponse:
        """
        Get models by provider
        
        Args:
            provider: Provider name
            openai_compatible: Return OpenAI-compatible format
            timeout: Request timeout in seconds
            
        Returns:
            ExnestResponse: The API response
        """
        params = {}
        if openai_compatible:
            params["openai_compatible"] = "true"

        endpoint = f"/models/provider/{provider}"
        if params:
            endpoint += "?" + "&".join([f"{k}={v}" for k, v in params.items()])

        request_timeout = timeout or self.timeout
        return await self._execute_request(endpoint, None, request_timeout, method="GET")

    async def _execute_request(
        self,
        endpoint: str,
        body: Optional[Dict[str, Any]],
        timeout: int,
        method: str = "POST"
    ) -> ExnestResponse:
        """
        Execute HTTP request with retry logic
        
        Args:
            endpoint: API endpoint
            body: Request body
            timeout: Request timeout
            method: HTTP method
            
        Returns:
            ExnestResponse: The API response
        """
        last_error = None

        for attempt in range(self.retries + 1):
            try:
                if self.debug:
                    print(f"[ExnestAI] Attempt {attempt + 1}/{self.retries + 1} - {endpoint}")

                # Update timeout for this request
                self._client.timeout = httpx.Timeout(timeout)

                url = f"{self.base_url}{endpoint}"
                
                if method.upper() == "GET":
                    response = await self._client.get(url)
                else:
                    response = await self._client.post(url, json=body)

                result = response.json()

                if self.debug:
                    print(f"[ExnestAI] Response status: {response.status_code}")
                    print(f"[ExnestAI] Response body: {result}")

                # Return the result regardless of success/failure status
                return ExnestResponse(**result)

            except Exception as error:
                last_error = error

                if self.debug:
                    print(f"[ExnestAI] Attempt {attempt + 1} failed: {str(error)}")

                # Don't retry on the last attempt
                if attempt < self.retries:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff

        # If all retries failed, return a formatted error response
        return self._create_error_response(last_error)

    async def _execute_stream_request(
        self,
        endpoint: str,
        body: Dict[str, Any],
        timeout: int
    ) -> AsyncGenerator[ExnestStreamChunk, None]:
        """
        Execute streaming HTTP request
        
        Args:
            endpoint: API endpoint
            body: Request body
            timeout: Request timeout
            
        Yields:
            ExnestStreamChunk: Stream chunks
        """
        try:
            # Update timeout for this request
            self._client.timeout = httpx.Timeout(timeout)
            
            url = f"{self.base_url}{endpoint}"
            async with self._client.stream("POST", url, json=body) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]  # Remove "data: " prefix
                        if data == "[DONE]":
                            break
                        try:
                            chunk_data = json.loads(data)
                            yield ExnestStreamChunk(**chunk_data)
                        except json.JSONDecodeError:
                            if self.debug:
                                print(f"[ExnestAI] Failed to parse stream chunk: {data}")
        except Exception as error:
            raise Exception(f"Streaming failed: {str(error)}")

    def _create_error_response(self, error: Exception) -> ExnestResponse:
        """
        Create standardized error response
        
        Args:
            error: The exception that occurred
            
        Returns:
            ExnestResponse: Formatted error response
        """
        message = "Network error occurred"
        error_code = "NETWORK_ERROR"

        if isinstance(error, httpx.TimeoutException):
            message = "Request timeout"
            error_code = "TIMEOUT"
        elif str(error):
            message = str(error)

        return ExnestResponse(
            success=False,
            status_code=500,
            message=message,
            error={
                "details": message,
                "code": error_code,
                "type": "CLIENT_ERROR"
            }
        )

    def _validate_inputs(self, model: str, messages: List[ExnestMessage]) -> None:
        """
        Validate inputs before making request
        
        Args:
            model: Model identifier
            messages: Array of messages
        """
        if not model or not isinstance(model, str):
            raise ValueError("Model must be a non-empty string")

        if not isinstance(messages, list) or len(messages) == 0:
            raise ValueError("Messages must be a non-empty array")

        for message in messages:
            if not hasattr(message, 'role') or message.role not in ["system", "user", "assistant"]:
                raise ValueError("Each message must have a valid role (system, user, or assistant)")
            if not hasattr(message, 'content') or not message.content or not isinstance(message.content, str):
                raise ValueError("Each message must have non-empty content")

    def get_config(self) -> Dict[str, Any]:
        """
        Get client configuration information
        
        Returns:
            Dict containing configuration information
        """
        return {
            "base_url": self.base_url,
            "timeout": self.timeout,
            "retries": self.retries,
            "retry_delay": self.retry_delay,
            "debug": self.debug,
            "api_key": self.get_api_key_info(),
        }

    def get_api_key_info(self) -> str:
        """
        Get masked API key info
        
        Returns:
            str: Masked API key
        """
        if not self.api_key:
            return "No API key set"
        visible_part = self.api_key[-4:]
        return f"****{visible_part}"

    def update_config(self, config: Dict[str, Any]) -> None:
        """
        Update configuration
        
        Args:
            config: Configuration updates
        """
        if "api_key" in config:
            self.api_key = config["api_key"]
            # Update authorization header
            self._client.headers["Authorization"] = f"Bearer {self.api_key}"
        if "base_url" in config:
            self.base_url = config["base_url"]
        if "timeout" in config:
            self.timeout = config["timeout"]
        if "retries" in config:
            self.retries = config["retries"]
        if "retry_delay" in config:
            self.retry_delay = config["retry_delay"]
        if "debug" in config:
            self.debug = config["debug"]

    async def test_connection(self) -> ExnestResponse:
        """
        Test API connection
        
        Returns:
            ExnestResponse: Test result
        """
        try:
            return await self.responses("openai:gpt-3.5-turbo", "Hello", 5)
        except Exception as error:
            return self._create_error_response(error)

    async def health_check(self) -> Dict[str, Any]:
        """
        Health check method
        
        Returns:
            Dict containing health status
        """
        test_result = await self.test_connection()
        
        return {
            "status": "healthy" if test_result.success else "unhealthy",
            "timestamp": time.time(),
            "config": self.get_config(),
        }

    async def close(self) -> None:
        """Close the HTTP client session"""
        await self._client.aclose()