"""Central configuration for the KOHLER Unified Enterprise AI Agent.

All environment-driven paths, model names, and tunables live here so that
every other module imports its configuration from a single place instead of
re-reading environment variables.
"""

from __future__ import annotations

import os
from pathlib import Path

# src/kohler_agent/config.py -> src/kohler_agent -> src -> <project root>
PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent.parent

KNOWLEDGE_DIR = Path(
    os.getenv("KOHLER_KNOWLEDGE_DIR", str(PROJECT_ROOT / "knowledge_base"))
).expanduser()

MEMORY_FILE = Path(
    os.getenv("KOHLER_MEMORY_FILE", str(PROJECT_ROOT / "conversation_memory.json"))
).expanduser()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
CHAT_MODEL = os.getenv("KOHLER_CHAT_MODEL", "qwen2.5:3b")
EMBED_MODEL = os.getenv("KOHLER_EMBED_MODEL", "nomic-embed-text")

TOP_K = int(os.getenv("KOHLER_TOP_K", "5"))
MIN_RELEVANCE_SCORE = float(os.getenv("KOHLER_MIN_RELEVANCE", "0.20"))

MAX_MEMORY_MESSAGES = int(os.getenv("KOHLER_MAX_MEMORY_MESSAGES", "40"))
CHUNK_SIZE = int(os.getenv("KOHLER_CHUNK_SIZE", "1400"))
CHUNK_OVERLAP = int(os.getenv("KOHLER_CHUNK_OVERLAP", "220"))

SUPPORTED_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".yaml", ".yml", ".pdf", ".docx"}

APP_TITLE = "KOHLER Unified Enterprise AI Agent"
