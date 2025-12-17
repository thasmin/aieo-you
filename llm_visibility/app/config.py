"""Application configuration management."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""

    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    LOGS_DIR = DATA_DIR / "logs"

    # Ensure directories exist
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Environment variables
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    @classmethod
    def get(cls, key: str, default=None):
        """Get configuration value."""
        return getattr(cls, key, default)


# Singleton instance
config = Config()
