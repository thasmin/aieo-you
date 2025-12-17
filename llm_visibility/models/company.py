"""Company profile data model."""

import json
import os
from datetime import datetime
from typing import List, Optional, Dict


class CompanyProfile:
    """
    Structured company profile extracted from website content.

    Attributes:
        company_name: Name of the company
        products: List of products offered
        services: List of services offered
        value_propositions: List of key value propositions
        category: Primary business category
        source_url: URL where data was extracted from
        timestamp: When the profile was created
        raw_data: Original extraction data
    """

    def __init__(
        self,
        company_name: str = "",
        products: Optional[List[str]] = None,
        services: Optional[List[str]] = None,
        value_propositions: Optional[List[str]] = None,
        category: str = "",
        source_url: str = "",
        timestamp: Optional[str] = None,
        raw_data: Optional[Dict] = None
    ):
        """
        Initialize company profile.

        Args:
            company_name: Name of the company
            products: List of products offered
            services: List of services offered
            value_propositions: List of key value propositions
            category: Primary business category
            source_url: URL where data was extracted from
            timestamp: ISO timestamp (defaults to current time)
            raw_data: Original extraction data
        """
        self.company_name = company_name
        self.products = products or []
        self.services = services or []
        self.value_propositions = value_propositions or []
        self.category = category
        self.source_url = source_url
        self.timestamp = timestamp or datetime.utcnow().isoformat()
        self.raw_data = raw_data or {}

    @classmethod
    def from_dict(cls, data: Dict) -> "CompanyProfile":
        """
        Create CompanyProfile from dictionary.

        Args:
            data: Dictionary containing profile data

        Returns:
            CompanyProfile instance
        """
        return cls(
            company_name=data.get("company_name", ""),
            products=data.get("products", []),
            services=data.get("services", []),
            value_propositions=data.get("value_propositions", []),
            category=data.get("category", ""),
            source_url=data.get("source_url", ""),
            timestamp=data.get("timestamp"),
            raw_data=data.get("raw_data", {})
        )

    def to_dict(self) -> Dict:
        """
        Convert profile to dictionary.

        Returns:
            Dictionary representation of profile
        """
        return {
            "company_name": self.company_name,
            "products": self.products,
            "services": self.services,
            "value_propositions": self.value_propositions,
            "category": self.category,
            "source_url": self.source_url,
            "timestamp": self.timestamp,
            "raw_data": self.raw_data
        }

    def to_json(self, indent: int = 2) -> str:
        """
        Convert profile to JSON string.

        Args:
            indent: Indentation level for pretty printing

        Returns:
            JSON string
        """
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def save(self, output_dir: str = "data/company_profiles") -> str:
        """
        Save profile to disk.

        Args:
            output_dir: Directory to save profile

        Returns:
            Path to saved file
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Generate filename from company name and timestamp
        safe_name = "".join(
            c if c.isalnum() else "_" for c in self.company_name
        ).lower()
        if not safe_name:
            safe_name = "unknown"

        timestamp_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_name}_{timestamp_str}.json"
        filepath = os.path.join(output_dir, filename)

        # Save to JSON
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

        return filepath

    @classmethod
    def load(cls, filepath: str) -> "CompanyProfile":
        """
        Load profile from disk.

        Args:
            filepath: Path to JSON file

        Returns:
            CompanyProfile instance
        """
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls.from_dict(data)

    def validate(self) -> bool:
        """
        Validate that profile has required structure.

        Returns:
            True if valid, False otherwise
        """
        # Check that all fields exist (even if empty)
        required_fields = [
            "company_name",
            "products",
            "services",
            "value_propositions",
            "category"
        ]

        for field in required_fields:
            if not hasattr(self, field):
                return False

        # Check that list fields are actually lists
        list_fields = ["products", "services", "value_propositions"]
        for field in list_fields:
            if not isinstance(getattr(self, field), list):
                return False

        return True

    def __repr__(self) -> str:
        """String representation of profile."""
        return (
            f"CompanyProfile(company_name='{self.company_name}', "
            f"products={len(self.products)}, services={len(self.services)}, "
            f"category='{self.category}')"
        )

    def __str__(self) -> str:
        """Human-readable string representation."""
        lines = [
            f"Company: {self.company_name or 'N/A'}",
            f"Category: {self.category or 'N/A'}",
            f"Products: {', '.join(self.products) if self.products else 'None'}",
            f"Services: {', '.join(self.services) if self.services else 'None'}",
            f"Value Props: {', '.join(self.value_propositions) if self.value_propositions else 'None'}"
        ]
        return "\n".join(lines)
