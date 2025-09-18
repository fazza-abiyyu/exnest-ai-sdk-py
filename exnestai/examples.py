"""
Example usage of ExnestAI Python services
This file demonstrates how to use both wrapper and client services
"""

import asyncio
from .wrapper import ExnestAIWrapper
from .client import ExnestAI
from .models import ExnestMessage, ExnestClientOptions, ExnestChatOptions


# Example 1: Simple wrapper usage
async def example_simple_wrapper():
    """Example of using the simple wrapper"""
    exnest = ExnestAIWrapper("your-api-key-here")
    
    try:
        # Simple chat
        response = await exnest.chat("gpt-4o-mini", [
            ExnestMessage(role="user", content="Hello, how are you?")
        ])
        
        print("Simple wrapper response:", response)
        
        # Simple response method
        quick_response = await exnest.response("gemini-2.0-flash-exp", "What is Python?")
        print("Quick response:", quick_response)
        
        # Get models
        models = await exnest.get_models()
        print("Available models:", models)
        
    except Exception as error:
        print("Simple wrapper error:", error)
    finally:
        await exnest.close()


# Example 2: Advanced client usage
async def example_advanced_client():
    """Example of using the advanced client"""
    exnest = ExnestAI(ExnestClientOptions(
        api_key="your-api-key-here",
        base_url="https://api.exnest.app/v1",
        timeout=30,
        retries=3,
        debug=True
    ))
    
    try:
        # Advanced chat with options
        response = await exnest.chat(
            "gemini-2.0-flash-exp",
            [
                ExnestMessage(role="system", content="You are a helpful programming assistant."),
                ExnestMessage(role="user", content="Explain async/await in Python")
            ],
            ExnestChatOptions(
                temperature=0.7,
                max_tokens=500,
                timeout=15
            )
        )
        
        print("Advanced client response:", response)
        
        # Health check
        health = await exnest.health_check()
        print("Health check:", health)
        
        # Get configuration
        config = exnest.get_config()
        print("Client config:", config)
        
        # Get models with OpenAI compatibility
        models = await exnest.get_models(openai_compatible=True)
        print("OpenAI-compatible models:", models)
        
    except Exception as error:
        print("Advanced client error:", error)
    finally:
        await exnest.close()


# Example 3: Streaming usage
async def example_streaming():
    """Example of using streaming responses"""
    exnest = ExnestAI(ExnestClientOptions(
        api_key="your-api-key-here",
        debug=True
    ))
    
    try:
        print("Starting streaming response...")
        
        # Stream response
        async for chunk in exnest.stream(
            "gpt-4o-mini",
            [
                ExnestMessage(role="user", content="Write a short story about a robot learning to paint.")
            ],
            ExnestChatOptions(max_tokens=300)
        ):
            # Print each chunk as it arrives
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].get("delta", {})
                content = delta.get("content")
                if content:
                    print(content, end="", flush=True)
        
        print("\nStreaming completed.")
        
    except Exception as error:
        print("Streaming error:", error)
    finally:
        await exnest.close()


# Example 4: Error handling
async def example_error_handling():
    """Example of error handling"""
    exnest = ExnestAI(ExnestClientOptions(
        api_key="invalid-key",
        retries=2,
        debug=True
    ))
    
    try:
        response = await exnest.responses("gpt-4o-mini", "Test message")
        
        if not response.success:
            print("Expected error response:", response.error)
        
    except Exception as error:
        print("Caught error:", error)
    finally:
        await exnest.close()


# Example 5: Configuration updates
async def example_config_updates():
    """Example of updating configuration"""
    exnest = ExnestAI(ExnestClientOptions(
        api_key="initial-key",
        debug=False
    ))
    
    print("Initial config:", exnest.get_config())
    
    # Update configuration
    exnest.update_config({
        "debug": True,
        "timeout": 60,
        "retries": 5
    })
    
    print("Updated config:", exnest.get_config())
    await exnest.close()


# Example 6: Model operations
async def example_model_operations():
    """Example of model operations"""
    exnest = ExnestAI(ExnestClientOptions(
        api_key="your-api-key-here",
        debug=True
    ))
    
    try:
        # Get all models
        all_models = await exnest.get_models()
        print("All models:", all_models)
        
        # Get models for a specific provider
        openai_models = await exnest.get_models_by_provider("openai")
        print("OpenAI models:", openai_models)
        
        # Get a specific model
        specific_model = await exnest.get_model("gpt-4o-mini")
        print("Specific model:", specific_model)
        
    except Exception as error:
        print("Model operations error:", error)
    finally:
        await exnest.close()


# Integration with controller-like function
async def integrate_with_controller(api_key: str, model: str, messages: list):
    """
    Integration with controller-like function
    This shows how the services can be integrated into existing application logic
    """
    exnest = ExnestAI(ExnestClientOptions(
        api_key=api_key,
        timeout=30,
        retries=2,
        debug=False  # Enable in development
    ))
    
    try:
        result = await exnest.chat(model, 
                                  [ExnestMessage(**msg) for msg in messages],
                                  ExnestChatOptions(
                                      temperature=0.7,
                                      max_tokens=2048
                                  ))
        
        if result.success and result.data:
            return {
                "success": True,
                "content": result.data.choices[0].message.content if result.data.choices else "",
                "usage": result.data.usage.__dict__ if result.data.usage else {},
                "model": result.data.model
            }
        else:
            raise Exception(result.message or "API request failed")
            
    except Exception as error:
        raise Exception(f"Chat completion failed: {str(error)}")
    finally:
        await exnest.close()


# Main function to run examples
async def main():
    """Run all examples"""
    print("Running ExnestAI Python SDK examples...")
    
    # Run simple wrapper example
    print("\n=== Simple Wrapper Example ===")
    await example_simple_wrapper()
    
    # Run advanced client example
    print("\n=== Advanced Client Example ===")
    await example_advanced_client()
    
    # Run configuration update example
    print("\n=== Configuration Update Example ===")
    await example_config_updates()
    
    # Run model operations example
    print("\n=== Model Operations Example ===")
    await example_model_operations()
    
    # Run error handling example
    print("\n=== Error Handling Example ===")
    await example_error_handling()


# Export for use in other parts of the application
__all__ = [
    "example_simple_wrapper",
    "example_advanced_client", 
    "example_streaming",
    "example_error_handling",
    "example_config_updates",
    "example_model_operations",
    "integrate_with_controller"
]


if __name__ == "__main__":
    # Run examples when script is executed directly
    asyncio.run(main())