"""
ExnestAI Wrapper Service
Simple wrapper class following the FazzaAI pattern for basic AI interactions
"""

import os
import json
import httpx
from typing import List, Optional, Dict, Any, AsyncGenerator
from .models import ExnestMessage, ExnestResponse, ExnestStreamChunk


class ExnestAIWrapper:
    """Simple wrapper for basic ExnestAI interactions"""

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize the ExnestAI wrapper
        
        Args:
            api_key: Your ExnestAI API key
            base_url: Base URL for the API (optional)
        """
        self.api_key = api_key
        self.base_url = base_url or os.getenv("EXNEST_API_URL") or "https://api.exnest.app/v1"
        
        # Create HTTP client
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(30),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
        )

    async def chat(
        self,
        model: str,
        messages: List[ExnestMessage],
        max_tokens: Optional[int] = None
    ) -> ExnestResponse:
        """
        Simple chat completion method
        
        Args:
            model: Model identifier (e.g., "gpt-4", "claude-3")
            messages: Array of chat messages
            max_tokens: Optional maximum tokens to generate
            
        Returns:
            ExnestResponse: The API response
        """
        try:
            request_body = {
                "model": model,
                "messages": [msg.__dict__ for msg in messages],
                "api_key": self.api_key,
            }

            if max_tokens:
                request_body["max_tokens"] = max_tokens

            response = await self._client.post(
                f"{self.base_url}/completions",
                json=request_body
            )

            result = response.json()
            return ExnestResponse(**result)
            
        except Exception as error:
            return ExnestResponse(
                success=False,
                status_code=500,
                message="Network error occurred",
                error={
                    "details": str(error) or "Unknown error",
                }
            )

    async def stream(
        self,
        model: str,
        messages: List[ExnestMessage],
        max_tokens: Optional[int] = None
    ) -> AsyncGenerator[ExnestStreamChunk, None]:
        """
        Stream chat completion responses
        
        Args:
            model: Model identifier
            messages: Array of chat messages
            max_tokens: Optional maximum tokens to generate
            
        Yields:
            ExnestStreamChunk: Stream chunks
        """
        try:
            request_body = {
                "model": model,
                "messages": [msg.__dict__ for msg in messages],
                "api_key": self.api_key,
                "stream": True,
            }

            if max_tokens:
                request_body["max_tokens"] = max_tokens

            async with self._client.stream(
                "POST",
                f"{self.base_url}/completions",
                json=request_body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                    "Accept": "text/event-stream",
                }
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]  # Remove "data: " prefix
                        if data == "[DONE]":
                            break
                        try:
                            chunk_data = json.loads(data)
                            yield ExnestStreamChunk(**chunk_data)
                        except json.JSONDecodeError:
                            print(f"Failed to parse stream chunk: {data}")
                            
        except Exception as error:
            raise Exception(f"Streaming failed: {str(error)}")

    async def response(
        self,
        model: str,
        input_text: str,
        max_tokens: Optional[int] = None
    ) -> ExnestResponse:
        """
        Simple response method for single-turn conversations
        
        Args:
            model: Model identifier
            input_text: User input string
            max_tokens: Optional maximum tokens to generate
            
        Returns:
            ExnestResponse: The API response
        """
        return await self.chat(
            model, 
            [ExnestMessage(role="user", content=input_text)], 
            max_tokens
        )

    async def get_models(self) -> ExnestResponse:
        """
        Get all available models
        
        Returns:
            ExnestResponse: The API response
        """
        try:
            response = await self._client.get(
                f"{self.base_url}/models",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                }
            )

            result = response.json()
            return ExnestResponse(**result)
            
        except Exception as error:
            return ExnestResponse(
                success=False,
                status_code=500,
                message="Network error occurred",
                error={
                    "details": str(error) or "Unknown error",
                }
            )

    async def get_model(self, model_name: str) -> ExnestResponse:
        """
        Get a specific model by name
        
        Args:
            model_name: Name of the model to retrieve
            
        Returns:
            ExnestResponse: The API response
        """
        try:
            response = await self._client.get(
                f"{self.base_url}/models/{model_name}",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                }
            )

            result = response.json()
            return ExnestResponse(**result)
            
        except Exception as error:
            return ExnestResponse(
                success=False,
                status_code=500,
                message="Network error occurred",
                error={
                    "details": str(error) or "Unknown error",
                }
            )

    def get_api_key_info(self) -> str:
        """
        Get the API key being used (useful for debugging)
        
        Returns:
            str: The API key (masked for security)
        """
        if not self.api_key:
            return "No API key set"
        visible_part = self.api_key[-4:]
        return f"****{visible_part}"

    def get_base_url(self) -> str:
        """
        Get the base URL being used
        
        Returns:
            str: The base URL
        """
        return self.base_url

    def set_api_key(self, new_api_key: str) -> None:
        """
        Update the API key
        
        Args:
            new_api_key: New API key to use
        """
        self.api_key = new_api_key
        # Update authorization header
        self._client.headers["Authorization"] = f"Bearer {self.api_key}"

    def set_base_url(self, new_base_url: str) -> None:
        """
        Update the base URL
        
        Args:
            new_base_url: New base URL to use
        """
        self.base_url = new_base_url

    async def close(self) -> None:
        """Close the HTTP client session"""
        await self._client.aclose()