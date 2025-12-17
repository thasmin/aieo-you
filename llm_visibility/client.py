"""LLM Client abstraction for multiple providers."""

import time
from abc import ABC, abstractmethod
from typing import Optional
from app.logging import logger
from app.config import config


class BaseLLMClient(ABC):
    """Base class for LLM clients."""

    @abstractmethod
    def complete(self, model: str, system_prompt: str, user_prompt: str) -> str:
        """
        Send a completion request to the LLM.

        Args:
            model: Model identifier
            system_prompt: System/instruction prompt
            user_prompt: User prompt/query

        Returns:
            Response as plain string
        """
        pass


class OpenAIClient(BaseLLMClient):
    """OpenAI LLM client."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI client."""
        from openai import OpenAI

        self.api_key = api_key or config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key not found in configuration")

        self.client = OpenAI(api_key=self.api_key)

    def complete(self, model: str, system_prompt: str, user_prompt: str) -> str:
        """Send completion request to OpenAI."""
        start_time = time.time()

        try:
            logger.info(f"Calling OpenAI model: {model}")
            logger.debug(f"System prompt: {system_prompt[:100]}...")
            logger.debug(f"User prompt: {user_prompt[:100]}...")

            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                timeout=config.LLM_TIMEOUT
            )

            result = response.choices[0].message.content
            latency = time.time() - start_time

            logger.info(f"OpenAI response received in {latency:.2f}s")
            logger.debug(f"Response: {result[:100]}...")

            return result

        except Exception as e:
            latency = time.time() - start_time
            logger.error(f"OpenAI API error after {latency:.2f}s: {str(e)}")
            raise


class GeminiClient(BaseLLMClient):
    """Gemini LLM client (placeholder)."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini client."""
        self.api_key = api_key or config.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("Gemini API key not found in configuration")

        logger.warning("Gemini client is a placeholder and not yet implemented")

    def complete(self, model: str, system_prompt: str, user_prompt: str) -> str:
        """Send completion request to Gemini (placeholder)."""
        raise NotImplementedError("Gemini client is not yet implemented")


class LLMClient:
    """Unified LLM client with retry logic."""

    def __init__(self):
        """Initialize LLM client."""
        self.openai_client = None
        self.gemini_client = None

    def _get_client(self, model: str) -> BaseLLMClient:
        """Get appropriate client based on model name."""
        if model.startswith("gpt-") or model.startswith("o1-"):
            if not self.openai_client:
                self.openai_client = OpenAIClient()
            return self.openai_client
        elif model.startswith("gemini-"):
            if not self.gemini_client:
                self.gemini_client = GeminiClient()
            return self.gemini_client
        else:
            raise ValueError(f"Unsupported model: {model}")

    def complete(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        max_retries: Optional[int] = None
    ) -> str:
        """
        Send completion request with retry logic.

        Args:
            model: Model identifier (e.g., "gpt-4", "gpt-3.5-turbo")
            system_prompt: System/instruction prompt
            user_prompt: User prompt/query
            max_retries: Maximum retry attempts (defaults to config)

        Returns:
            Response as plain string

        Raises:
            Exception: If all retries fail
        """
        max_retries = max_retries or config.LLM_MAX_RETRIES
        client = self._get_client(model)

        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{max_retries} for model {model}")
                return client.complete(model, system_prompt, user_prompt)

            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    logger.warning(
                        f"Attempt {attempt + 1} failed: {str(e)}. "
                        f"Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(
                        f"All {max_retries} attempts failed for model {model}"
                    )
                    raise
