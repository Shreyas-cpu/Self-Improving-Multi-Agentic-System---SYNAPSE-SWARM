"""Configuration module for SYNAPSE-SWARM.

Loads Gemini API key, server settings, and preset scenarios.
"""

import json
import os
from pathlib import Path
from typing import Optional


def get_gemini_api_key() -> Optional[str]:
    # 1. Environment variable
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"]

    # 2. Jarvis config
    jarvis_cfg = Path.home() / ".config" / "jarvis" / "config.json"
    if jarvis_cfg.exists():
        try:
            with open(jarvis_cfg, "r", encoding="utf-8") as f:
                data = json.load(f)
                key = data.get("gemini", {}).get("api_key")
                if key and not key.startswith("YOUR_"):
                    return key
        except Exception:
            pass

    return None


GEMINI_API_KEY = get_gemini_api_key()
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
SERVER_PORT = int(os.environ.get("PORT", "8765"))
SERVER_HOST = os.environ.get("HOST", "0.0.0.0")

# Maximum iterations per autonomous self-improvement cycle
MAX_ITERATIONS = 3
TARGET_BENCHMARK_SCORE = 92.0
