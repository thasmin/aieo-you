"""Example usage of the LLM client."""

from client import LLMClient
from app.logging import logger


def example_basic_usage():
    """Basic usage example."""
    client = LLMClient()

    # Example 1: Using GPT-4
    response = client.complete(
        model="gpt-4",
        system_prompt="You are a helpful assistant.",
        user_prompt="What is the capital of France?"
    )
    print(f"Response: {response}")


def example_model_switching():
    """Example of switching between models."""
    client = LLMClient()

    models = ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]

    for model in models:
        logger.info(f"Testing model: {model}")
        response = client.complete(
            model=model,
            system_prompt="You are a concise assistant.",
            user_prompt="Say hello in one word."
        )
        print(f"{model}: {response}")


def example_with_retry():
    """Example showing retry behavior."""
    client = LLMClient()

    # The client will automatically retry on failures
    # You can customize max retries per call
    response = client.complete(
        model="gpt-4",
        system_prompt="You are a helpful assistant.",
        user_prompt="Explain retry logic in one sentence.",
        max_retries=5  # Override default from config
    )
    print(f"Response: {response}")


if __name__ == "__main__":
    print("LLM Client Examples")
    print("=" * 60)

    # Uncomment to run examples (requires OPENAI_API_KEY in .env)
    # example_basic_usage()
    # example_model_switching()
    # example_with_retry()

    print("\nTo run these examples, uncomment the function calls above")
    print("and ensure OPENAI_API_KEY is set in your .env file")
