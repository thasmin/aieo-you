"""Main entry point for the LLM Visibility application."""

from app.logging import logger
from app.config import config


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

    # Application logic will be added in future tickets
    logger.info("Application initialized successfully")

    logger.info("=" * 60)
    logger.info("LLM Visibility Application Completed")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
