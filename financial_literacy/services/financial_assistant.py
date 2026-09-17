"""
services/financial_assistant.py

AI backend abstraction for the Financial Literacy application.

Design:
  - FinancialAssistant is the public class used by the Streamlit pages.
  - It builds a safe, context-aware prompt and delegates to a backend.
  - The backend is swappable: set AI_BACKEND=watsonx|openai|stub in .env.
    Default is "stub" (works offline, returns a canned educational message).

Environment variables (loaded from .env):
  AI_BACKEND   : "stub" | "openai" | "watsonx"  (default: "stub")
  AI_API_URL   : Base URL of the API endpoint
  AI_API_KEY   : API key / token
  AI_MODEL_ID  : Model identifier
"""
from __future__ import annotations

import os
from typing import Optional

from utils.exceptions import AIServiceError

# Load .env if python-dotenv is installed (best-effort)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ------------------------------------------------------------------
# System prompt — defines the AI's role and safety boundaries
# ------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are a student financial literacy assistant. "
    "Your role is to explain financial concepts clearly and help students "
    "understand their options. "
    "Provide educational information, calculations, and budgeting guidance. "
    "Do not present yourself as a financial advisor. "
    "Do not make decisions for the user. "
    "Do not fabricate current scholarship, loan, interest-rate, or "
    "government-program information. "
    "When information may have changed, tell the user to verify it through "
    "an official source. "
    "Clearly explain assumptions and limitations. "
    "Use simple language suitable for college students in India. "
    "Always respond in plain text — do not use markdown formatting."
)


# ------------------------------------------------------------------
# Backend implementations
# ------------------------------------------------------------------

class _StubBackend:
    """
    Offline stub — returns a helpful placeholder without any API call.
    Used when no AI credentials are configured or for local development.
    """

    def query(self, prompt: str) -> str:  # noqa: ARG002
        return (
            "🤖 AI Assistant is running in offline (stub) mode.\n\n"
            "To enable real AI responses, add your API credentials to a "
            ".env file (see .env.example). "
            "The rest of the application works fully without AI.\n\n"
            "In a real deployment, IBM Bob / WatsonX would answer your "
            "financial literacy questions here."
        )


class _OpenAIBackend:
    """Calls an OpenAI-compatible chat completions endpoint."""

    def __init__(self, api_url: str, api_key: str, model_id: str) -> None:
        self._api_url = api_url.rstrip("/")
        self._api_key = api_key
        self._model_id = model_id

    def query(self, prompt: str) -> str:
        try:
            import requests  # type: ignore
        except ImportError:
            raise AIServiceError("'requests' library is not installed.")

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self._model_id,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.4,
            "max_tokens": 600,
        }
        try:
            response = requests.post(
                f"{self._api_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as exc:
            raise AIServiceError(f"OpenAI API call failed: {exc}") from exc


class _WatsonXBackend:
    """Calls a WatsonX / IBM Generative AI text-generation endpoint."""

    def __init__(self, api_url: str, api_key: str, model_id: str) -> None:
        self._api_url = api_url.rstrip("/")
        self._api_key = api_key
        self._model_id = model_id

    def query(self, prompt: str) -> str:
        try:
            import requests  # type: ignore
        except ImportError:
            raise AIServiceError("'requests' library is not installed.")

        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {prompt}\nAssistant:"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model_id": self._model_id,
            "input": full_prompt,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 600,
                "temperature": 0.4,
            },
        }
        try:
            response = requests.post(
                self._api_url,
                json=payload,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data["results"][0]["generated_text"].strip()
        except Exception as exc:
            raise AIServiceError(f"WatsonX API call failed: {exc}") from exc


# ------------------------------------------------------------------
# Public facade
# ------------------------------------------------------------------

class FinancialAssistant:
    """
    Public AI assistant facade.
    Selects the backend based on environment variables and exposes a
    single ask() method used by all Streamlit pages.
    """

    def __init__(self) -> None:
        self._backend = self._build_backend()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ask(self, question: str, context: Optional[str] = None) -> str:
        """
        Send a question to the AI backend, optionally enriched with
        financial context (e.g. current budget/spending summary).

        Returns the AI's response as a plain string.
        Raises AIServiceError on backend failure.
        """
        if not question or not question.strip():
            raise AIServiceError("Question cannot be empty.")

        prompt = self._build_prompt(question.strip(), context)
        return self._backend.query(prompt)

    def is_stub(self) -> bool:
        """Return True if the app is using the offline stub backend."""
        return isinstance(self._backend, _StubBackend)

    # ------------------------------------------------------------------
    # Prompt construction
    # ------------------------------------------------------------------

    @staticmethod
    def _build_prompt(question: str, context: Optional[str]) -> str:
        """
        Assemble a safe, context-enriched prompt.
        The system prompt is prepended by the backend (or included inline
        for WatsonX which uses a text completion format).
        """
        if context:
            return (
                f"Financial context for this student:\n{context}\n\n"
                f"Student's question: {question}"
            )
        return question

    # ------------------------------------------------------------------
    # Backend selection
    # ------------------------------------------------------------------

    @staticmethod
    def _build_backend():
        backend_name = os.getenv("AI_BACKEND", "stub").lower().strip()
        api_url = os.getenv("AI_API_URL", "")
        api_key = os.getenv("AI_API_KEY", "")
        model_id = os.getenv("AI_MODEL_ID", "")

        if backend_name == "openai" and api_url and api_key:
            return _OpenAIBackend(api_url, api_key, model_id)
        if backend_name == "watsonx" and api_url and api_key:
            return _WatsonXBackend(api_url, api_key, model_id)

        # Fall back to stub if credentials are missing or backend is unknown
        return _StubBackend()
