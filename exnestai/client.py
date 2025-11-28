
import httpx
import asyncio
import json
from typing import Optional, List, Dict, Any, AsyncGenerator, Union
from .models import (
    ExnestMessage,
    ExnestChatResponse,
    ExnestCompletionResponse,
    ExnestStreamChunk,
    ExnestResponse,
    ExnestModel,
    EBCDecisionContext
)

class ExnestAI:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.exnest.app/v1",
        timeout: int = 30000,
        retries: int = 3,
        retry_delay: int = 1000,
        debug: bool = False
    ):
        if not api_key:
            raise ValueError("API key is required")

        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout / 1000  # Convert ms to seconds for httpx
        self.retries = retries
        self.retry_delay = retry_delay / 1000  # Convert ms to seconds
        self.debug = debug
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

    async def _execute_request(
        self, method: str, endpoint: str, body: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        last_error = None
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "ExnestAI-Python-Client/1.0.0",
            "Authorization": f"Bearer {self.api_key}"
        }

        for attempt in range(self.retries + 1):
            try:
                if self.debug:
                    print(f"[ExnestAI] Attempt {attempt + 1}/{self.retries + 1} - {method} {endpoint}")

                response = await self._client.request(
                    method,
                    endpoint,
                    json=body,
                    params=params,
                    headers=headers
                )
                response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
                result = response.json()

                if self.debug:
                    print(f"[ExnestAI] Response status: {response.status_code}")
                    print(f"[ExnestAI] Response body: {result}")

                return result

            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                last_error = e
                if self.debug:
                    print(f"[ExnestAI] Attempt {attempt + 1} failed: {e}")
                if attempt < self.retries:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
        
        raise last_error # Re-raise the last error if all retries fail

    async def _execute_stream_request(
        self, endpoint: str, body: Dict[str, Any]
    ) -> AsyncGenerator[ExnestStreamChunk, None]:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "ExnestAI-Python-Client/1.0.0",
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "text/event-stream"
        }
        body['stream'] = True

        async with self._client.stream("POST", endpoint, json=body, headers=headers) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data:"):
                    data_str = line[len("data:"):].strip()
                    if data_str == "[DONE]":
                        return
                    try:
                        chunk_data = json.loads(data_str)
                        yield ExnestStreamChunk(**chunk_data)
                    except json.JSONDecodeError:
                        if self.debug:
                            print(f"[ExnestAI] Failed to parse stream chunk: {data_str}")

    async def completion(self, model: str, prompt: str, **kwargs) -> ExnestCompletionResponse:
        body = {
            "model": model,
            "prompt": prompt,
            **kwargs
        }
        response_data = await self._execute_request("POST", "/completions", body)
        return ExnestCompletionResponse(**response_data)

    async def chat(self, model: str, messages: List[ExnestMessage], **kwargs) -> ExnestChatResponse:
        body = {
            "model": model,
            "messages": [msg.__dict__ for msg in messages],
            **kwargs
        }
        response_data = await self._execute_request("POST", "/chat/completions", body)
        return ExnestChatResponse(**response_data)

    async def stream_completion(self, model: str, prompt: str, **kwargs) -> AsyncGenerator[ExnestStreamChunk, None]:
        body = {
            "model": model,
            "prompt": prompt,
            **kwargs
        }
        async for chunk in self._execute_stream_request("/completions", body):
            yield chunk

    async def stream(self, model: str, messages: List[ExnestMessage], **kwargs) -> AsyncGenerator[ExnestStreamChunk, None]:
        body = {
            "model": model,
            "messages": [msg.__dict__ for msg in messages],
            **kwargs
        }
        async for chunk in self._execute_stream_request("/chat/completions", body):
            yield chunk

    async def responses(self, model: str, input_str: str, max_tokens: int = 200) -> ExnestChatResponse:
        """
        Simple response method for single-turn conversations
        """
        if not input_str:
            raise ValueError("Input must be a non-empty string")
        
        return await self.chat(model, [ExnestMessage(role="user", content=input_str)], max_tokens=max_tokens)

    async def deep_think(self, messages: List[ExnestMessage], **kwargs) -> ExnestChatResponse:
        """
        EBC Deep Think Analysis
        Performs advanced reasoning and decision making
        """
        body = {
            "messages": [msg.__dict__ for msg in messages],
            **kwargs
        }
        response_data = await self._execute_request("POST", "/ebc/deep-think", body)
        return ExnestChatResponse(**response_data)

    async def structured_decision(
        self, messages: List[ExnestMessage], context: EBCDecisionContext, **kwargs
    ) -> ExnestChatResponse:
        """
        EBC Structured Decision Making
        Performs structured analysis based on decision context
        """
        body = {
            "messages": [msg.__dict__ for msg in messages],
            "context": context.__dict__,
            **kwargs
        }
        response_data = await self._execute_request("POST", "/decision-making/session", body)
        return ExnestChatResponse(**response_data)

    async def delegate(self, messages: List[ExnestMessage], **kwargs) -> ExnestChatResponse:
        """
        EBC Task Delegation
        Quick reasoning for task delegation and action dispatch
        """
        body = {
            "messages": [msg.__dict__ for msg in messages],
            **kwargs
        }
        response_data = await self._execute_request("POST", "/ebc/delegate", body)
        return ExnestChatResponse(**response_data)

    async def get_models(self, openai_compatible: bool = False) -> Union[List[ExnestModel], Dict[str, Any]]:
        params = {}
        if openai_compatible:
            params["openai_compatible"] = "true"
            
        response_data = await self._execute_request("GET", "/models", params=params)
        
        # Handle v1 response wrapper if not openai compatible
        if not openai_compatible and isinstance(response_data, dict) and "data" in response_data:
             if "models" in response_data["data"]:
                 response_data = response_data["data"]["models"]
        
        if isinstance(response_data, list):
            return [ExnestModel(**model_data) for model_data in response_data]
        return response_data

    async def get_model(self, model_name: str, openai_compatible: bool = False) -> Union[ExnestModel, Dict[str, Any]]:
        params = {}
        if openai_compatible:
            params["openai_compatible"] = "true"

        response_data = await self._execute_request("GET", f"/models/{model_name}", params=params)
        
        # Handle v1 response wrapper
        if not openai_compatible and isinstance(response_data, dict) and "data" in response_data:
            response_data = response_data["data"]

        if openai_compatible:
             return response_data
             
        return ExnestModel(**response_data)

    async def get_models_by_provider(self, provider: str, openai_compatible: bool = False) -> Union[List[ExnestModel], Dict[str, Any]]:
        params = {}
        if openai_compatible:
            params["openai_compatible"] = "true"

        response_data = await self._execute_request("GET", f"/models/provider/{provider}", params=params)
        
        # Handle v1 response wrapper
        if not openai_compatible and isinstance(response_data, dict) and "data" in response_data:
             if "models" in response_data["data"]:
                 response_data = response_data["data"]["models"]

        if isinstance(response_data, list):
            return [ExnestModel(**model_data) for model_data in response_data]
        return response_data

    def get_config(self) -> Dict[str, Any]:
        return {
            "baseUrl": self.base_url,
            "timeout": self.timeout * 1000,
            "retries": self.retries,
            "retryDelay": self.retry_delay * 1000,
            "debug": self.debug,
            "apiKey": f"****{self.api_key[-4:]}"
        }

    def update_config(self, **kwargs):
        if "api_key" in kwargs: self.api_key = kwargs["api_key"]
        if "base_url" in kwargs: self.base_url = kwargs["base_url"]
        if "timeout" in kwargs: self.timeout = kwargs["timeout"] / 1000
        if "retries" in kwargs: self.retries = kwargs["retries"]
        if "retry_delay" in kwargs: self.retry_delay = kwargs["retry_delay"] / 1000
        if "debug" in kwargs: self.debug = kwargs["debug"]
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

    async def test_connection(self) -> ExnestResponse:
        try:
            return await self.chat("openai:gpt-3.5-turbo", [ExnestMessage(role="user", content="Hello")], max_tokens=5)
        except Exception as e:
            return ExnestChatResponse(error={"message": str(e), "type": "client_error", "code": "connection_error"})

    async def health_check(self) -> Dict[str, Any]:
        test_result = await self.test_connection()
        return {
            "status": "healthy" if not test_result.error else "unhealthy",
            "timestamp": asyncio.get_event_loop().time(),
            "config": self.get_config()
        }
