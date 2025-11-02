"""
LLM and Agent execution functions.

This module provides functions to run language models (LLMs) and agents
using specified providers and models.
"""

from typing import List

import streamlit as st
from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelFallbackMiddleware,
    SummarizationMiddleware,
    ToolCallLimitMiddleware,
)
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver


def run_llm(selected_provider: str, selected_model: str, prompt: str):

    model = init_chat_model(
        model=selected_model,
        model_provider=selected_provider,
    )

    response = model.invoke(f"{prompt}")
    return response


def run_agent(selected_provider: str, selected_model: str, tools: List):

    # Initialize memory only once
    if "checkpointer" not in st.session_state:
        st.session_state.checkpointer = InMemorySaver()

    checkpointer = st.session_state.checkpointer

    # Limit all tool calls
    global_limiter = ToolCallLimitMiddleware(thread_limit=6, run_limit=20)

    # Optional summarization middleware to manage long conversations
    summarizer = SummarizationMiddleware(
        model="groq:llama-3.3-70b-versatile",
        max_tokens_before_summary=4000,  # Trigger summarization at 4000 tokens
        messages_to_keep=20,  # Keep last 20 messages after summary
        summary_prompt=st.session_state.instructions_config["travel_info_agent"].get(
            "summarizer_prompt", ""
        ),
    )

    # Optional model fallback middleware
    fallback_model = ModelFallbackMiddleware(
        "groq:llama-3.3-70b-versatile", "google_genai:gemini-2.5-flash-lite"
    )

    # Create the agent with specified model, tools, and middleware
    agent = create_agent(
        model=f"{selected_provider}:{selected_model}",
        system_prompt=st.session_state.instructions_config["travel_info_agent"].get(
            "sys_prompt", ""
        ),
        tools=tools,
        middleware=[global_limiter, summarizer, fallback_model],
        checkpointer=checkpointer,
    )

    return agent
