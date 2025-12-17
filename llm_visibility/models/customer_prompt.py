"""Customer prompt data model."""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class CustomerPrompt:
    """
    A single customer prompt with intent label.

    Attributes:
        text: The prompt text (as a user question)
        intent: Intent label (e.g., comparison, recommendation, problem-solving)
    """

    def __init__(self, text: str, intent: str):
        """
        Initialize customer prompt.

        Args:
            text: The prompt text
            intent: Intent label
        """
        self.text = text
        self.intent = intent

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "text": self.text,
            "intent": self.intent
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "CustomerPrompt":
        """Create from dictionary."""
        return cls(
            text=data.get("text", ""),
            intent=data.get("intent", "")
        )

    def __repr__(self) -> str:
        """String representation."""
        return f"CustomerPrompt(intent='{self.intent}', text='{self.text[:50]}...')"


class CustomerPromptSet:
    """
    Collection of customer prompts with metadata.

    Attributes:
        prompts: List of CustomerPrompt instances
        company_name: Company the prompts are for
        source_url: URL where company info was extracted
        timestamp: When prompts were generated
        metadata: Additional metadata
    """

    def __init__(
        self,
        prompts: Optional[List[CustomerPrompt]] = None,
        company_name: str = "",
        source_url: str = "",
        timestamp: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """
        Initialize prompt set.

        Args:
            prompts: List of CustomerPrompt instances
            company_name: Company the prompts are for
            source_url: URL where company info was extracted
            timestamp: ISO timestamp (defaults to current time)
            metadata: Additional metadata
        """
        self.prompts = prompts or []
        self.company_name = company_name
        self.source_url = source_url
        self.timestamp = timestamp or datetime.utcnow().isoformat()
        self.metadata = metadata or {}

    def add_prompt(self, prompt: CustomerPrompt) -> None:
        """Add a prompt to the set."""
        self.prompts.append(prompt)

    def get_by_intent(self, intent: str) -> List[CustomerPrompt]:
        """Get all prompts with a specific intent."""
        return [p for p in self.prompts if p.intent == intent]

    def get_intents(self) -> List[str]:
        """Get list of unique intents."""
        return list(set(p.intent for p in self.prompts))

    def count_by_intent(self) -> Dict[str, int]:
        """Count prompts by intent."""
        counts = {}
        for prompt in self.prompts:
            counts[prompt.intent] = counts.get(prompt.intent, 0) + 1
        return counts

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "prompts": [p.to_dict() for p in self.prompts],
            "company_name": self.company_name,
            "source_url": self.source_url,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "count": len(self.prompts),
            "intents": self.count_by_intent()
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict) -> "CustomerPromptSet":
        """Create from dictionary."""
        prompts = [
            CustomerPrompt.from_dict(p) for p in data.get("prompts", [])
        ]
        return cls(
            prompts=prompts,
            company_name=data.get("company_name", ""),
            source_url=data.get("source_url", ""),
            timestamp=data.get("timestamp"),
            metadata=data.get("metadata", {})
        )

    def save(self, output_dir: str = "data/prompts") -> str:
        """
        Save prompt set to disk.

        Args:
            output_dir: Directory to save prompts

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
        filename = f"{safe_name}_prompts_{timestamp_str}.json"
        filepath = os.path.join(output_dir, filename)

        # Save to JSON
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

        return filepath

    @classmethod
    def load(cls, filepath: str) -> "CustomerPromptSet":
        """
        Load prompt set from disk.

        Args:
            filepath: Path to JSON file

        Returns:
            CustomerPromptSet instance
        """
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls.from_dict(data)

    def validate(self) -> bool:
        """
        Validate prompt set.

        Returns:
            True if valid, False otherwise
        """
        # Check that we have prompts
        if not self.prompts:
            return False

        # Check that all prompts have text and intent
        for prompt in self.prompts:
            if not prompt.text or not prompt.intent:
                return False

        return True

    def __len__(self) -> int:
        """Return number of prompts."""
        return len(self.prompts)

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"CustomerPromptSet(company='{self.company_name}', "
            f"prompts={len(self.prompts)}, "
            f"intents={len(self.get_intents())})"
        )

    def __str__(self) -> str:
        """Human-readable string representation."""
        lines = [
            f"Customer Prompts for: {self.company_name or 'Unknown'}",
            f"Total Prompts: {len(self.prompts)}",
            f"Unique Intents: {len(self.get_intents())}",
            "",
            "Intent Distribution:"
        ]

        for intent, count in sorted(
            self.count_by_intent().items(),
            key=lambda x: x[1],
            reverse=True
        ):
            lines.append(f"  {intent}: {count}")

        return "\n".join(lines)
