import streamlit as st

from src.utils.load import load_config

if "instructions_config" not in st.session_state:
    st.session_state.instructions_config = load_config("instructions.toml")
