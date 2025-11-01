import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.utils.load import load_config


def setup_logger(name: str = None) -> logging.Logger:
    """
    Set up a logger with both file and console handlers.

    Args:
        name (str, optional): Name of the logger. Defaults to None.

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Create or get logger
    logger = logging.getLogger(name or __name__)

    # Only add handlers if the logger doesn't already have them
    if not logger.handlers:
        try:
            # Load logging config using the existing config loader
            config = load_config("logging.toml")["logging"]
            level = getattr(logging, config["level"].upper())
        except FileNotFoundError:
            level = logging.INFO

        logger.setLevel(level)

        # Create formatters
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_formatter = logging.Formatter("%(levelname)s - %(message)s")

        # File handler (rotating log files)
        file_handler = RotatingFileHandler(
            log_dir / "app.log", maxBytes=1024 * 1024, backupCount=5  # 1MB
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(file_formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(console_formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
