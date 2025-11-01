"""
Text Summarizer Page

This page provides a text summarization interface using various LLM providers and models.
It allows users to select different providers, models, and customize system instructions
for text summarization tasks.
"""

import streamlit as st

from src.miscs.disclaimer import show_disclaimer_dialog
from src.models.llm import run_llm
from src.utils.environment import initialize_environment
from src.utils.load import load_config
from src.utils.logger import setup_logger

# ------------------------------------------------------------------------
# Initialization and Configuration
# ------------------------------------------------------------------------
# Initialize environment and logging
initialize_environment()
logger = setup_logger("summarizer")

# Configure page
st.set_page_config(page_title="Summarizer")
st.title("Text Summarizer")

# ------------------------------------------------------------------------
# Model Selection Section
# ------------------------------------------------------------------------
# Initialize session state for provider selection
if "previous_provider" not in st.session_state:
    st.session_state.previous_provider = None

# Provider dropdown
selected_provider = st.selectbox(
    "Select Provider",
    options=[key.upper() for key in st.session_state.model_config.keys()],
    help="Choose the AI provider for text summarization",
)

# Log provider changes
if selected_provider != st.session_state.previous_provider:
    logger.info(f"Selected provider: {selected_provider}")
    st.session_state.previous_provider = selected_provider

# Initialize session state for model selection
if "previous_model" not in st.session_state:
    st.session_state.previous_model = None

# Model dropdown
model_options = st.session_state.model_config[selected_provider].get("model", None)
selected_model = st.selectbox(
    "Select Model",
    options=model_options,
    help="Choose the specific model for summarization",
)

# Log model changes
if selected_model != st.session_state.previous_model:
    logger.info(f"Selected model: {selected_model}")
    st.session_state.previous_model = selected_model

# ------------------------------------------------------------------------
# System Instructions Section
# ------------------------------------------------------------------------
sys_instr = st.text_area(
    "System Instructions",
    height=250,
    value=st.session_state.instructions_config["summarizer"].get("instruction", ""),
    help="Customize the instructions given to the AI model",
)

# ------------------------------------------------------------------------
# Text Input and Summarization Section
# ------------------------------------------------------------------------
# Initialize session state for prompt tracking
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None

# Text input and processing
if prompt := st.chat_input("Enter text to summarize..."):
    if prompt != st.session_state.last_prompt:  # Prevent duplicate processing
        logger.info("Received text for summarization")
        try:
            # Get provider configuration and run summarization
            provider = st.session_state.model_config[selected_provider].get(
                "model_provider", None
            )
            logger.debug(f"Using provider: {provider} with model: {selected_model}")

            response = run_llm(
                selected_provider=provider,
                selected_model=selected_model,
                prompt=f"{sys_instr}\n\nSummarize the following text:\n{prompt}",
            )

            # Display results
            logger.info("Successfully generated summary")
            st.write(f"**Summary**: \n{response.content}")
            st.session_state.last_prompt = prompt

        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            st.error(
                "An error occurred while generating the summary. Please try again."
            )

# ------------------------------------------------------------------------
# Footer Section
# ------------------------------------------------------------------------
# Legal disclaimer
st.button(
    "&nbsp;:small[:gray[:material/balance: Legal disclaimer]]",
    type="tertiary",
    on_click=show_disclaimer_dialog,
)

# Tech stack information
st.markdown("---")
st.markdown("### 🛠 Tech Stack")

# Display tech stack in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Python**\nCore programming language for logic and data handling")
    st.info("**uv**\nManaging dependencies and virtual environments")

with col2:
    st.info("**Streamlit**\nInteractive UI and web app framework")
    st.info("**Groq** and **Google Gemini**\nAI model hosting platforms")

with col3:
    st.info("**LLM**\nPowering text summarization using AI models")
    st.info("**LangChain**\nFramework for developing LLM applications")
