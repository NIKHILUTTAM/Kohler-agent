"""Document discovery, text extraction, and chunking for the knowledge base."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

from . import config
from .demo_content import DEMO_FILES


def split_text(
    text: str,
    size: int = config.CHUNK_SIZE,
    overlap: int = config.CHUNK_OVERLAP,
) -> list[str]:
    """Split text into overlapping chunks, breaking on paragraph/sentence
    boundaries where possible so a chunk doesn't cut a sentence in half."""
    cleaned = re.sub(r"\r\n?", "\n", text).strip()
    if not cleaned:
        return []
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("size must be positive and overlap must be between 0 and size")
    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(start + size, len(cleaned))
        if end < len(cleaned):
            boundary = max(
                cleaned.rfind("\n\n", start, end),
                cleaned.rfind(". ", start, end),
                cleaned.rfind(" ", start, end),
            )
            if boundary > start + size // 2:
                end = boundary + (2 if cleaned[boundary : boundary + 2] == ". " else 1)
        piece = cleaned[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= len(cleaned):
            break
        start = max(end - overlap, start + 1)
    return chunks


def ensure_demo_knowledge_base(folder: Path = config.KNOWLEDGE_DIR) -> None:
    """Seed the knowledge base folder with synthetic demo documents the very
    first time it's empty, so the app is usable out of the box."""
    folder.mkdir(parents=True, exist_ok=True)
    has_supported_file = any(
        item.is_file() and item.suffix.lower() in config.SUPPORTED_EXTENSIONS
        for item in folder.rglob("*")
    )
    if not has_supported_file:
        for filename, content in DEMO_FILES.items():
            (folder / filename).write_text(content, encoding="utf-8")


def _extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader

        return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
    if suffix == ".docx":
        from docx import Document as DocxDocument

        return "\n".join(paragraph.text for paragraph in DocxDocument(str(path)).paragraphs)
    return path.read_text(encoding="utf-8", errors="ignore")


def load_documents(folder: Path = config.KNOWLEDGE_DIR) -> list[Any]:
    """Load, extract, and chunk every supported file in the knowledge base
    folder into LangChain Document objects tagged with their source file."""
    from langchain_core.documents import Document

    ensure_demo_knowledge_base(folder)
    documents: list[Any] = []
    for path in sorted(folder.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in config.SUPPORTED_EXTENSIONS:
            continue
        try:
            text = _extract_text(path)
            source = str(path.relative_to(folder))
            for number, chunk in enumerate(split_text(text), start=1):
                documents.append(
                    Document(page_content=chunk, metadata={"source": source, "chunk": number})
                )
        except Exception as exc:  # noqa: BLE001 - keep ingesting other files
            print(f"Warning: skipped {path}: {exc}", file=sys.stderr)
    return documents
