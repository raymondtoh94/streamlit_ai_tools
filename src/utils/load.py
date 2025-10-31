import os
import toml
from pathlib import Path
from typing import Any, Dict, Tuple

def load_config(
    config_filename: str,
) -> Tuple[Dict[Any, Any]]:
    """Load configuration from a TOML file.

    Args:
        config_filename (str): The name of the configuration file.
    Returns:
        Tuple[Dict[Any, Any]]: The loaded configuration as a dictionary.
    """
    # Get the root directory (where Home.py is located)
    root_dir = Path(os.getcwd())
    config_path = root_dir / "config" / config_filename
    
    with open(config_path, "r") as config_file:
        config = toml.load(config_file)
    return config
