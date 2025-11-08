"""
This Page uses auto executed code blocks from agents to build a customized tool interface.
The tools generated are static utilities that don't require external APIs or ML models.
"""

# ------------------------------------------------------------------------
# Standard Library Imports
# ------------------------------------------------------------------------
import re
from datetime import datetime

# ------------------------------------------------------------------------
# Third Party Imports
# ------------------------------------------------------------------------
import streamlit as st

# ------------------------------------------------------------------------
# Local Imports
# ------------------------------------------------------------------------
from src.models.llm import create_llm_service
from src.utils.environment import initialize_environment
from src.utils.logger import setup_logger

# ------------------------------------------------------------------------
# Initialization and Configuration
# ------------------------------------------------------------------------
# Initialize environment and logging
initialize_environment()
logger = setup_logger("customized_tools")

# Configure page
st.set_page_config(page_title="Customized Tools")
st.title("Customized Tools")


# ------------------------------------------------------------------------
# System Instructions
# ------------------------------------------------------------------------
sys_instr = """You are an expert Stream Lit developer focusing on static programming tools.
You will generate code for customized tools based on user requirements, but ONLY create tools that use standard programming operations
and utilities (no machine learning, AI, or external API calls).

Important Instructions:
1. Return your answer as python code delimiter within <execute_python> </execute_python> tags.
2. For ALL interactive elements (buttons, inputs, etc.), use unique keys:
   - st.button("Click me", key="unique_button_1")
   - st.text_input("Enter text", key="unique_input_1")

3. Initialize ALL required session state variables at the start of your code:
   - if 'variable_name' not in st.session_state:
       st.session_state.variable_name = initial_value

4. For any button interactions, use callbacks to handle the logic:
   def button_callback():
       st.session_state.result = process_data()

   st.button("Process", key="process_btn", on_click=button_callback)

5. Always show the current state or results:
   if 'result' in st.session_state:
       st.write(st.session_state.result)

6. Structure your code in this order:
   - Session state initialization
   - Function definitions
   - UI elements
   - Result display

7. Use st.form when multiple inputs need to be submitted together:
   with st.form(key="my_form"):
       # form elements
       submitted = st.form_submit_button("Submit")

8. Handle errors gracefully and show meaningful messages to users:
   try:
       # your code
   except Exception as e:
       st.error(f"Error: {str(e)}")
"""


# ------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------
def save_code_blocks(code_blocks: list[str], timestamp: str) -> None:
    """Save generated code blocks to a file with timestamp."""
    try:
        file_path = f"logs/generated_tools_{timestamp}.py"
        with open(file_path, "w") as f:
            f.write("# Generated Tools\n\n")
            for i, code in enumerate(code_blocks, 1):
                f.write(f"# Code Block {i}\n")
                f.write(code + "\n\n")
        logger.info(f"Saved generated code blocks to {file_path}")
    except Exception as e:
        logger.error(f"Error saving code blocks: {e}")


def generate_and_execute_tools(user_requirements: str) -> None:
    """Generate and execute customized tools based on user requirements."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Log user requirements
    try:
        with open("logs/user_requirements.log", "a") as f:
            f.write(f"[{timestamp}] User Requirements:\n{user_requirements}\n\n")
        logger.info(f"Logged user requirements at {timestamp}")
    except Exception as e:
        logger.error(f"Error logging user requirements: {e}")

    # Generate tool using LLM
    llm_service = create_llm_service(
        model="gemini-2.5-flash",
        provider="google_genai",
    )

    response = llm_service.get_llm_response(
        f"{sys_instr}\n\n User Requirements:\n{user_requirements}"
    )

    # Extract code blocks
    response_content = (
        str(response.content) if hasattr(response, "content") else str(response)
    )
    code_blocks = re.findall(
        r"<execute_python>(.*?)</execute_python>", response_content, re.DOTALL
    )

    # Store code blocks in session state to persist across refreshes
    st.session_state.code_blocks = code_blocks
    st.session_state.timestamp = timestamp

    # Execute each code block
    for i, code in enumerate(code_blocks, 1):
        st.markdown(f"#### 🔧 Generated Tool Code Block {i}")
        try:
            exec(code, globals())
            logger.info(f"[{timestamp}] Successfully executed code block {i}")
        except Exception as e:
            st.error(f"Error executing code block {i}: {str(e)}")
            logger.error(f"[{timestamp}] Error executing code block {i}: {e}")

    if not code_blocks:
        st.error(
            "No valid tools were generated. Please try rephrasing your requirements."
        )
        logger.warning(f"[{timestamp}] No valid code blocks generated")
        return

    # Save generated code blocks
    save_code_blocks(code_blocks, timestamp)
    logger.info(f"[{timestamp}] Generated {len(code_blocks)} code blocks")


# ------------------------------------------------------------------------
# UI Elements
# ------------------------------------------------------------------------
# Initialize session state for code blocks if not present
if "code_blocks" not in st.session_state:
    st.session_state.code_blocks = []
    st.session_state.timestamp = None

st.markdown("### ✍️ Tool Requirements")
user_requirements = st.text_area(
    "Enter your requirements for customized tools:", height=150
)

if st.button("Generate Tools", key="generate_tools_btn"):
    if not user_requirements.strip():
        st.error("Please enter your tool requirements before generating.")
    else:
        generate_and_execute_tools(user_requirements)

# Re-execute stored code blocks on page refresh
if st.session_state.code_blocks:
    for i, code in enumerate(st.session_state.code_blocks, 1):
        st.markdown(f"#### 🔧 Generated Tool Code Block {i}")
        try:
            exec(code, globals())
        except Exception as e:
            st.error(f"Error executing code block {i}: {str(e)}")
            logger.error(f"Error re-executing code block {i}: {e}")

# Footer
st.markdown("---")
st.markdown("### 💡 Available Features")
st.info(
    """
**Data Processing:**
- Numerical computations with NumPy
- Data manipulation with Pandas
- Statistical analysis with SciPy/StatsModels

**Visualization:**
- Charts and plots using Matplotlib/Seaborn
- Interactive visualizations with Plotly/Bokeh
- Data dashboards with Streamlit components

**Examples:**
- "Create a tool to analyze CSV data with basic statistics"
- "Build a data visualization dashboard for time series data"
- "Make a calculator for statistical hypothesis testing"
- "Create a tool for data cleaning and validation"
"""
)
