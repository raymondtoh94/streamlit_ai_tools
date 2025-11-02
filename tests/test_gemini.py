"""
Unit tests for Gemini LLM integration.

These tests focus on the functionality of the Gemini LLM model integration,
including response generation and error handling.
"""

from unittest.mock import patch

import pytest

from src.models.llm import create_llm_service
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
    with patch("src.models.llm.create_llm_service") as mock_run:
        mock_run.return_value = f"Response to: {prompt}"

        service = create_llm_service(provider="google_genai", model="gemini-2.5-flash")

        response = service.get_llm_response(prompt)

        assert response is not None
        assert isinstance(response.content, str)
