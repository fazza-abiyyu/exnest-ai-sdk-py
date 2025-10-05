
from typing import Optional, List, AsyncGenerator
from .client import ExnestAI
from .models import (
    ExnestMessage,
    ExnestChatResponse,
    ExnestCompletionResponse,
    ExnestStreamChunk,
    ExnestModel
)

class ExnestWrapper:
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        client_options = {"api_key": api_key}
        if base_url:
            client_options["base_url"] = base_url
        self._client = ExnestAI(**client_options)

    async def completion(
        self, model: str, prompt: str, max_tokens: Optional[int] = None
    ) -> ExnestCompletionResponse:
        opts = {}
        if max_tokens:
            opts["max_tokens"] = max_tokens
        return await self._client.completion(model, prompt, **opts)

    async def chat(
        self, model: str, messages: List[ExnestMessage], max_tokens: Optional[int] = None
    ) -> ExnestChatResponse:
        opts = {}
        if max_tokens:
            opts["max_tokens"] = max_tokens
        return await self._client.chat(model, messages, **opts)

    async def response(self, model: str, input_str: str, max_tokens: int = 200) -> ExnestChatResponse:
        """Legacy method for simple, single-turn chat."""
        messages = [ExnestMessage(role="user", content=input_str)]
        return await self.chat(model, messages, max_tokens=max_tokens)

    async def stream_completion(
        self, model: str, prompt: str, max_tokens: Optional[int] = None
    ) -> AsyncGenerator[ExnestStreamChunk, None]:
        opts = {}
        if max_tokens:
            opts["max_tokens"] = max_tokens
        async for chunk in self._client.stream_completion(model, prompt, **opts):
            yield chunk

    async def stream(
        self, model: str, messages: List[ExnestMessage], max_tokens: Optional[int] = None
    ) -> AsyncGenerator[ExnestStreamChunk, None]:
        opts = {}
        if max_tokens:
            opts["max_tokens"] = max_tokens
        async for chunk in self._client.stream(model, messages, **opts):
            yield chunk

    async def get_models(self) -> List[ExnestModel]:
        return await self._client.get_models()
