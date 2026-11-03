"""Base Agent implementation with Gemini 2.5 Flash REST client and robust error handling."""

from abc import ABC, abstractmethod
import json
import logging
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional
import httpx

from app.config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger("synapse.agents")


class BaseAgent(ABC):

    def __init__(
        self,
        name: str,
        role: str,
        system_instruction: str,
        color: str = "#3b82f6",
        avatar: str = "bot",
    ):
        self.name = name
        self.role = role
        self.system_instruction = system_instruction
        self.color = color
        self.avatar = avatar
        self.api_key = GEMINI_API_KEY
        self.model = GEMINI_MODEL

    async def call_llm(
        self,
        prompt: str,
        temperature: float = 0.4,
        max_tokens: int = 2048,
        response_schema: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Call Gemini API via REST with fallback handling."""
        if not self.api_key:
            logger.warning(
                f"[{self.name}] No GEMINI_API_KEY found. Using heuristic deterministic response."
            )
            return self.get_fallback_response(prompt)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        payload: Dict[str, Any] = {
            "system_instruction": {
                "parts": [{"text": self.system_instruction}]
            },
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
        }

        if response_schema:
            payload["generationConfig"]["responseMimeType"] = "application/json"
            payload["generationConfig"]["responseSchema"] = response_schema

        try:
            async with httpx.AsyncClient(timeout=25.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        text = candidates[0]["content"]["parts"][0]["text"]
                        return text
                else:
                    logger.error(
                        f"[{self.name}] API error ({resp.status_code}): {resp.text[:200]}"
                    )
        except Exception as e:
            logger.error(f"[{self.name}] Call error: {e}")

        # Graceful fallback to deterministic high-quality response
        return self.get_fallback_response(prompt)

    @abstractmethod
    def get_fallback_response(self, prompt: str) -> str:
        """Deterministic fallback response when offline or API limit reached."""
        pass
