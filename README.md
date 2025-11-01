# 🚀 GenAI Tools Showcase

[![Python](https://img.shields.io/badge/python-3.13-blue?logo=python&logoColor=white)](https://www.python.org/) 
[![Streamlit](https://img.shields.io/badge/streamlit-1.51-orange?logo=streamlit&logoColor=white)](https://streamlit.io/)

---

## 🎯 Project Overview

**GenAI Tools Showcase** is an interactive Streamlit app designed to demonstrate various Generative AI tools in one unified interface. This project serves both as **documentation** for the tools and as a **portfolio project** to highlight my AI skills.

The app includes multiple pages, each dedicated to a specific AI tool with **live examples**, **descriptions**, and **usage guidelines**.

---

## 🛠 Features

### Core Components
- Streamlit-based interactive web interface
- Multi-page application structure
- Configurable API integration with GROQ and Google AI
- Environment variable management
- Modular code architecture

### AI Tools
- **Text Summarizer**
  - Multiple AI provider support (GROQ, Google)
  - Customizable system instructions
  - Model selection options
  - Real-time text summarization

### Technical Features
- LangChain integration for LLM operations
- Configurable model settings via TOML files
- Interactive UI components
- Comprehensive error handling
- Legal disclaimer integration
- Responsive layout design

### Developer Features
- Clean project structure
- Easy dependency management with `uv`
- Make commands for common operations
- Configuration-based model management
- Documentation and usage guidelines

---

## 💻 Setup Instructions

Follow these steps to clone the project and set up the environment using `uv`:

1. **Install Python 3.13** (if not already installed):

- Using **pyenv**:
```bash
pyenv install 3.13.0      # skip if already installed
pyenv local 3.13.0        # sets Python 3.13 for this project
python --version          # verify it shows Python 3.13.x
```

2. **Clone the repository**:
```bash
git clone https://github.com/raymondtoh94/streamlit_ai_tools.git
cd streamlit_ai_tools
```

3. **Install `uv`** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

4. **Setup and install dependencies**:
```bash
make init       # Initialize uv project
make install    # Install dependencies
```

5. **Configure API Keys**:
- Create or modify `.streamlit/secrets.toml` using the template provided:
```toml
[GROQ]
API_KEY="your-groq-api-key"

[GOOGLE]
API_KEY="your-google-api-key"
```
- Replace the placeholder values with your actual API keys
- Never commit this file to version control

6. **Run the application**:
```bash
make streamlit  # Start the Streamlit app
```

The app should now be running at `http://localhost:8501`

### 📝 Available Make Commands

- `make help` - Show all available commands
- `make init` - Initialize uv project
- `make install` - Install dependencies
- `make add pkg=<package>` - Add a new dependency
- `make remove pkg=<package>` - Remove a dependency
- `make run` - Run the main app
- `make streamlit` - Run Streamlit app
- `make test` - Run tests
- `make format` - Format code using black and isort

