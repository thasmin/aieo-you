"""Customer prompt generation using LLM."""

import json
from typing import Optional

from app.logging import logger
from app.config import config
from client import LLMClient
from models.company import CompanyProfile
from models.customer_prompt import CustomerPrompt, CustomerPromptSet
from prompts.customer_prompts import (
    CUSTOMER_PROMPTS_SYSTEM_PROMPT,
    CUSTOMER_PROMPTS_USER_PROMPT
)


class PromptGenerator:
    """
    Generate customer prompts based on company profile using LLM.

    Features:
    - Generates exactly 100 diverse prompts
    - Each prompt has an intent label
    - Automatic deduplication
    - JSON output validation
    """

    EXPECTED_PROMPT_COUNT = 100

    def __init__(self, model: Optional[str] = None):
        """
        Initialize prompt generator.

        Args:
            model: LLM model to use (defaults to config)
        """
        self.client = LLMClient()
        self.model = model or config.DEFAULT_LLM_MODEL

    def _parse_json_response(self, response: str) -> dict:
        """
        Parse JSON from LLM response.

        Handles common issues like markdown code blocks.

        Args:
            response: Raw LLM response

        Returns:
            Parsed JSON dictionary

        Raises:
            ValueError: If JSON cannot be parsed
        """
        # Remove markdown code blocks if present
        cleaned = response.strip()
        if cleaned.startswith("```"):
            # Remove opening ```json or ```
            lines = cleaned.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            # Remove closing ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned = "\n".join(lines)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {str(e)}")
            logger.debug(f"Response was: {response[:500]}...")
            raise ValueError(f"Invalid JSON response: {str(e)}")

    def _validate_prompts_data(self, data: dict) -> None:
        """
        Validate that prompts data has required structure.

        Args:
            data: Prompts data dictionary

        Raises:
            ValueError: If data is invalid
        """
        if "prompts" not in data:
            raise ValueError("Missing 'prompts' field in response")

        prompts = data["prompts"]
        if not isinstance(prompts, list):
            raise ValueError("'prompts' field must be a list")

        if len(prompts) != self.EXPECTED_PROMPT_COUNT:
            logger.warning(
                f"Expected {self.EXPECTED_PROMPT_COUNT} prompts, "
                f"got {len(prompts)}"
            )

        # Validate each prompt
        for i, prompt in enumerate(prompts):
            if not isinstance(prompt, dict):
                raise ValueError(f"Prompt {i} must be a dictionary")

            if "text" not in prompt:
                raise ValueError(f"Prompt {i} missing 'text' field")

            if "intent" not in prompt:
                raise ValueError(f"Prompt {i} missing 'intent' field")

            if not isinstance(prompt["text"], str):
                raise ValueError(f"Prompt {i} 'text' must be a string")

            if not isinstance(prompt["intent"], str):
                raise ValueError(f"Prompt {i} 'intent' must be a string")

    def _deduplicate_prompts(self, prompts: list) -> list:
        """
        Remove duplicate prompts based on text similarity.

        Uses exact text matching for deduplication.

        Args:
            prompts: List of prompt dictionaries

        Returns:
            Deduplicated list of prompts
        """
        seen_texts = set()
        deduplicated = []

        for prompt in prompts:
            text_lower = prompt["text"].lower().strip()
            if text_lower not in seen_texts:
                seen_texts.add(text_lower)
                deduplicated.append(prompt)
            else:
                logger.debug(f"Removed duplicate: {prompt['text']}")

        if len(deduplicated) < len(prompts):
            logger.info(
                f"Removed {len(prompts) - len(deduplicated)} duplicate prompts"
            )

        return deduplicated

    def generate(
        self,
        company_profile: CompanyProfile,
        save: bool = True
    ) -> CustomerPromptSet:
        """
        Generate customer prompts from company profile.

        Args:
            company_profile: CompanyProfile instance
            save: Whether to save prompts to disk

        Returns:
            CustomerPromptSet instance

        Raises:
            ValueError: If generation or validation fails
        """
        logger.info(
            f"Generating customer prompts for: {company_profile.company_name}"
        )
        logger.info(f"Using model: {self.model}")

        # Prepare company profile as JSON
        profile_json = company_profile.to_json()

        # Generate prompts
        system_prompt = CUSTOMER_PROMPTS_SYSTEM_PROMPT()
        user_prompt = CUSTOMER_PROMPTS_USER_PROMPT(profile_json)

        # Call LLM
        try:
            response = self.client.complete(
                model=self.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )

            logger.info("LLM response received")
            logger.debug(f"Response length: {len(response)} chars")

        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            raise

        # Parse JSON response
        try:
            prompts_data = self._parse_json_response(response)
            logger.info("Successfully parsed JSON response")

        except ValueError as e:
            logger.error(f"JSON parsing failed: {str(e)}")
            raise

        # Validate structure
        try:
            self._validate_prompts_data(prompts_data)
            logger.info(
                f"Validated {len(prompts_data['prompts'])} prompts"
            )

        except ValueError as e:
            logger.error(f"Validation failed: {str(e)}")
            raise

        # Deduplicate prompts
        deduplicated_prompts = self._deduplicate_prompts(
            prompts_data["prompts"]
        )

        # Create CustomerPrompt instances
        customer_prompts = [
            CustomerPrompt(
                text=p["text"],
                intent=p["intent"]
            )
            for p in deduplicated_prompts
        ]

        # Create CustomerPromptSet
        prompt_set = CustomerPromptSet(
            prompts=customer_prompts,
            company_name=company_profile.company_name,
            source_url=company_profile.source_url,
            metadata={
                "model": self.model,
                "original_count": len(prompts_data["prompts"]),
                "deduplicated_count": len(deduplicated_prompts)
            }
        )

        # Validate using model's validate method
        if not prompt_set.validate():
            raise ValueError("Prompt set validation failed")

        logger.info(f"Generated {len(prompt_set)} prompts")
        logger.info(f"Intent distribution: {prompt_set.count_by_intent()}")

        # Save if requested
        if save:
            filepath = prompt_set.save()
            logger.info(f"Prompts saved to: {filepath}")

        return prompt_set


def generate_prompts(
    company_profile: CompanyProfile,
    model: Optional[str] = None,
    save: bool = True
) -> CustomerPromptSet:
    """
    Convenience function to generate customer prompts.

    Args:
        company_profile: CompanyProfile instance
        model: LLM model to use (defaults to config)
        save: Whether to save prompts to disk

    Returns:
        CustomerPromptSet instance

    Example:
        >>> from models.company import CompanyProfile
        >>> profile = CompanyProfile.load("data/company_profiles/acme.json")
        >>> prompts = generate_prompts(profile)
        >>> print(f"Generated {len(prompts)} prompts")
        >>> print(prompts.count_by_intent())
    """
    generator = PromptGenerator(model=model)
    return generator.generate(company_profile, save=save)
