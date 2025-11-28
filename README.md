# ExnestAI Python SDK

[![PyPI version](https://badge.fury.io/py/exnest-ai.svg)](https://badge.fury.io/py/exnest-ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is the Python SDK for the ExnestAI API service. It provides both a simple wrapper and an advanced, fully-featured client for interacting with the ExnestAI API, with a response format compatible with OpenAI.

## Installation

```bash
pip install exnest-ai
```

## Quick Start

Make sure to set your API key as an environment variable:
```bash
export EXNEST_API_KEY="your-api-key-here"
```

### Simple Wrapper Usage

For straightforward use cases, the `ExnestWrapper` provides a simple interface.

```python
import asyncio
import os
from exnestai import ExnestWrapper, ExnestMessage

async def main():
    # Initialize the wrapper
    api_key = os.getenv("EXNEST_API_KEY")
    exnest = ExnestWrapper(api_key=api_key)

    # Perform a chat completion
    chat_response = await exnest.chat(
        model="openai:gpt-4o-mini",
        messages=[ExnestMessage(role="user", content="Hello, how are you?")]
    )
    if not chat_response.error:
        print(f"Wrapper Chat Response: {chat_response.choices[0].message.content}")

    # Perform a text completion
    completion_response = await exnest.completion(
        model="openai:gpt-4o-mini",
        prompt="What is the capital of France?",
        max_tokens=50
    )
    if not completion_response.error:
        print(f"Wrapper Completion Response: {completion_response.choices[0].text}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Client Usage

For full control over configuration, retries, timeouts, and access to **EBC (Exnest Brain Core)** features, use the `ExnestAI` client.

```python
import asyncio
import os
from exnestai import ExnestAI, ExnestMessage, EBCDecisionContext

async def main():
    api_key = os.getenv("EXNEST_API_KEY")
    
    # Initialize the advanced client
    client = ExnestAI(
        api_key=api_key,
        timeout=60000,  # 60 seconds
        retries=2,
        debug=True
    )

    # --- Standard Chat ---
    chat_response = await client.chat(
        model="openai:gpt-4o-mini",
        messages=[ExnestMessage(role="user", content="Hello! What can you tell me about ExnestAI?")],
        exnest_metadata=True
    )
    if not chat_response.error:
        print(f"Chat Response: {chat_response.choices[0].message.content}")

    # --- EBC Deep Think Analysis ---
    # Performs advanced reasoning and decision making
    deep_think_response = await client.deep_think(
        messages=[ExnestMessage(role="user", content="Analyze the potential impact of quantum computing on cryptography")],
        model="deepseek-r1" # Optional: specify EBC model
    )
    if not deep_think_response.error:
        print(f"\nDeep Think Response: {deep_think_response.choices[0].message.content}")

    # --- EBC Structured Decision Making ---
    # Performs structured analysis based on decision context
    decision_context = EBCDecisionContext(
        decisionType="technical_architecture",
        criteria=["scalability", "maintainability", "cost"],
        constraints=["must be open source", "budget < $500/month"]
    )
    
    decision_response = await client.structured_decision(
        messages=[ExnestMessage(role="user", content="Should we migrate our database to NoSQL?")],
        context=decision_context
    )
    if not decision_response.error:
        print(f"\nStructured Decision: {decision_response.choices[0].message.content}")

    # --- EBC Task Delegation ---
    # Quick reasoning for task delegation and action dispatch
    delegate_response = await client.delegate(
        messages=[ExnestMessage(role="user", content="Email the team about the meeting delay")]
    )
    if not delegate_response.error:
        print(f"\nDelegation Response: {delegate_response.choices[0].message.content}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Streaming Responses

Both the client and wrapper support streaming for real-time data processing.

```python
import asyncio
import os
from exnestai import ExnestAI, ExnestMessage

async def stream_demo():
    api_key = os.getenv("EXNEST_API_KEY")
    client = ExnestAI(api_key=api_key)

    print("\n--- Streaming Chat Completion ---")
    print("Streaming response: ", end="")
    try:
        async for chunk in client.stream(
            model="openai:gpt-4o-mini",
            messages=[ExnestMessage(role="user", content="Tell me a fun fact about Python programming.")]
        ):
            if chunk.choices and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print("\nStreaming complete.")
    except Exception as e:
        print(f"\nAn error occurred during streaming: {e}")

if __name__ == "__main__":
    asyncio.run(stream_demo())
```

## Features

- **OpenAI-Compatible**: Response formats are compatible with OpenAI's, allowing for easy integration.
- **Dual Clients**: Choose between a simple `ExnestWrapper` for quick tasks and an advanced `ExnestAI` client for full control.
- **EBC Capabilities**: Access Exnest Brain Core features like Deep Think, Structured Decision, and Task Delegation.
- **Async First**: Fully asynchronous architecture using `httpx` for high performance.
- **Streaming Support**: Built-in support for Server-Sent Events (SSE) for real-time responses.
- **Retry Logic**: The advanced client includes automatic retries for transient network errors.
- **Model Management**: Fetch lists of available models.
- **Billing Metadata**: Option to receive detailed billing and transaction information with each request.

## Currently Available Models

The services currently support the following AI models:

- **OpenAI**: `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`
- **Google**: `gemini-2.0-flash`, `gemini-2.0-flash-lite`, `gemini-2.5-flash`, `gemini-2.5-pro`
- **Moonshot**: `kimi-k2-0711-preview`, `kimi-k2-0905-preview`, `kimi-k2-turbo-preview`, `moonshot-v1-8k`, `moonshot-v1-32k`, `moonshot-v1-128k`
- **LongCat**: `LongCat-Flash-Chat`, `LongCat-Flash-Thinking`

*Note: More models will be added in the future*

## Authentication

The SDK uses Bearer Token authentication by passing your API key to the client constructor. It will be sent in the `Authorization` header.

## Configuration

The `ExnestAI` client can be configured during initialization:

- `api_key` (str): **Required**. Your ExnestAI API key.
- `base_url` (str): Optional. The base URL for the API. Defaults to `https://api.exnest.app/v1`.
- `timeout` (int): Optional. Request timeout in milliseconds. Defaults to `30000`.
- `retries` (int): Optional. Number of times to retry a failed request. Defaults to `3`.
- `retry_delay` (int): Optional. Delay between retries in milliseconds. Defaults to `1000`.
- `debug` (bool): Optional. Set to `True` to enable debug printing. Defaults to `False`.

## Requirements

- Python 3.8+
- `httpx`

## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/fazza-abiyyu/exnest-ai-sdk-py.git
cd exnest-ai-sdk-py

# Install dependencies
pip install -r requirements.txt

# Install for local development
pip install -e .
```

### Testing

To run tests:
```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to fork the repository, make changes, and submit a pull request.

## License

This project is licensed under the MIT License.