"""Company profile extraction using LLM."""

import json
from typing import Optional, Dict

from app.logging import logger
from app.config import config
from client import LLMClient
from models.company import CompanyProfile
from prompts.company_profile import (
    COMPANY_PROFILE_SYSTEM_PROMPT,
    COMPANY_PROFILE_USER_PROMPT
)


class ProfileExtractor:
    """
    Extract structured company profiles from website text using LLM.

    Features:
    - Single LLM call for extraction
    - Strict JSON output validation
    - Automatic profile saving
    - Graceful error handling
    """

    def __init__(self, model: Optional[str] = None):
        """
        Initialize profile extractor.

        Args:
            model: LLM model to use (defaults to config)
        """
        self.client = LLMClient()
        self.model = model or config.DEFAULT_LLM_MODEL

    def _parse_json_response(self, response: str) -> Dict:
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
            logger.debug(f"Response was: {response}")
            raise ValueError(f"Invalid JSON response: {str(e)}")

    def _validate_profile_data(self, data: Dict) -> None:
        """
        Validate that profile data has required structure.

        Args:
            data: Profile data dictionary

        Raises:
            ValueError: If data is invalid
        """
        required_fields = [
            "company_name",
            "products",
            "services",
            "value_propositions",
            "category"
        ]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        # Validate list fields
        list_fields = ["products", "services", "value_propositions"]
        for field in list_fields:
            if not isinstance(data[field], list):
                raise ValueError(f"Field '{field}' must be a list")

        # Validate string fields
        string_fields = ["company_name", "category"]
        for field in string_fields:
            if not isinstance(data[field], str):
                raise ValueError(f"Field '{field}' must be a string")

    def extract(
        self,
        website_text: str,
        source_url: str = "",
        save: bool = True
    ) -> CompanyProfile:
        """
        Extract company profile from website text.

        Args:
            website_text: Concatenated text from website crawl
            source_url: URL where text was extracted from
            save: Whether to save profile to disk

        Returns:
            CompanyProfile instance

        Raises:
            ValueError: If extraction or validation fails
        """
        logger.info(f"Extracting company profile using model: {self.model}")
        logger.debug(f"Input text length: {len(website_text)} chars")

        # Generate prompts
        system_prompt = COMPANY_PROFILE_SYSTEM_PROMPT
        user_prompt = COMPANY_PROFILE_USER_PROMPT(website_text)

        # Call LLM
        try:
            response = self.client.complete(
                model=self.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )

            logger.info("LLM response received")
            logger.debug(f"Response: {response[:200]}...")

        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            raise

        # Parse JSON response
        try:
            profile_data = self._parse_json_response(response)
            logger.info("Successfully parsed JSON response")

        except ValueError as e:
            logger.error(f"JSON parsing failed: {str(e)}")
            raise

        # Validate structure
        try:
            self._validate_profile_data(profile_data)
            logger.info("Profile data validated successfully")

        except ValueError as e:
            logger.error(f"Validation failed: {str(e)}")
            raise

        # Create CompanyProfile instance
        profile = CompanyProfile(
            company_name=profile_data["company_name"],
            products=profile_data["products"],
            services=profile_data["services"],
            value_propositions=profile_data["value_propositions"],
            category=profile_data["category"],
            source_url=source_url,
            raw_data={"llm_response": response, "parsed_data": profile_data}
        )

        # Validate using model's validate method
        if not profile.validate():
            raise ValueError("Profile validation failed")

        logger.info(f"Profile created: {profile}")

        # Save if requested
        if save:
            filepath = profile.save()
            logger.info(f"Profile saved to: {filepath}")

        return profile


def extract_profile(
    website_text: str,
    source_url: str = "",
    model: Optional[str] = None,
    save: bool = True
) -> CompanyProfile:
    """
    Convenience function to extract company profile.

    Args:
        website_text: Concatenated text from website crawl
        source_url: URL where text was extracted from
        model: LLM model to use (defaults to config)
        save: Whether to save profile to disk

    Returns:
        CompanyProfile instance

    Example:
        >>> from crawler import crawl_website
        >>> crawl_data = crawl_website("https://example.com")
        >>> profile = extract_profile(
        ...     crawl_data["concatenated_text"],
        ...     crawl_data["base_url"]
        ... )
        >>> print(profile)
    """
    extractor = ProfileExtractor(model=model)
    return extractor.extract(website_text, source_url=source_url, save=save)
