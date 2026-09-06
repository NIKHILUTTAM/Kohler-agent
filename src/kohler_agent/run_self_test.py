"""Fast, dependency-light self-test.

Exercises every pure-logic module (chunking, format detection, output
rendering, multi-format export) WITHOUT requiring Ollama or any network
access, so it can run in CI or as a quick "did I break anything" check
before wiring up the local LLM.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET

from .exporters import export_response_files
from .formatting import extract_json, format_output, infer_requested_format
from .ingestion import split_text
from .memory import build_reference_context


def run_self_test() -> None:
    chunks = split_text("Alpha paragraph.\n\nBeta paragraph. " * 80)
    assert chunks and all(chunk.strip() for chunk in chunks), "chunking produced empty output"

    assert extract_json('```json\n{"ok": true}\n```') == {"ok": True}, "fenced JSON not extracted"

    assert infer_requested_format("draft the mail for this", "markdown") == "email", (
        "email intent not detected"
    )

    reference = build_reference_context(
        [
            {"role": "user", "content": "Summarise policy"},
            {"role": "assistant", "content": "The policy says X."},
        ]
    )
    assert "The policy says X." in reference, "reference context missing prior answer"

    ET.fromstring(format_output("5 < 6 & safe", "xml", []))  # raises if malformed

    files = export_response_files("A response", "markdown", ["policy.md"])
    assert {"pdf", "xlsx", "docx", "json", "xml", "csv", "zip"} <= set(files), (
        "one or more export formats missing"
    )

    print("SELF-TEST PASSED: chunking, formatting, and all exporters are working.")


if __name__ == "__main__":
    run_self_test()
