"""
Environment initialization utilities.

This module handles the initialization and setup of environment variables
from Streamlit secrets and configuration files.
"""

import os

import streamlit as st

from .logger import setup_logger


@st.cache_resource
def initialize_environment() -> bool:
    """
    Initialize the application environment from secrets and configuration.
    Uses streamlit secrets for sensitive data and configuration files for
    application settings.

    Returns:
        bool: True if initialization was successful
    """
    # Set up logger for environment initialization
    logger = setup_logger("environment")
    logger.info("Starting environment initialization")

    # Load environment variables from streamlit secrets
    try:
        for external_app in st.secrets.keys():
            logger.info(f"Loading environment variables for {external_app}")
            for key, value in st.secrets[external_app].items():
                if key == "API_KEY":
                    key = f"{external_app}_{key}"
                logger.debug(f"Setting {key}")
                os.environ[key] = value

        logger.info("Environment initialization completed successfully")
        return True

    except Exception as e:
        logger.error(f"Failed to initialize environment: {str(e)}")
        raise
