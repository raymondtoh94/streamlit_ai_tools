"""
Travel Info Agent Page

This page provides a travel information interface using various LLM providers and models.
It allows users to select different providers, models, and customize system instructions
for travel information tasks.
"""

import streamlit as st

from src.miscs.disclaimer import show_disclaimer_dialog
from src.models.llm import run_agent
from src.utils.environment import initialize_environment
from src.utils.logger import setup_logger

# ------------------------------------------------------------------------
# Initialization and Configuration
# ------------------------------------------------------------------------
# Initialize environment and logging
initialize_environment()
logger = setup_logger("travel_info_agent")

# Configure page
st.set_page_config(page_title="Travel Info Agent")
st.title("Travel Info Agent")

# Initialize session state for chat history
if "page_2_messages" not in st.session_state:
    st.session_state.page_2_messages = []

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
    height=175,
    value=st.session_state.instructions_config["travel_info_agent"].get(
        "sys_prompt", ""
    ),
    help="Customize the instructions given to the AI model",
)

# ------------------------------------------------------------------------
# Text Input and Summarization Section
# ------------------------------------------------------------------------

# Text input and processing
if prompt := st.chat_input("Enter desired travel destination..."):
    logger.info("Received user input for travel information")
    try:
        # Get provider configuration and run summarization
        provider = st.session_state.model_config[selected_provider].get(
            "model_provider", None
        )
        logger.debug(f"Using provider: {provider} with model: {selected_model}")

        agent = run_agent(
            selected_provider=provider,
            selected_model=selected_model,
            tools=[],
        )

        # `thread_id` is a unique identifier for a given conversation.
        config = {"configurable": {"thread_id": st.session_state.session_id}}

        st.session_state.page_2_messages.append({"role": "user", "content": prompt})

        for chunk in agent.stream(
            {"messages": [{"role": "user", "content": f"{prompt}"}]},
            stream_mode="updates",
            config=config,
        ):
            for key, value in chunk.items():
                logger.info(f"Agent Calls -> {chunk}")
                if key == "model":
                    st.session_state.page_2_messages.append(
                        {"role": "assistant", "content": value["messages"][-1].content}
                    )
                else:
                    st.session_state.page_2_messages.append(
                        {"role": "tools", "content": chunk}
                    )

    except Exception as e:
        logger.error(f"Error during summarization: {str(e)}")
        st.error(
            "An error occurred while generating the travel information. Please try again."
        )

# Display chat messages
for msg in st.session_state.page_2_messages:
    if msg["role"] == "tools":
        for key, value in msg["content"].items():
            with st.expander(f"🤖 **Agent Triggered**: {key}"):
                st.write(f"💬 **Response**: {str(value)}")
    else:
        st.chat_message(msg["role"]).write(msg["content"])


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
