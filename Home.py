"""
Portfolio Home Page

This is the main landing page of the portfolio website. It displays personal information,
skills, and contact details in a clean, organized layout.
"""

import streamlit as st

from src.utils.environment import initialize_environment
from src.utils.logger import setup_logger

# ------------------------------------------------------------------------
# Initialization
# ------------------------------------------------------------------------
# Initialize environment and logging
initialize_environment()
logger = setup_logger("home")

# ------------------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------------------
st.set_page_config(page_title="Raymond's Portfolio", page_icon="💼", layout="wide")

# ------------------------------------------------------------------------
# Header Section
# ------------------------------------------------------------------------
st.title("👋 Hi, I'm Raymond")
st.subheader("An Applied Machine Learning & Data Science Enthusiast")

# ------------------------------------------------------------------------
# About Section
# ------------------------------------------------------------------------
st.header("About Me")
st.write(
    """
As a passionate data scientist, I firmly believe in the power of data-driven solutions
to transform businesses and solve complex problems. My approach emphasizes the critical
importance of quality data, adhering to the principle of "garbage in, garbage out."
For me, data is the most crucial component in building robust models and deriving
meaningful insights.

Beyond my technical expertise, I understand the value of domain knowledge in
comprehending problem statements and business requirements. This understanding allows
me to bridge the gap between data science and business needs, delivering solutions
that are both technically sound and practically valuable.
"""
)

# ------------------------------------------------------------------------
# Skills Section
# ------------------------------------------------------------------------
st.header("Skills")
cols = st.columns(3)

# Technical Skills
with cols[0]:
    st.markdown("**Tech Stack:** Python, SQL, Bash, Spark, Pandas")

# Frameworks
with cols[1]:
    st.markdown(
        "**Frameworks:** TensorFlow, Scikit-Learn, Keras, Hugging Face, LangChain, Streamlit"
    )

# Tools
with cols[2]:
    st.markdown(
        "**Tools:** VS Code, Git, AWS, Azure, Kubernetes, Docker, CI/CD Pipelines, Jupyter"
    )

# ------------------------------------------------------------------------
# Contact Section
# ------------------------------------------------------------------------
st.header("Contact")
st.write("📧 Email: raymondtkh94@gmail.com")
st.write("🌐 LinkedIn: [Your LinkedIn](https://www.linkedin.com/in/raymondtkh94)")
st.write("💻 GitHub: [Your GitHub](https://github.com/raymondtoh94)")

# ------------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------------
st.markdown("---")
st.write("© 2025 Raymond | Built with Streamlit 💡")
