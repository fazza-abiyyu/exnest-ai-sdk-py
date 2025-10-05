
import asyncio
import os
from exnestai import ExnestAI, ExnestMessage, ExnestWrapper

async def demo_advanced_client():
    """Demonstrates the features of the advanced ExnestAI client."""
    print("\n=== Demo: Advanced ExnestAI Client ===\n")
    
    api_key = os.getenv("EXNEST_API_KEY", "your-api-key-here")
    if api_key == "your-api-key-here":
        print("Warning: EXNEST_API_KEY environment variable not set. Using placeholder.")

    client = ExnestAI(
        api_key=api_key,
        debug=True
    )

    # 1. Chat Completion
    print("--- 1. Chat Completion ---")
    try:
        chat_response = await client.chat(
            model="openai:gpt-4o-mini",
            messages=[ExnestMessage(role="user", content="Hello! What can you tell me about ExnestAI?")],
            exnest_metadata=True
        )
        if chat_response.error:
            print(f"API Error: {chat_response.error.message}")
        else:
            print(f"Response: {chat_response.choices[0].message.content}")
            if chat_response.usage:
                print(f"Tokens: {chat_response.usage.total_tokens}")
            if chat_response.exnest and chat_response.exnest.billing:
                print(f"Cost: {chat_response.exnest.billing.actual_cost_usd} USD")
    except Exception as e:
        print(f"An error occurred: {e}")

    # 2. Streaming Chat Completion
    print("\n--- 2. Streaming Chat Completion ---")
    try:
        print("Streaming response: ", end="")
        async for chunk in client.stream(
            model="openai:gpt-4o-mini",
            messages=[ExnestMessage(role="user", content="Tell me a fun fact about Python programming.")]
        ):
            if chunk.choices and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print("\nStreaming complete.")
    except Exception as e:
        print(f"An error occurred during streaming: {e}")

    # 3. Get Models
    print("\n--- 3. Get Available Models ---")
    try:
        models = await client.get_models()
        print(f"Successfully fetched {len(models)} models.")
        # print([model.id for model in models])
    except Exception as e:
        print(f"An error occurred while fetching models: {e}")

async def demo_simple_wrapper():
    """Demonstrates the features of the simple ExnestWrapper."""
    print("\n=== Demo: Simple ExnestAI Wrapper ===\n")
    
    api_key = os.getenv("EXNEST_API_KEY", "your-api-key-here")
    if api_key == "your-api-key-here":
        print("Warning: EXNEST_API_KEY environment variable not set. Using placeholder.")

    wrapper = ExnestWrapper(api_key=api_key)

    # 1. Text Completion
    print("--- 1. Text Completion ---")
    try:
        completion_response = await wrapper.completion(
            model="openai:gpt-4o-mini",
            prompt="What is the capital of France?",
            max_tokens=50
        )
        if completion_response.error:
            print(f"API Error: {completion_response.error.message}")
        else:
            print(f"Response: {completion_response.choices[0].text}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # 2. Legacy `response` method
    print("\n--- 2. Legacy `response` method ---")
    try:
        legacy_response = await wrapper.response(
            model="google:gemini-2.0-flash-exp",
            input_str="What is TypeScript?"
        )
        if legacy_response.error:
            print(f"API Error: {legacy_response.error.message}")
        else:
            print(f"Response: {legacy_response.choices[0].message.content}")
    except Exception as e:
        print(f"An error occurred: {e}")

async def main():
    await demo_advanced_client()
    print("\n" + "="*50 + "\n")
    await demo_simple_wrapper()

if __name__ == "__main__":
    asyncio.run(main())
