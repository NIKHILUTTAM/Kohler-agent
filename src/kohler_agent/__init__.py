"""KOHLER Unified Enterprise AI Agent - a local-first RAG + LangGraph agent.

Public API re-exported here so callers can do:

    from kohler_agent import build_graph, export_response_files

instead of reaching into individual submodules.
"""

from __future__ import annotations

from . import config
from .exporters import EXPORT_LABELS, export_response_files
from .formatting import extract_json, format_output, infer_requested_format
from .graph import AgentState, build_graph
from .ingestion import ensure_demo_knowledge_base, load_documents, split_text
from .memory import (
    build_reference_context,
    clear_conversation_memory,
    load_conversation_memory,
    save_conversation_memory,
)
from .retrieval import SemanticIndex

__all__ = [
    "config",
    "AgentState",
    "build_graph",
    "EXPORT_LABELS",
    "export_response_files",
    "extract_json",
    "format_output",
    "infer_requested_format",
    "ensure_demo_knowledge_base",
    "load_documents",
    "split_text",
    "build_reference_context",
    "clear_conversation_memory",
    "load_conversation_memory",
    "save_conversation_memory",
    "SemanticIndex",
]

__version__ = "1.0.0"
