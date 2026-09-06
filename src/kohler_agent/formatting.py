"""Requested-format detection and final answer formatting (Markdown/JSON/XML/CSV/email)."""

from __future__ import annotations

import csv
import html
import json
import re
from io import StringIO
from typing import Any


def infer_requested_format(question: str, selected_format: str) -> str:
    """The sidebar dropdown sets a default, but a user typing "draft the
    email for this" or "give me JSON" should override it for that turn."""
    selected = selected_format.lower().strip()
    if selected != "markdown":
        return selected
    if re.search(
        r"\b(draft|write|compose|prepare|send)\b.{0,40}\b(email|e-mail|mail)\b"
        r"|\b(email|e-mail)\b.{0,40}\b(draft|write|compose|prepare)\b",
        question,
        flags=re.I,
    ):
        return "email"
    for output_format in ("json", "xml", "csv"):
        if re.search(rf"\b{output_format}\b", question, flags=re.I):
            return output_format
    return selected


def extract_json(text: str) -> Any | None:
    candidates = [text.strip()]
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, flags=re.I | re.S)
    if fenced:
        candidates.insert(0, fenced.group(1).strip())
    for opener, closer in [("{", "}"), ("[", "]")]:
        start, end = text.find(opener), text.rfind(closer)
        if start >= 0 and end > start:
            candidates.append(text[start : end + 1])
    for candidate in candidates:
        try:
            return json.loads(candidate)
        except (json.JSONDecodeError, TypeError):
            continue
    return None


def format_output(draft: str, requested_format: str, sources: list[str]) -> str:
    draft = draft.strip() or "The local model returned an empty response."
    requested_format = requested_format.lower()
    if requested_format == "json":
        parsed = extract_json(draft)
        if parsed is None:
            parsed = {"answer": draft, "sources": sources, "grounded": bool(sources)}
        elif isinstance(parsed, dict):
            parsed.setdefault("sources", sources)
        return json.dumps(parsed, indent=2, ensure_ascii=False)
    if requested_format == "xml":
        return (
            "<response>\n"
            f"  <answer>{html.escape(draft)}</answer>\n"
            f"  <sources>{html.escape(', '.join(sources) or 'none')}</sources>\n"
            "</response>"
        )
    if requested_format == "csv":
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=["answer", "sources", "grounded"])
        writer.writeheader()
        writer.writerow({"answer": draft, "sources": "; ".join(sources), "grounded": bool(sources)})
        return output.getvalue().strip()
    if requested_format == "email" and not re.search(r"^\s*subject\s*:", draft, flags=re.I | re.M):
        return (
            "Subject: Response from the KOHLER Unified Enterprise AI Agent\n\n"
            f"Hello,\n\n{draft}\n\nBest regards,\n"
            "KOHLER Unified Enterprise AI Agent"
        )
    return draft
