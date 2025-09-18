# ExnestAI Python SDK

[![CI](https://github.com/fazza-abiyyu/sdk-exnestai-py/actions/workflows/ci.yml/badge.svg)](https://github.com/fazza-abiyyu/sdk-exnestai-py/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/exnestai.svg)](https://badge.fury.io/py/exnestai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is the Python SDK for the ExnestAI API service. It provides both a simple wrapper and an advanced client for interacting with the ExnestAI API.

## Installation

```bash
pip install exnestai
```

## Quick Start

### Simple Wrapper Usage

```python
from exnestai.wrapper import ExnestAIWrapper
from exnestai.models import ExnestMessage

# Initialize the wrapper
exnest = ExnestAIWrapper("your-api-key-here")

# Simple chat
response = await exnest.chat("gpt-4o-mini", [
    ExnestMessage(role="user", content="Hello, how are you?")
])

print(response)

# Quick response
result = await exnest.response("gemini-2.0-flash-exp", "What is Python?")

# Get models
models = await exnest.get_models()
```

### Advanced Client Usage

```python
from exnestai.client import ExnestAI
from exnestai.models import ExnestClientOptions, ExnestChatOptions, ExnestMessage

# Initialize the advanced client
exnest = ExnestAI(ExnestClientOptions(
    api_key="your-api-key-here",
    timeout=30,
    retries=3,
    debug=True
))

# Advanced chat with options
response = await exnest.chat(
    "gemini-2.0-flash-exp",
    [
        ExnestMessage(role="system", content="You are a helpful assistant."),
        ExnestMessage(role="user", content="Explain async/await in Python")
    ],
    ExnestChatOptions(
        temperature=0.7,
        max_tokens=500,
        timeout=15
    )
)

print(response)
```

## Features

- **Simple Wrapper**: Lightweight interface for basic AI interactions
- **Advanced Client**: Full configuration options with error handling and retry logic
- **Streaming Responses**: Support for real-time streaming of AI responses
- **Model Management**: Access to all available models and model information
- **Error Handling**: Comprehensive error handling with automatic retries
- **Async Support**: Fully asynchronous implementation for better performance

## API Reference

### ExnestMessage
```python
class ExnestMessage:
    role: str  # "system", "user", or "assistant"
    content: str
```

### ExnestResponse
```python
class ExnestResponse:
    success: bool
    status_code: int
    message: str
    data: Optional[ExnestResponseData]
    error: Optional[Dict[str, Any]]
    meta: Optional[ExnestMeta]
```

## Authentication

The API supports Bearer token authentication:

```python
# Using the Authorization header (recommended)
exnest = ExnestAI(ExnestClientOptions(
    api_key="your-api-key-here"
))
```

## Configuration Options

### ExnestClientOptions
```python
class ExnestClientOptions:
    api_key: str           # Required: Your ExnestAI API key
    base_url: str          # Optional: API base URL (default: https://api.exnest.app/v1)
    timeout: int           # Optional: Request timeout in seconds (default: 30)
    retries: int           # Optional: Number of retries (default: 3)
    retry_delay: int       # Optional: Delay between retries in seconds (default: 1)
    debug: bool            # Optional: Enable debug logging (default: False)
```

### ExnestChatOptions
```python
class ExnestChatOptions:
    temperature: Optional[float]     # Optional: Model temperature (0-2)
    max_tokens: Optional[int]        # Optional: Maximum tokens to generate
    timeout: Optional[int]           # Optional: Request-specific timeout
    openai_compatible: Optional[bool] # Optional: Return OpenAI-compatible format
    stream: Optional[bool]           # Optional: Enable streaming response
```

## Streaming Responses

The SDK supports streaming responses for real-time output:

```python
# Using the advanced client
async for chunk in exnest.stream(
    "gpt-4o-mini",
    [ExnestMessage(role="user", content="Tell me a story")],
    ExnestChatOptions(max_tokens=300)
):
    if chunk.choices and len(chunk.choices) > 0:
        delta = chunk.choices[0].get("delta", {})
        content = delta.get("content")
        if content:
            print(content, end="", flush=True)
```

## Error Handling

The advanced client provides comprehensive error handling with automatic retries:

```python
try:
    response = await exnest.chat(model, messages)
    
    if not response.success:
        print('API Error:', response.error)
except Exception as error:
    print('Network Error:', error)
```

## Examples

See `examples.py` for comprehensive usage examples including:
- Simple wrapper usage
- Advanced client configuration
- Streaming responses
- Error handling patterns
- Configuration updates
- Model operations
- Controller integration

## Requirements

- Python 3.8+
- httpx 0.23.0+

## Development

### Setup
```bash
# Clone the repository
git clone https://github.com/fazza-abiyyu/sdk-exnestai-py.git
cd sdk-exnestai-py

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio
```

### Testing
```bash
# Run all tests
python -m pytest tests/ -v
```

## Git Workflow

See [GIT_WORKFLOW.md](GIT_WORKFLOW.md) for detailed information about our Git workflow.

## License

MIT License

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed information about changes in each release.