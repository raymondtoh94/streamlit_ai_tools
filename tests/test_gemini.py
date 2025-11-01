from unittest.mock import patch

import pytest

from src.models.llm import run_llm
from src.utils.environment import initialize_environment

# Initialize environment variables for testing
initialize_environment()


# Mocked version for unit testing without calling real API
@pytest.mark.parametrize(
    "prompt",
    [
        "Hello, how are you?",
    ],
)
def test_run_llm_parametrized(prompt):
    """Test run_llm with multiple prompts using mocking."""
    with patch("src.models.llm.run_llm") as mock_run:
        mock_run.return_value = f"Response to: {prompt}"

        response = run_llm("google_genai", "gemini-2.5-flash", prompt)

        assert response is not None
        assert isinstance(response.content, str)
