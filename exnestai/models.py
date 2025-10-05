from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union

@dataclass
class ExnestMessage:
    role: str
    content: str

@dataclass
class Billing:
    transaction_id: str
    actual_cost_usd: str
    estimated_cost_usd: str
    refund_amount_usd: str
    wallet_currency: str
    deducted_amount: str
    exchange_rate: Optional[str] = None

@dataclass
class Links:
    transaction: str
    apiKey: str

@dataclass
class ExnestErrorDetails:
    transaction_refunded: Optional[bool] = None
    processing_time_ms: Optional[int] = None
    original_error: Optional[str] = None
    details: Optional[str] = None

@dataclass
class ExnestMetadata:
    billing: Optional[Billing] = None
    links: Optional[Links] = None
    processing_time_ms: Optional[int] = None

@dataclass
class Error:
    message: str
    type: str
    code: str
    exnest: Optional[ExnestErrorDetails] = None

@dataclass
class Usage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

@dataclass
class ExnestBaseResponse:
    id: Optional[str] = None
    object: Optional[str] = None
    created: Optional[int] = None
    model: Optional[str] = None
    usage: Optional[Usage] = None
    exnest: Optional[ExnestMetadata] = None
    error: Optional[Error] = None

@dataclass
class ChatChoice:
    index: Optional[int] = None
    message: Optional[ExnestMessage] = None
    finish_reason: Optional[str] = None

@dataclass
class ExnestChatResponse(ExnestBaseResponse):
    object: str = "chat.completion"
    choices: List[ChatChoice] = field(default_factory=list)

@dataclass
class CompletionChoice:
    index: Optional[int] = None
    text: Optional[str] = None
    finish_reason: Optional[str] = None

@dataclass
class ExnestCompletionResponse(ExnestBaseResponse):
    object: str = "text_completion"
    choices: List[CompletionChoice] = field(default_factory=list)

@dataclass
class Delta:
    role: Optional[str] = None
    content: Optional[str] = None

@dataclass
class StreamChoice:
    index: int
    delta: Delta
    finish_reason: Optional[str] = None

@dataclass
class ExnestStreamChunk:
    id: str
    object: str
    created: int
    model: str
    choices: List[StreamChoice]

@dataclass
class Provider:
    id: str
    name: str
    displayName: str

@dataclass
class Pricing:
    inputPrice: str
    outputPrice: str
    currency: str
    per: str

@dataclass
class Limits:
    maxTokens: int
    contextWindow: int

@dataclass
class ExnestModel:
    id: str
    name: str
    displayName: str
    description: str
    provider: Provider
    pricing: Pricing
    limits: Limits
    isActive: bool
    createdAt: str

ExnestResponse = Union[ExnestChatResponse, ExnestCompletionResponse]
