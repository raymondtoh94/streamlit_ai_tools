import streamlit as st

from src.utils.load import initialize_environment

# Initialize environment variables
initialize_environment()

# ---- PAGE SETUP ----
st.set_page_config(page_title="Raymond's Portfolio", page_icon="💼", layout="wide")


# ---- HEADER SECTION ----
st.title("👋 Hi, I'm Raymond")
st.subheader("An Applied Machine Learning & Data Science Enthusiast")

# ---- ABOUT SECTION ----
st.header("About Me")
st.write(
    """
As a passionate data scientist, I firmly believe in the power of data-driven solutions to transform businesses and solve complex problems. My approach emphasizes the critical importance of quality data, adhering to the principle of "garbage in, garbage out." For me, data is the most crucial component in building robust models and deriving meaningful insights.

Beyond my technical expertise, I understand the value of domain knowledge in comprehending problem statements and business requirements. This understanding allows me to bridge the gap between data science and business needs, delivering solutions that are both technically sound and practically valuable.
"""
)

# ---- SKILLS SECTION ----
st.header("Skills")
cols = st.columns(3)
with cols[0]:
    st.markdown("**Tech Stack:**: Python, SQL, Bash, Spark, Pandas")
with cols[1]:
    st.markdown(
        "**Frameworks:** TensorFlow, Scikit-Learn, Keras, Hugging Face, LangChain, Streamlit"
    )
with cols[2]:
    st.markdown(
        "**Tools:** VS Code, Git, AWS, Azure, Kubernetes, Docker, CI/CD Pipelines, Jupyter"
    )

# ---- CONTACT SECTION ----
st.header("Contact")
st.write("📧 Email: raymondtkh94@gmail.com")
st.write("🌐 LinkedIn: [Your LinkedIn](https://www.linkedin.com/in/raymondtkh94)")
st.write("💻 GitHub: [Your GitHub](https://github.com/raymondtoh94)")

# ---- FOOTER ----
st.markdown("---")
st.write("© 2025 Raymond | Built with Streamlit 💡")
