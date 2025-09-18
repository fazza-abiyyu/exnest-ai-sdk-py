"""
Example usage of the ExnestAI Python SDK without provider prefixes
"""

import asyncio
from exnestai.client import ExnestAI
from exnestai.wrapper import ExnestAIWrapper
from exnestai.models import ExnestClientOptions, ExnestMessage, ExnestChatOptions


async def example_with_wrapper():
    """Example using the simple wrapper"""
    print("=== Example with Simple Wrapper ===")
    
    # Initialize the wrapper
    exnest = ExnestAIWrapper("your-api-key-here")
    
    # Simple chat - using model name without provider prefix
    print("Sending chat request with 'gpt-4o-mini' (no provider prefix)...")
    
    # In a real implementation, this would make an API call
    # For this example, we're just showing the API usage
    print("✓ Model name 'gpt-4o-mini' will be passed through unchanged")
    print("✓ Backend will automatically map to the appropriate provider")
    
    await exnest.close()
    print("✓ Connection closed\n")


async def example_with_client():
    """Example using the advanced client"""
    print("=== Example with Advanced Client ===")
    
    # Initialize the advanced client
    exnest = ExnestAI(ExnestClientOptions(
        api_key="your-api-key-here",
        timeout=30,
        retries=3,
        debug=True
    ))
    
    # Advanced chat with options - using model name without provider prefix
    print("Sending chat request with 'gemini-2.0-flash-exp' (no provider prefix)...")
    
    # In a real implementation, this would make an API call
    # For this example, we're just showing the API usage
    print("✓ Model name 'gemini-2.0-flash-exp' will be passed through unchanged")
    print("✓ Backend will automatically map to the appropriate provider")
    
    await exnest.close()
    print("✓ Connection closed\n")


async def main():
    """Run examples"""
    print("ExnestAI Python SDK Examples (without provider prefixes)")
    print("=" * 50)
    
    await example_with_wrapper()
    await example_with_client()
    
    print("All examples completed!")


if __name__ == "__main__":
    asyncio.run(main())