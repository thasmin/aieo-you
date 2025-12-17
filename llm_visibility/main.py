"""Main entry point for the LLM Visibility application."""

from app.logging import logger
from app.config import config
from client import LLMClient


def test_llm_client():
    """Test LLM client functionality."""
    if not config.OPENAI_API_KEY:
        logger.warning("OpenAI API key not configured. Skipping LLM client test.")
        logger.info("To test LLM client, add OPENAI_API_KEY to your .env file")
        return

    logger.info("Testing LLM client...")

    try:
        client = LLMClient()

        # Test with a simple prompt
        model = config.DEFAULT_LLM_MODEL
        system_prompt = "You are a helpful assistant."
        user_prompt = "Say 'Hello, World!' and nothing else."

        response = client.complete(model, system_prompt, user_prompt)

        logger.info(f"LLM Response: {response}")
        logger.info("LLM client test completed successfully")

    except Exception as e:
        logger.error(f"LLM client test failed: {str(e)}")


def main():
    """Main application entry point."""
    logger.info("=" * 60)
    logger.info("LLM Visibility Application Starting")
    logger.info("=" * 60)
    logger.info(f"Environment: {config.ENVIRONMENT}")
    logger.info(f"Log Level: {config.LOG_LEVEL}")
    logger.info(f"Data Directory: {config.DATA_DIR}")
    logger.info(f"Logs Directory: {config.LOGS_DIR}")
    logger.info("=" * 60)

    # Test LLM client
    test_llm_client()

    logger.info("=" * 60)
    logger.info("LLM Visibility Application Completed")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
