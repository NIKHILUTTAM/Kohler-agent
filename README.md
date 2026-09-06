# KOHLER Unified Enterprise AI Agent

**Track 3 — KOHLER-MITWPU AI Research Lab Program**

An enterprise-grade conversational AI agent that answers questions across HR,
finance, customer support, and privacy knowledge domains, with **multi-turn
follow-up resolution** ("draft the mail for this") and **on-demand output
formatting** (Markdown, JSON, XML, CSV, email, or downloadable Word / Excel /
PDF). Runs **entirely locally** via [Ollama](https://ollama.com) — no data
leaves the machine, no API keys required.

---

## 1. Architecture

```
                 ┌────────────────────────────────────────┐
                 │              Streamlit UI               │
                 │  (kohler_agent/app.py)                   │
                 └───────────────┬──────────────────────────┘
                                 │ graph.invoke(question, history, format)
                                 ▼
        ┌─────────────────────────────────────────────────────┐
        │                LangGraph pipeline                     │
        │        (kohler_agent/graph.py)                        │
        │                                                         │
        │   retrieve ──▶ reason ──▶ format                       │
        └───────┬────────────┬────────────┬──────────────────────┘
                │            │            │
                ▼            ▼            ▼
      ┌──────────────┐ ┌────────────┐ ┌────────────────┐
      │ retrieval.py │ │   llm.py   │ │ formatting.py    │
      │ (cosine-sim  │ │ (Ollama    │ │ (JSON/XML/CSV/    │
      │  vector      │ │  lifecycle │ │  email rendering) │
      │  search)     │ │  + models) │ └────────────────┘
      └──────┬───────┘ └────────────┘
             │
             ▼
      ┌──────────────┐        ┌───────────────┐
      │ ingestion.py │        │  memory.py     │
      │ (load/chunk  │        │ (conversation  │
      │  documents)  │        │  persistence)  │
      └──────────────┘        └───────────────┘

      exporters.py -> turns the final answer into .txt/.md/.json/.xml/.csv/
                       .html/.docx/.xlsx/.pdf, plus a bundled .zip
```

**Pipeline nodes**

1. **retrieve** — embeds the question (+ recent turns) with a local
   embedding model, ranks knowledge-base chunks by cosine similarity, and
   keeps only chunks above a relevance threshold (grounding — the agent
   never fabricates a policy it can't cite).
2. **reason** — the local chat model answers strictly from retrieved
   context, resolves follow-ups ("this", "that", "the previous answer")
   using the last turn, and is instructed on the requested output format.
3. **format** — deterministically post-processes the model's draft into
   valid JSON / XML / CSV / a ready-to-send email, so formatting never
   depends on the LLM getting syntax exactly right.

## 2. Project layout

```
kohler-unified-agent/
├── run_app.py              # `streamlit run run_app.py` entry point
├── run_self_test.py        # fast, no-Ollama-required sanity check
├── requirements.txt
├── pyproject.toml
├── src/kohler_agent/
│   ├── __init__.py         # public API re-exports
│   ├── config.py           # every env-driven constant, in one place
│   ├── demo_content.py     # synthetic seed documents (HR/finance/etc.)
│   ├── ingestion.py        # file loading, text extraction, chunking
│   ├── retrieval.py        # SemanticIndex (embeddings + cosine search)
│   ├── llm.py               # start Ollama, pull models, HTTP helpers
│   ├── memory.py            # conversation persistence + reference context
│   ├── formatting.py        # format detection + JSON/XML/CSV/email rendering
│   ├── graph.py              # LangGraph state + retrieve/reason/format nodes
│   ├── exporters.py          # txt/md/json/xml/csv/html/docx/xlsx/pdf/zip export
│   ├── app.py                 # Streamlit UI (chat, sidebar, downloads)
│   └── run_self_test.py       # the actual assertions run_self_test.py calls
├── tests/test_core.py       # pytest suite (11 tests, same coverage as above)
├── knowledge_base/          # your documents go here (seeded with demo docs)
└── docs/                    # prompts documentation / deck / demo video go here
```

Every module has one job, and the LLM-dependent code (`llm.py`, `graph.py`'s
`build_graph`) is isolated from the pure-logic code (`formatting.py`,
`ingestion.py`'s `split_text`, `exporters.py`) so the latter can be tested
instantly without Ollama installed.

## 3. Setup

**Prerequisites:** Python 3.10+, and [Ollama](https://ollama.com) installed
(the app will start it and pull models automatically on first run if it's on
your PATH — model downloads need internet access once).

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Run it

```bash
streamlit run run_app.py
```

The first launch will:
1. Start `ollama serve` if it isn't already running.
2. Pull `qwen2.5:3b` (chat) and `nomic-embed-text` (embeddings) — override
   with `KOHLER_CHAT_MODEL` / `KOHLER_EMBED_MODEL` env vars for a
   larger/smaller model.
3. Seed `knowledge_base/` with four demo policy documents (HR, finance,
   customer support, privacy) if it's empty.
4. Index everything and open the chat UI, where you can:
   - Ask a question and pick a response format from the sidebar.
   - Type "as JSON" / "draft the email for this" to override the format
     inline, without touching the sidebar.
   - Upload your own `.txt/.md/.csv/.json/.yaml/.pdf/.docx` documents.
   - Download any answer as TXT/MD/JSON/XML/CSV/HTML/DOCX/XLSX/PDF, or all
     of them zipped together.

## 5. Test it

```bash
# Fast — no Ollama or network required, checks chunking/format/export logic
python run_self_test.py

# Full pytest suite (11 tests)
pytest -q
```

Both are green on a clean checkout with only `requirements.txt` installed —
they deliberately don't touch `graph.py`'s `build_graph()` (the only
function that needs a running local model), so CI/graders can verify the
core logic without installing Ollama.

## 6. Configuration reference

All of these are optional; sensible defaults are set in `config.py`.

| Env var                    | Default                   | Purpose                          |
|-----------------------------|----------------------------|-----------------------------------|
| `KOHLER_KNOWLEDGE_DIR`      | `./knowledge_base`         | Where source documents live       |
| `KOHLER_MEMORY_FILE`        | `./conversation_memory.json` | Where chat history persists     |
| `OLLAMA_BASE_URL`           | `http://127.0.0.1:11434`   | Local Ollama server               |
| `KOHLER_CHAT_MODEL`         | `qwen2.5:3b`                | Local chat model                  |
| `KOHLER_EMBED_MODEL`        | `nomic-embed-text`         | Local embedding model             |
| `KOHLER_TOP_K`               | `5`                        | Chunks retrieved per question     |
| `KOHLER_MIN_RELEVANCE`      | `0.20`                     | Cosine-similarity cutoff          |
| `KOHLER_CHUNK_SIZE` / `KOHLER_CHUNK_OVERLAP` | `1400` / `220` | Document chunking       |

## 7. Design notes / why these choices

- **Local-first**: everything runs on Ollama, so no HR/finance/legal
  document ever leaves the machine — a hard requirement for the domains in
  this track.
- **Grounded answers**: the system prompt forbids inventing policy details,
  and the retrieval node explicitly flags `NO_RELIABLE_SOURCE_MATCH` when
  nothing relevant is found, so the model is told to say so rather than guess.
  Prompt-injection risk is mitigated by instructing the model to treat
  retrieved document content as data, never as instructions.
- **Deterministic formatting layer**: rather than trusting the LLM to emit
  perfect JSON/XML, `formatting.py` parses/repairs the draft and
  guarantees valid output — this is what makes "adaptive agent... formats
  responses on demand" reliable rather than best-effort.
- **No vector database dependency**: a small, dependency-light in-memory
  cosine index (`retrieval.py`) is enough at this document scale and keeps
  the two-file-turned-package prototype easy to read end-to-end; swapping in
  FAISS/Chroma later only touches this one file.

## 8. Submission checklist (for this repo)

- [x] Working model — source + run instructions (this repo)
- [x] Prompts Documentation (PDF) — see `docs/`
- [ ] Video demo (1–3 min) — link or file in `docs/`
- [x] Presentation deck (max 4 slides, PDF) — see `docs/`
