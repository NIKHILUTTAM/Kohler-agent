"""Conversation memory: local persistence and follow-up reference context.

Memory is stored as a flat JSON file on disk (no database) which keeps the
prototype trivially inspectable and portable, matching the "local-first"
design goal of Track 3.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import config


def load_conversation_memory(path: Path = config.MEMORY_FILE) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            return []
        valid: list[dict[str, Any]] = []
        for item in payload:
            if (
                not isinstance(item, dict)
                or item.get("role") not in {"user", "assistant"}
                or not isinstance(item.get("content"), str)
                or not item["content"].strip()
            ):
                continue
            clean: dict[str, Any] = {"role": item["role"], "content": item["content"]}
            if item.get("format"):
                clean["format"] = str(item["format"])
            if isinstance(item.get("sources"), list):
                clean["sources"] = [str(source) for source in item["sources"]]
            valid.append(clean)
        return valid[-config.MAX_MEMORY_MESSAGES :]
    except (OSError, json.JSONDecodeError, TypeError):
        return []


def save_conversation_memory(
    messages: list[dict[str, Any]], path: Path = config.MEMORY_FILE
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(messages[-config.MAX_MEMORY_MESSAGES :], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(path)


def clear_conversation_memory(path: Path = config.MEMORY_FILE) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def build_reference_context(history: list[dict[str, Any]]) -> str:
    """Summarise the most recent user/assistant turn so the reasoning node
    can resolve follow-ups like "draft the mail for this"."""
    previous_assistant = next(
        (item.get("content", "") for item in reversed(history) if item.get("role") == "assistant"),
        "",
    )
    previous_user = next(
        (item.get("content", "") for item in reversed(history) if item.get("role") == "user"),
        "",
    )
    if not previous_assistant:
        return "(no previous assistant answer is available)"
    return (
        f"Most recent user request:\n{previous_user[-2000:]}\n\n"
        f"Most recent assistant answer:\n{previous_assistant[-5000:]}"
    )
