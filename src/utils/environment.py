"""
Environment initialization utilities.

This module handles the initialization and setup of environment variables
from Streamlit secrets and configuration files.
"""

import os
import uuid

import streamlit as st

from src.utils.load import load_config

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

        # Check if page is being initialized for the first time
        if "home_page_initialized" not in st.session_state:
            logger.info("Setting up home page")
            st.session_state.home_page_initialized = True

        # If no session ID exists, create one
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())

        # Load configuration files
        if "instructions_config" not in st.session_state:
            logger.info("Loading instructions configuration")
            st.session_state.instructions_config = load_config("instructions.toml")

        if "model_config" not in st.session_state:
            logger.info("Loading model configuration")
            st.session_state.model_config = load_config("models.toml")

        if "middleware_config" not in st.session_state:
            logger.info("Loading middleware configuration")
            st.session_state.middleware_config = load_config("middleware.toml")

        logger.info("Environment initialization completed successfully")
        return True

    except Exception as e:
        logger.error(f"Failed to initialize environment: {str(e)}")
        raise
