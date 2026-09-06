"""Pytest suite for pure-logic modules (no Ollama / network required).

Run with:
    pytest -q
from the project root (after `pip install -r requirements.txt`).
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kohler_agent.exporters import export_response_files
from kohler_agent.formatting import extract_json, format_output, infer_requested_format
from kohler_agent.ingestion import split_text
from kohler_agent.memory import build_reference_context


def test_split_text_produces_nonempty_chunks():
    chunks = split_text("Alpha paragraph.\n\nBeta paragraph. " * 80)
    assert chunks
    assert all(chunk.strip() for chunk in chunks)


def test_split_text_empty_input():
    assert split_text("") == []
    assert split_text("   \n  ") == []


def test_extract_json_from_fenced_block():
    assert extract_json('```json\n{"ok": true}\n```') == {"ok": True}


def test_extract_json_returns_none_for_plain_text():
    assert extract_json("just a sentence, no JSON here") is None


def test_infer_requested_format_detects_email_intent():
    assert infer_requested_format("draft the mail for this", "markdown") == "email"


def test_infer_requested_format_respects_explicit_selection():
    # A non-markdown sidebar selection should never be overridden.
    assert infer_requested_format("draft the mail for this", "json") == "json"


def test_infer_requested_format_detects_named_formats():
    assert infer_requested_format("give me this as json", "markdown") == "json"
    assert infer_requested_format("export as csv please", "markdown") == "csv"


def test_build_reference_context_includes_prior_answer():
    reference = build_reference_context(
        [
            {"role": "user", "content": "Summarise policy"},
            {"role": "assistant", "content": "The policy says X."},
        ]
    )
    assert "The policy says X." in reference


def test_build_reference_context_empty_history():
    assert "no previous assistant answer" in build_reference_context([])


def test_format_output_xml_is_well_formed_even_with_special_characters():
    xml_text = format_output("5 < 6 & safe", "xml", [])
    ET.fromstring(xml_text)  # raises ET.ParseError if malformed


def test_export_response_files_covers_every_format():
    files = export_response_files("A response", "markdown", ["policy.md"])
    expected = {"txt", "md", "json", "xml", "csv", "html", "docx", "xlsx", "pdf", "zip"}
    assert expected <= set(files)
    for data, filename, mime in files.values():
        assert data and filename and mime
