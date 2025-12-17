"""Logging configuration for the application."""

import logging
import sys
from datetime import datetime
from pathlib import Path
from .config import config


def setup_logging():
    """Configure logging to write to both stdout and file."""

    # Create logger
    logger = logging.getLogger("llm_visibility")
    logger.setLevel(getattr(logging, config.LOG_LEVEL))

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Create formatters
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    log_filename = f"app_{datetime.now().strftime('%Y%m%d')}.log"
    log_filepath = config.LOGS_DIR / log_filename

    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Create default logger instance
logger = setup_logging()
