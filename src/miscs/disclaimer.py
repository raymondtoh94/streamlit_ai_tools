"""
Legal disclaimer dialog for the application.

This module defines a Streamlit dialog that displays a legal disclaimer
to inform users about the limitations and responsibilities associated with
the use of AI-generated content.
"""

import streamlit as st


@st.dialog("Legal disclaimer")
def show_disclaimer_dialog():
    st.caption(
        """
        This application uses a Large Language Model (LLM) to generate responses.
        Please be aware that:
        - The model may produce **inaccurate or biased information**.
        - The model does not replace professional advice (legal, medical, financial, etc.).
        - Use outputs at your own discretion.

        By using this app, you acknowledge that the developers are **not responsible** for decisions made based on the generated content.
        """
    )
