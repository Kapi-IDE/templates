"""Reusable Gemini client wrapper for healthcare agents."""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, Optional

import google.generativeai as genai

logger = logging.getLogger(__name__)


class GeminiClient:
    """Lightweight wrapper around the Gemini generative model.

    Responsible for configuring the SDK, generating plain text responses, and
    producing structured JSON output with graceful fallbacks. The class is
    intentionally stateless so multiple agents can share an instance.
    """

    def __init__(
        self,
        model_name: str = "gemini-pro",
        api_key: Optional[str] = None,
    ) -> None:
        api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")

        genai.configure(api_key=api_key)
        self._model_name = model_name
        self._model = genai.GenerativeModel(model_name)
        logger.debug("GeminiClient initialised with model %s", model_name)

    def generate_text(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a plain text response for a given prompt.

        Args:
            prompt: Natural language instruction/question.
            context: Optional dictionary that will be rendered alongside the
                prompt to provide additional grounding for the model.
        """
        if context:
            prompt = self._render_context(context) + prompt

        response = self._model.generate_content(prompt)
        if not getattr(response, "text", None):
            raise ValueError("Empty response from Gemini API")
        return response.text.strip()

    def generate_json(self, prompt: str) -> Dict[str, Any]:
        """Request JSON output from Gemini and parse it into a dictionary."""
        response = self._model.generate_content(prompt)
        if not getattr(response, "text", None):
            raise ValueError("Empty response from Gemini API")
        return json.loads(response.text)

    def health_check(self) -> bool:
        """Verify the client can reach Gemini and produce output."""
        try:
            self.generate_text("health check")
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error("Gemini health check failed: %s", exc)
            return False
        return True

    @staticmethod
    def _render_context(context: Dict[str, Any]) -> str:
        safe_json = json.dumps(context, indent=2, default=str)
        return f"\nCONTEXT:\n{safe_json}\n"
