"""
LLM module providing factory patterns for creating and running language models and agents.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

import streamlit as st
from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelFallbackMiddleware,
    SummarizationMiddleware,
    ToolCallLimitMiddleware,
)
from langchain.chat_models import BaseChatModel, init_chat_model
from langgraph.checkpoint.memory import InMemorySaver


@dataclass
class LLMConfig:
    """Configuration for LLM initialization."""

    provider: str
    model: str
    system_prompt: Optional[str] = None
    tools: Optional[List] = None


@dataclass
class MiddlewareConfig:
    """Configuration for middleware settings."""

    enabled: bool
    settings: Dict


class LLMFactory:
    """Factory class for creating and managing LLM instances."""

    @staticmethod
    def create_middleware(config: Dict) -> List:
        """Create middleware based on configuration."""
        middleware = []

        # Tool Limit Middleware
        if config.get("tool_limit", {}).get("enabled", False):
            tool_config = config["tool_limit"]
            middleware.append(
                ToolCallLimitMiddleware(
                    thread_limit=tool_config.get("thread_limit", 6),
                    run_limit=tool_config.get("run_limit", 20),
                )
            )

        # Summarization Middleware
        if config.get("summarization", {}).get("enabled", False):
            sum_config = config["summarization"]
            middleware.append(
                SummarizationMiddleware(
                    model=sum_config.get("model"),
                    max_tokens_before_summary=sum_config.get("max_tokens", 4000),
                    messages_to_keep=sum_config.get("messages_to_keep", 20),
                    summary_prompt=st.session_state.instructions_config[
                        "travel_info_agent"
                    ].get("summarizer_prompt", ""),
                )
            )

        # Model Fallback Middleware
        if config.get("model_fallback", {}).get("enabled", False):
            fallback_config = config["model_fallback"]
            middleware.append(
                ModelFallbackMiddleware(
                    fallback_config.get("primary_model"),
                    fallback_config.get("fallback_model"),
                )
            )

        return middleware

    @staticmethod
    def create_llm(config: LLMConfig) -> BaseChatModel:
        """Create a basic LLM instance."""
        return init_chat_model(
            model=config.model,
            model_provider=config.provider,
        )

    @staticmethod
    def create_agent(config: LLMConfig):
        """Create an agent with specified configuration and middleware."""
        if "checkpointer" not in st.session_state:
            st.session_state.checkpointer = InMemorySaver()

        middleware = LLMFactory.create_middleware(st.session_state.middleware_config)

        return create_agent(
            model=f"{config.provider}:{config.model}",
            system_prompt=config.system_prompt,
            tools=config.tools,
            middleware=middleware,
            checkpointer=st.session_state.checkpointer,
        )


class LLMService:
    """Service class for handling LLM operations."""

    def __init__(self, config: LLMConfig):
        self.config = config
        self._llm = None
        self._agent = None

    def setup_llm(self) -> None:
        """Initialize LLM if not already initialized."""
        if self._llm is None:
            self._llm = LLMFactory.create_llm(self.config)

    def setup_agent(self) -> None:
        """Initialize agent if not already initialized."""
        if self._agent is None:
            self._agent = LLMFactory.create_agent(self.config)

    def get_llm_response(self, prompt: str) -> str:
        """Generate response using basic LLM."""
        self.setup_llm()
        return self._llm.invoke(prompt)

    def get_agent_stream(
        self, messages: List[dict], config: Optional[dict] = None
    ) -> dict:
        """Get streaming response from agent."""
        self.setup_agent()
        return self._agent.stream(
            {"messages": messages}, stream_mode="updates", config=config or {}
        )

    def get_agent_response(
        self, messages: List[dict], config: Optional[dict] = None
    ) -> dict:
        """Get full response from agent."""
        self.setup_agent()
        return self._agent.invoke({"messages": messages}, config=config or {})


def create_llm_service(
    provider: str,
    model: str,
    system_prompt: Optional[str] = None,
    tools: Optional[List] = None,
) -> LLMService:
    """Create an LLM service instance with specified configuration."""
    config = LLMConfig(
        provider=provider, model=model, system_prompt=system_prompt, tools=tools
    )
    return LLMService(config)
