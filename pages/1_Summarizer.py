import streamlit as st
from src.utils.load import load_config

# Load config
instructions = load_config(
    "instructions.toml"
)

st.set_page_config(page_title="Summarizer")

st.title("Text Summarizer")
sys_instr = st.text_area("System Instructions", height=100, value=instructions["summarizer"].get("instruction", ""))

if prompt := st.chat_input():
    st.write(f"System Prompt: {sys_instr}")
    st.write(f"Summarizing the following text: {prompt}")


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