"""
Data models for ExnestAI Python SDK
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ExnestMessage:
    """Represents a message in the chat conversation"""
    role: str  # "system", "user", or "assistant"
    content: str


@dataclass
class ExnestUsage:
    """Represents token usage information"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class ExnestChoice:
    """Represents a choice in the response"""
    message: 'ExnestMessage'
    index: Optional[int] = None
    finish_reason: Optional[str] = None


@dataclass
class ExnestResponseData:
    """Represents the data portion of an ExnestAI response"""
    model: str
    choices: List['ExnestChoice']
    usage: 'ExnestUsage'


@dataclass
class ExnestMeta:
    """Represents metadata in the response"""
    timestamp: str
    request_id: str
    version: str
    execution_time: str
    execution_time_ms: Optional[int] = None


@dataclass
class ExnestResponse:
    """Represents a response from the ExnestAI API"""
    success: bool
    status_code: int
    message: str
    data: Optional['ExnestResponseData'] = None
    error: Optional[Dict[str, Any]] = None
    meta: Optional['ExnestMeta'] = None
    
    # Allow additional fields
    def __init__(self, **kwargs):
        self.success = kwargs.get('success')
        self.status_code = kwargs.get('status_code')
        self.message = kwargs.get('message')
        self.data = self._parse_data(kwargs.get('data'))
        self.error = kwargs.get('error')
        self.meta = self._parse_meta(kwargs.get('meta'))
        
        # Store any additional fields
        for key, value in kwargs.items():
            if key not in ['success', 'status_code', 'message', 'data', 'error', 'meta']:
                setattr(self, key, value)
    
    def _parse_data(self, data):
        if data is None:
            return None
        if isinstance(data, dict):
            # Parse choices
            choices = []
            for choice_data in data.get('choices', []):
                if isinstance(choice_data, dict):
                    message_data = choice_data.get('message', {})
                    if isinstance(message_data, dict):
                        message = ExnestMessage(
                            role=message_data.get('role', ''),
                            content=message_data.get('content', '')
                        )
                    else:
                        message = message_data
                    choice = ExnestChoice(
                        message=message,
                        index=choice_data.get('index'),
                        finish_reason=choice_data.get('finish_reason')
                    )
                    choices.append(choice)
                else:
                    choices.append(choice_data)
            
            # Parse usage
            usage_data = data.get('usage')
            if isinstance(usage_data, dict):
                usage = ExnestUsage(
                    prompt_tokens=usage_data.get('prompt_tokens', 0),
                    completion_tokens=usage_data.get('completion_tokens', 0),
                    total_tokens=usage_data.get('total_tokens', 0)
                )
            else:
                usage = usage_data
            
            return ExnestResponseData(
                model=data.get('model', ''),
                choices=choices,
                usage=usage
            )
        return data
    
    def _parse_meta(self, meta):
        if meta is None:
            return None
        if isinstance(meta, dict):
            return ExnestMeta(
                timestamp=meta.get('timestamp', ''),
                request_id=meta.get('request_id', ''),
                version=meta.get('version', ''),
                execution_time=meta.get('execution_time', ''),
                execution_time_ms=meta.get('execution_time_ms')
            )
        return meta


@dataclass
class ExnestStreamChunk:
    """Represents a chunk in a streaming response"""
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict[str, Any]]


@dataclass
class ExnestModelProvider:
    """Represents a model provider"""
    id: str
    name: str
    displayName: str


@dataclass
class ExnestModelPricing:
    """Represents model pricing information"""
    inputPrice: str
    outputPrice: str
    currency: str
    per: str


@dataclass
class ExnestModelLimits:
    """Represents model limits"""
    maxTokens: int
    contextWindow: int


@dataclass
class ExnestModel:
    """Represents a model available in ExnestAI"""
    id: str
    name: str
    displayName: str
    description: str
    provider: 'ExnestModelProvider'
    pricing: 'ExnestModelPricing'
    limits: 'ExnestModelLimits'
    isActive: bool
    createdAt: str


@dataclass
class ExnestClientOptions:
    """Configuration options for the ExnestAI client"""
    api_key: str
    base_url: str = "https://api.exnest.app/v1"
    timeout: int = 30  # in seconds
    retries: int = 3
    retry_delay: int = 1  # in seconds
    debug: bool = False


@dataclass
class ExnestChatOptions:
    """Options for chat completion requests"""
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    timeout: Optional[int] = None
    openai_compatible: Optional[bool] = None
    stream: Optional[bool] = None