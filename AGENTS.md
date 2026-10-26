# AGENTS.md

## Project overview

This repository contains the AIE2026 course exercises. The main Python application is under `app/`, course data is under `data/`, and each lecture's written work is under `lectures/`.

## Environment and commands

- Use `uv` for dependency management and command execution.
- Install or synchronize dependencies with `uv sync` when needed.
- Run the full test suite with `uv run pytest -q`.
- Run a Python module with `uv run python -m <module>`.
- Run a syntax check with `python3 -m py_compile <file>`.
- Check whitespace errors with `git diff --check`.

## Code guidelines

- Keep changes focused on the current exercise and preserve existing public APIs unless the task requires otherwise.
- Add concise English comments only for non-obvious new logic.
- Preserve the existing Python style and type annotations.
- Do not add unnecessary dependencies or unrelated refactors.

## Secrets and API usage

- Never hard-code, print, commit, or document `GEMINI_API_KEY`.
- The Gemini API key must be provided through the `GEMINI_API_KEY` environment variable or the configured Codespaces secret.
- Be mindful of free-tier rate limits when running live model calls.