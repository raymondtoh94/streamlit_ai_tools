# -----------------------------
# Common Makefile for uv-based Python projects
# -----------------------------

# Variables
PYTHON := uv run python
APP := Home.py

# Default target
.DEFAULT_GOAL := help

# -----------------------------
# Targets
# -----------------------------

.PHONY: help
help:  ## Show available commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[1;32m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: init
init:  ## Initialize uv project (create pyproject.toml and venv)
	uv init

.PHONY: install
install:  ## Install all dependencies
	uv sync

.PHONY: add
add:  ## Add a new dependency (usage: make add pkg=<package>)
	uv add $(pkg)

.PHONY: remove
remove:  ## Remove a dependency (usage: make remove pkg=<package>)
	uv remove $(pkg)

.PHONY: run
run:  ## Run the main app (default: app.py)
	uv run $(PYTHON) $(APP)

.PHONY: streamlit
streamlit:  ## Run Streamlit app
	uv run streamlit run $(APP)

.PHONY: test
test:  ## Run pytest
	uv run pytest -v

.PHONY: format
format:  ## Format code using black and isort
	uv run black .
	uv run isort .

.PHONY: lint
lint:  ## Run flake8 or ruff linter
	uv run ruff check .

.PHONY: clean
clean:  ## Remove cache and temporary files
	rm -rf __pycache__ .pytest_cache .ruff_cache
	find . -type d -name '*.egg-info' -exec rm -rf {} +

