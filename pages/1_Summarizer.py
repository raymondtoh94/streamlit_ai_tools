import os
import streamlit as st
from src.models.llm import run_llm
from src.utils.load import load_config, initialize_environment
from src.miscs.disclaimer import show_disclaimer_dialog

# Initialize environment variables
initialize_environment()

# Load config
instructions = load_config(
    "instructions.toml"
)

model_config = load_config(
    "models.toml"
)

# Streamlit App
st.set_page_config(page_title="Summarizer")
st.title("Text Summarizer")

# Provider Selection
model_config = load_config("models.toml")
selected_provider = st.selectbox("Select Provider", options=[key.upper() for key in model_config.keys()])

# Select Model based on Provider
model_options = model_config[selected_provider].get("model", None)
selected_model = st.selectbox("Select Model", options=model_options)

# System Instructions
sys_instr = st.text_area("System Instructions", height=250, value=instructions["summarizer"].get("instruction", ""))

# Chat Input for Text to Summarize
if prompt := st.chat_input():
    response = run_llm(
        selected_provider=model_config[selected_provider].get("model_provider", None),
        selected_model=selected_model,
        prompt=f"{sys_instr}\n\nSummarize the following text:\n{prompt}"
    )
    
    st.write(f"**Summary**: \n{response.content}")

st.button(
    "&nbsp;:small[:gray[:material/balance: Legal disclaimer]]",
    type="tertiary",
    on_click=show_disclaimer_dialog,
)

# --- Tech Stack Section ---
st.markdown("---")  # horizontal divider

st.markdown("### 🛠 Tech Stack")
col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Python**\nCore programming language for logic and data handling")

with col2:
    st.info("**Streamlit**\nInteractive UI and web app framework")

with col3:
    st.info("**LLM**\nPowering text summarization using AI models")