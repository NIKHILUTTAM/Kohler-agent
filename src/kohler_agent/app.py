"""Streamlit UI for the KOHLER Unified Enterprise AI Agent (Track 3).

Run with:
    streamlit run run_app.py
or:
    python -m kohler_agent.app
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from . import config
from .exporters import EXPORT_LABELS, export_response_files
from .formatting import infer_requested_format
from .graph import build_graph
from .memory import clear_conversation_memory, load_conversation_memory, save_conversation_memory
from .run_self_test import run_self_test


def render_downloads(
    st: Any, answer: str, response_format: str, sources: list[str], key_prefix: str
) -> None:
    try:
        files = export_response_files(answer, response_format, sources)
    except Exception as exc:  # noqa: BLE001 - surface the error to the user
        st.warning(f"Export generation failed: {exc}")
        return

    with st.expander("Download this response"):
        columns = st.columns(5)
        for index, extension in enumerate(EXPORT_LABELS):
            data, filename, mime = files[extension]
            with columns[index % 5]:
                st.download_button(
                    label=EXPORT_LABELS[extension],
                    data=data,
                    file_name=filename,
                    mime=mime,
                    key=f"{key_prefix}_{extension}",
                    use_container_width=True,
                )


def render_sidebar(st: Any) -> str:
    with st.sidebar:
        st.header("Controls")
        requested_format = st.selectbox(
            "Response format", ["markdown", "json", "xml", "csv", "email"], index=0
        )
        st.write(f"Chat model: `{config.CHAT_MODEL}`")
        st.write(f"Embedding model: `{config.EMBED_MODEL}`")
        st.write(f"Knowledge base: `{config.KNOWLEDGE_DIR}`")
        uploaded = st.file_uploader(
            "Add a knowledge document",
            type=["txt", "md", "csv", "json", "yaml", "yml", "pdf", "docx"],
        )
        if uploaded is not None:
            signature = f"{uploaded.name}:{uploaded.size}"
            if st.session_state.get("last_upload_signature") != signature:
                config.KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
                destination = config.KNOWLEDGE_DIR / Path(uploaded.name).name
                destination.write_bytes(uploaded.getvalue())
                st.session_state.last_upload_signature = signature
                st.cache_resource.clear()
                st.success(f"Saved {destination.name}. Rebuild the index to use it.")
        if st.button("Rebuild knowledge index"):
            st.cache_resource.clear()
            st.rerun()
        if st.button("Clear conversation memory"):
            st.session_state.kohler_messages = []
            clear_conversation_memory()
            st.rerun()
        st.caption("Conversation memory is stored locally in conversation_memory.json.")
    return requested_format


def run_streamlit() -> None:
    import streamlit as st

    st.set_page_config(page_title=config.APP_TITLE, page_icon="\U0001f6bf", layout="wide")
    st.title(config.APP_TITLE)
    st.caption("Local-first RAG + LangGraph workflow for Track 3")

    if "kohler_messages" not in st.session_state:
        st.session_state.kohler_messages = load_conversation_memory()

    requested_format = render_sidebar(st)

    @st.cache_resource(
        show_spinner="Starting Ollama, downloading models if needed, and indexing documents..."
    )
    def cached_runtime() -> tuple[Any, dict[str, Any]]:
        return build_graph()

    try:
        graph, stats = cached_runtime()
        with st.sidebar:
            st.divider()
            st.metric("Indexed chunks", stats["documents"])
            st.caption("Sources: " + (", ".join(stats["sources"]) or "none"))
    except Exception as exc:  # noqa: BLE001 - show a friendly setup message
        st.error(str(exc))
        st.info(
            "Install the Python dependencies and Ollama runtime, then restart "
            "the app. The first run downloads the two local models automatically."
        )
        return

    for message_index, message in enumerate(st.session_state.kohler_messages):
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and message.get("format") in {"json", "xml", "csv"}:
                st.code(message["content"], language=message["format"])
            else:
                st.markdown(message["content"])
            if message["role"] == "assistant" and message_index == len(
                st.session_state.kohler_messages
            ) - 1:
                render_downloads(
                    st,
                    message["content"],
                    message.get("format", "markdown"),
                    message.get("sources", []),
                    f"history_{message_index}",
                )

    question = st.chat_input("Ask about an HR, finance, privacy, or customer-support policy...")
    if question:
        effective_format = infer_requested_format(question, requested_format)
        st.session_state.kohler_messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Retrieving evidence and reasoning locally..."):
                result = graph.invoke(
                    {
                        "question": question,
                        "requested_format": effective_format,
                        "history": st.session_state.kohler_messages[:-1],
                    }
                )
            answer = result.get("answer", "No answer returned.")
            if effective_format in {"json", "xml", "csv"}:
                st.code(answer, language=effective_format)
            else:
                st.markdown(answer)
            st.session_state.kohler_messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "format": effective_format,
                    "sources": result.get("sources", []),
                }
            )
            save_conversation_memory(st.session_state.kohler_messages)
            render_downloads(
                st,
                answer,
                effective_format,
                result.get("sources", []),
                f"current_{len(st.session_state.kohler_messages)}",
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="KOHLER Unified Enterprise AI Agent")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run the core and export tests without starting Streamlit.",
    )
    args = parser.parse_args()
    if args.self_test:
        run_self_test()
    else:
        run_streamlit()


if __name__ == "__main__":
    main()
