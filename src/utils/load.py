"""
Configuration loading utilities.

This module handles loading and parsing of configuration files from
the config directory.
"""

from pathlib import Path
from typing import Any, Dict

import toml


def load_config(config_file: str) -> Dict[str, Any]:
    """
    Load a configuration file from the config directory.

    Args:
        config_file (str): Name of the configuration file to load

    Returns:
        Dict[str, Any]: Parsed configuration data

    Raises:
        FileNotFoundError: If the configuration file doesn't exist
    """
    config_path = Path("config") / config_file
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file {config_file} not found")
    return toml.load(config_path)
