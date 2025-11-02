"""
Unit tests for Agent LLM integration.

These tests focus on the functionality of the Agent LLM model integration,
including response generation and error handling.
"""

from unittest.mock import patch

import pytest

from src.models.llm import run_agent
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

        config = {"configurable": {"thread_id": "1"}}

        agent = run_agent(
            selected_provider="groq",
            selected_model="llama-3.1-8b-instant",
            tools=[],
        )

        response = agent.invoke(
            {"messages": [{"role": "user", "content": f"{prompt}"}]},
            config=config,
        )

        ai_response = response["messages"][-1].content

        assert response is not None
        assert isinstance(ai_response, str)
