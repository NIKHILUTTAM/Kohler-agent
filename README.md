# KOHLER Unified Enterprise AI Agent

### KOHLER–MIT WPU AI Research Lab Program | Track 3

> **One enterprise conversation. Multiple knowledge domains. Any output format.**

An AI-powered enterprise knowledge assistant that combines **Retrieval-Augmented Generation (RAG), conversational memory, local LLM inference, semantic search, and dynamic response formatting** to answer organization-specific questions and convert responses into business-ready formats such as JSON, XML, CSV, Email, PDF, Excel, and Word.

---

## 📌 Project Overview

The **KOHLER Unified Enterprise AI Agent** is a prototype designed for **Track 3: KOHLER Unified Enterprise AI Agent**.

The objective is to create an enterprise-grade conversational AI system capable of answering questions across multiple organizational knowledge domains while adapting its output according to user requirements.

The system provides a unified conversational interface for domains such as:

* 👥 HR & Employee Policies
* 💰 Finance & Expense Guidelines
* 🎧 Customer Support
* 🔐 Privacy & Data Protection
* 📄 Enterprise Documentation

Instead of manually searching through different documents, users can interact with a single AI assistant using natural language.

The system retrieves relevant information from the enterprise knowledge base, provides it as context to the LLM, generates a grounded response, and optionally transforms the response into the format requested by the user.

---

# 🎯 Problem Statement

Enterprise information is often distributed across multiple departments, documents, policies, and knowledge bases.

Employees may need to:

1. Find the correct document.
2. Search for relevant information.
3. Understand the policy.
4. Interpret the information.
5. Convert it into a usable business format.

This process is time-consuming and can lead to inconsistent interpretations.

### Proposed Solution

The KOHLER Unified Enterprise AI Agent provides a single conversational interface over enterprise knowledge.

```text
User Question
      ↓
Conversation Context
      ↓
Semantic Retrieval
      ↓
Relevant Knowledge
      ↓
LLM Reasoning
      ↓
Grounded Response
      ↓
Requested Output Format
```

---

# 🚀 Key Features

## 1. Retrieval-Augmented Generation (RAG)

The system does not rely solely on the LLM's internal knowledge.

It first retrieves relevant information from the local knowledge base and uses that information as context for generation.

```text
Knowledge Documents
        ↓
Text Extraction
        ↓
Chunking
        ↓
Embeddings
        ↓
Semantic Index
        ↓
Query Retrieval
        ↓
Relevant Context
        ↓
LLM
```

This improves factual grounding and reduces unsupported responses.

---

## 2. Multi-Domain Enterprise Knowledge

The prototype supports multiple enterprise knowledge domains through separate knowledge documents.

Example:

```text
knowledge_base/
├── hr_policy.md
├── finance_guidelines.md
├── customer_support.md
└── privacy_policy.md
```

The architecture can be extended to additional enterprise domains without changing the core conversational workflow.

---

## 3. Multi-Turn Conversational Memory

The agent maintains recent conversation history to understand follow-up questions.

For example:

```text
User:
What information is required for an expense claim?

AI:
[Answer]

User:
Summarize that in three points.

AI:
[Summary]

User:
Convert this into JSON.

AI:
[JSON response]
```

The system can resolve contextual references such as:

* this
* that
* it
* previous answer
* above
* earlier
* same

This enables conversational transformations without requiring the user to repeat the original question.

---

# 🧠 AI Architecture

The core workflow is implemented using **LangGraph**.

```text
                 ┌──────────────────┐
                 │       USER       │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   STREAMLIT UI   │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │    LANGGRAPH     │
                 │   WORKFLOW       │
                 └────────┬─────────┘
                          │
                 ┌────────┴────────┐
                 │                 │
                 ▼                 ▼
          ┌──────────────┐  ┌───────────────┐
          │   RETRIEVE   │  │  CONVERSATION │
          │              │  │    MEMORY     │
          └──────┬───────┘  └───────┬───────┘
                 │                  │
                 └────────┬─────────┘
                          ▼
                 ┌──────────────────┐
                 │      REASON      │
                 │   Local LLM      │
                 │   + RAG Context  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │      FORMAT      │
                 └────────┬─────────┘
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
         Markdown        JSON          XML
            │             │             │
            ├─────────────┼─────────────┤
            ▼             ▼             ▼
           CSV          Email       Downloads
```

---

# 🔍 Retrieval Pipeline

The retrieval system uses embedding-based semantic similarity.

### Processing

```text
Document
   ↓
Text Extraction
   ↓
Cleaning
   ↓
Chunking
   ↓
Embedding Generation
   ↓
Index
```

For a user query:

```text
User Query
   ↓
Query Embedding
   ↓
Cosine Similarity
   ↓
Top-K Relevant Chunks
   ↓
LLM Context
```

### Current Retrieval Configuration

| Parameter            |           Value |
| -------------------- | --------------: |
| Top-K Results        |               5 |
| Similarity Threshold |            0.20 |
| Chunk Size           | 1400 characters |
| Chunk Overlap        |  220 characters |

---

# 📚 Supported Documents

The knowledge ingestion pipeline supports:

| Format   | Supported |
| -------- | --------- |
| TXT      | ✅         |
| Markdown | ✅         |
| CSV      | ✅         |
| JSON     | ✅         |
| YAML     | ✅         |
| PDF      | ✅         |
| DOCX     | ✅         |

Documents can be added through the application interface and indexed for retrieval.

---

# 🤖 Local AI Models

The prototype uses **Ollama** for local model serving.

### Default Chat Model

```text
qwen2.5:3b
```

### Default Embedding Model

```text
nomic-embed-text
```

The models can be changed using environment variables.

```bash
KOHLER_CHAT_MODEL
KOHLER_EMBED_MODEL
OLLAMA_BASE_URL
```

---

# 🛡️ Grounded AI & Hallucination Control

Enterprise AI systems should not confidently invent organizational policies.

The system therefore instructs the LLM to:

* Use retrieved knowledge as the primary factual source.
* Avoid inventing policies.
* Avoid inventing deadlines or numerical requirements.
* Avoid unsupported legal conclusions.
* Clearly communicate when sufficient information is unavailable.
* Recommend human/team escalation where appropriate.
* Treat retrieved document content as data rather than system instructions.
* Preserve source information for grounded responses.

### Intended behavior

```text
Relevant Evidence Found
        ↓
Grounded Answer
        ↓
Source Attribution
```

If sufficient evidence is not available:

```text
Insufficient Evidence
        ↓
Do Not Guess
        ↓
Explain Limitation
        ↓
Recommend Escalation
```

---

# 🔄 Dynamic Output Formatting

One of the primary capabilities of the system is the ability to transform conversational responses into different output formats.

Supported formats include:

* Markdown
* JSON
* XML
* CSV
* Email

### Example

```text
User:
What does the finance policy require?

        ↓

AI:
Provides a grounded answer.

        ↓

User:
Convert this into JSON.

        ↓

AI:
Returns structured JSON.

        ↓

User:
Draft an email based on this.

        ↓

AI:
Returns a ready-to-send email.
```

This transforms the assistant from a simple Q&A chatbot into a **knowledge-to-action interface**.

---

# 📤 Export Capabilities

Generated responses can be exported into business-friendly formats.

| Output           | Extension |
| ---------------- | --------- |
| Text             | `.txt`    |
| Markdown         | `.md`     |
| JSON             | `.json`   |
| XML              | `.xml`    |
| CSV              | `.csv`    |
| HTML             | `.html`   |
| Word             | `.docx`   |
| Excel            | `.xlsx`   |
| PDF              | `.pdf`    |
| Complete Package | `.zip`    |

---

# 🖥️ User Interface

The application is built using **Streamlit**.

### Main Interface

The user can:

* Ask natural-language questions.
* Continue multi-turn conversations.
* Select an output format.
* View generated responses.
* Download generated outputs.

### Sidebar

The interface provides controls for:

* Chat model configuration
* Embedding model information
* Knowledge-base management
* Document upload
* Knowledge-index rebuilding
* Conversation-memory management

---

# 📥 Knowledge Upload

Users can upload enterprise documents directly through the interface.

```text
Upload Document
       ↓
Save Document
       ↓
Rebuild Knowledge Index
       ↓
Generate Embeddings
       ↓
Document Available for Retrieval
```

This demonstrates how the prototype can adapt to changing organizational knowledge.

---

# 🗂️ Project Structure

```text
kohler-unified-enterprise-ai-agent/
│
├── kohler_agent_core.py
├── kohler_unified_agent_app.py
├── requirements.txt
├── README.md
│
├── knowledge_base/
│   ├── hr_policy.md
│   ├── finance_guidelines.md
│   ├── customer_support.md
│   └── privacy_policy.md
│
├── conversation_memory.json
│
├── prompts/
│   └── KOHLER_Prompts_Documentation.pdf
│
├── presentation/
│   └── KOHLER_Track3_Presentation.pdf
│
└── demo/
    └── VIDEO_LINK.md
```

---

# 🧩 Core Files

## `kohler_agent_core.py`

Contains the main AI functionality:

* Document ingestion
* Text extraction
* Text chunking
* Embedding generation
* Semantic retrieval
* RAG context construction
* Ollama integration
* LangGraph workflow
* Conversation memory
* Response formatting
* Export generation
* Self-tests

---

## `kohler_unified_agent_app.py`

Contains the Streamlit application:

* Chat interface
* Output-format selection
* File upload
* Knowledge-base management
* Index rebuilding
* Conversation-memory controls
* Response rendering
* Download functionality

---

# ⚙️ Configuration

The application supports environment-based configuration.

Example:

```bash
export KOHLER_CHAT_MODEL="qwen2.5:3b"
export KOHLER_EMBED_MODEL="nomic-embed-text"
export OLLAMA_BASE_URL="http://127.0.0.1:11434"
export KOHLER_TOP_K="5"
export KOHLER_KNOWLEDGE_DIR="./knowledge_base"
export KOHLER_MEMORY_FILE="./conversation_memory.json"
```

---

# 💻 Installation

## Prerequisites

Install:

* Python 3.10+
* Ollama

Then install Python dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Application

Start the application using:

```bash
streamlit run kohler_unified_agent_app.py
```

The application will load the knowledge base and initialize the retrieval pipeline.

---

# 🧪 Self-Test

The project includes a built-in self-test.

Run:

```bash
python kohler_unified_agent_app.py --self-test
```

Expected output:

```text
CORE SELF-TEST PASSED
```

The self-test validates important components including:

* Text chunking
* JSON extraction
* Email-format detection
* Conversation-reference handling
* XML generation
* Multi-format export

---

# 💡 Example Use Cases

## HR

```text
What does the HR policy say about flexible work?
```

## Finance

```text
What information is required for an expense claim?
```

## Customer Support

```text
When should a customer issue be escalated?
```

## Privacy

```text
How should a personal-data deletion request be handled?
```

## Conversational Transformation

```text
User:
What are the reimbursement requirements?

User:
Summarize this.

User:
Convert this into JSON.

User:
Now draft an email based on it.
```

---

# 🏢 Enterprise Use Cases

The architecture can support:

### Employee Self-Service

Quick access to HR policies and internal procedures.

### Finance Operations

Faster understanding of reimbursement and finance guidelines.

### Customer Support

Rapid access to escalation procedures and standardized response generation.

### Privacy Operations

Retrieval of approved privacy procedures and escalation guidance.

### Enterprise Knowledge Search

Unified conversational access to organizational documentation.

---

# 🔐 Security Considerations

The prototype follows a local-first approach.

### Local Model Inference

The default setup uses Ollama for local LLM inference.

### Knowledge Grounding

Enterprise responses are based on retrieved knowledge rather than unrestricted model generation.

### Source Awareness

Source filenames are preserved during retrieval.

### Prompt Injection Awareness

Retrieved documents are treated as information/data and not as higher-priority system instructions.

### Memory Control

Conversation memory is bounded to prevent unlimited context growth.

### Secrets

No API keys or credentials should be committed to the repository.

---

# ⚠️ Prototype Disclaimer

The documents included in the demonstration knowledge base are **synthetic demonstration content**.

They are:

> **NOT official KOHLER policies, procedures, legal documents, financial guidelines, or customer-support documentation.**

For production deployment, these documents would be replaced by authorized and version-controlled enterprise sources.

The prototype should not be used to make real legal, financial, HR, privacy, or compliance decisions.

---

# 📊 KOHLER Evaluation Alignment

The project is designed around the four evaluation dimensions specified for the challenge.

| Evaluation Criterion             |  Weight | Project Alignment                                                                |
| -------------------------------- | ------: | -------------------------------------------------------------------------------- |
| Approach & Innovation            | **45%** | RAG, local AI, multi-turn reasoning, dynamic formatting, source grounding        |
| Technical Execution              | **25%** | LangGraph, Ollama, semantic retrieval, document ingestion, exports, self-tests   |
| User Experience & Feasibility    | **20%** | Streamlit UI, conversational workflow, uploads, downloads                        |
| Business & Sustainability Impact | **10%** | Enterprise knowledge accessibility, operational efficiency, standardized outputs |

---

# 💎 Innovation Highlights

## 1. Unified Enterprise Knowledge

One interface across multiple enterprise domains.

## 2. Local-First RAG

The prototype can perform LLM inference locally through Ollama.

## 3. Context-Aware Conversations

The system maintains conversational context and resolves references to previous responses.

## 4. Dynamic Output Generation

The user can transform the same knowledge into different formats:

```text
Natural Language
      ↓
Markdown
      ↓
JSON
      ↓
XML
      ↓
CSV
      ↓
Email
```

## 5. Enterprise Export Layer

The generated result can become:

```text
PDF
Excel
Word
JSON
XML
CSV
HTML
```

## 6. Grounded Responses

The system prioritizes retrieved enterprise evidence and discourages unsupported claims.

## 7. Human Escalation

When information is insufficient, the system is designed to avoid guessing and direct the user toward appropriate human/team review.

---

# 🔮 Future Enhancements

The current prototype provides the foundation for a production-grade enterprise AI platform.

Potential improvements include:

### Hybrid Search

Combine:

```text
Semantic Search + Keyword Search
```

for improved retrieval precision.

### Reranking

Introduce a dedicated reranker after initial retrieval.

### Persistent Vector Database

Replace the in-memory index with a persistent vector database.

### Domain Routing

Automatically classify requests into:

```text
HR
Finance
Customer Support
Privacy
Legal / Compliance
```

### Enterprise Authentication

Add:

* SSO
* RBAC
* User identity
* Department-level access controls

### Auditability

Store:

```text
User Query
     ↓
Retrieved Sources
     ↓
Generated Response
     ↓
Output Format
```

for enterprise auditing.

### RAG Evaluation

Introduce automated evaluation for:

* Retrieval precision
* Context relevance
* Answer groundedness
* Answer correctness
* Hallucination rate

### Enterprise Integrations

Future versions could integrate with:

* Document Management Systems
* HR systems
* CRM platforms
* Ticketing systems
* Enterprise databases
* Internal APIs

---

# 🎥 Recommended Demo Flow

For the 1–3 minute demonstration video:

### 1. Introduce the Agent

Show:

```text
KOHLER Unified Enterprise AI Agent
Track 3
```

### 2. Ask an Enterprise Question

Example:

```text
What information is required for an expense claim?
```

Show the grounded response.

### 3. Demonstrate Multi-Turn Context

Ask:

```text
Summarize that in three points.
```

### 4. Demonstrate Dynamic Formatting

Ask:

```text
Convert this into JSON.
```

Then:

```text
Draft an email based on this.
```

### 5. Demonstrate Export

Show:

```text
Download → PDF / Excel / JSON / Word
```

### 6. Demonstrate Knowledge Ingestion

Upload a document and rebuild the knowledge index.

### 7. Close With Architecture

Show:

```text
User
 ↓
Retrieval
 ↓
RAG
 ↓
LangGraph
 ↓
Local LLM
 ↓
Dynamic Output
```

---

# 📦 Submission Checklist

Before submitting the GitHub repository:

* [ ] Working model
* [ ] Source code
* [ ] `README.md`
* [ ] `requirements.txt`
* [ ] Knowledge-base documents
* [ ] Prompt documentation PDF
* [ ] 1–3 minute demonstration video
* [ ] Maximum 4-slide presentation PDF
* [ ] Installation instructions
* [ ] Self-test instructions
* [ ] Synthetic-data disclaimer
* [ ] No API keys or secrets
* [ ] Repository can be cloned and executed by an evaluator

---

# 🏁 Final Architecture

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │   STREAMLIT UI  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │    LANGGRAPH    │
                  │   ORCHESTRATOR  │
                  └────────┬────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
      ┌───────────────┐        ┌────────────────┐
      │   SEMANTIC    │        │ CONVERSATION   │
      │   RETRIEVAL   │        │    MEMORY      │
      └───────┬───────┘        └───────┬────────┘
              │                        │
              └────────────┬───────────┘
                           ▼
                  ┌─────────────────┐
                  │     LOCAL LLM   │
                  │     OLLAMA      │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ DYNAMIC FORMAT  │
                  └────────┬────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Markdown        JSON          XML
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                  ┌─────────────────┐
                  │ BUSINESS EXPORT │
                  │ PDF/XLSX/DOCX   │
                  │ CSV/HTML/ZIP    │
                  └─────────────────┘
```

---

# 🎯 Project Pitch

> **KOHLER Unified Enterprise AI Agent transforms fragmented enterprise knowledge into a single conversational interface that can retrieve grounded information, maintain multi-turn context, and convert knowledge into the exact business format required by the user.**

---

## KOHLER–MIT WPU AI Research Lab

**Selected Track:** Track 3 — KOHLER Unified Enterprise AI Agent

**Submission Deadline:** September 20, 2026 — 11:59 PM IST

**Primary Innovation:**
**RAG + Conversational Memory + Local LLM + Dynamic Output Formatting + Enterprise Export**
