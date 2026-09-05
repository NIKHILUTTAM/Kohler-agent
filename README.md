# KOHLER Unified Enterprise AI Agent

### KOHLER–MIT WPU AI Research Lab Program | Track 3

> **One enterprise conversation. Multiple knowledge domains. Any output format.**

An AI-powered enterprise knowledge assistant that combines **Retrieval-Augmented Generation (RAG), conversational memory, local LLM inference, semantic search, and dynamic response formatting** to answer organization-specific questions and convert responses into business-ready formats such as JSON, XML, CSV, Email, PDF, Excel, and Word.

---

## 📌 Project Overview

The **KOHLER Unified Enterprise AI Agent** is a functional prototype developed for:

> **Track 3 — KOHLER Unified Enterprise AI Agent**

The objective of this project is to create a conversational AI system capable of answering questions across multiple enterprise knowledge domains while adapting its output according to user requirements.

The system provides a unified conversational interface for domains such as:

* 👥 HR & Employee Policies
* 💰 Finance & Expense Guidelines
* 🎧 Customer Support
* 🔐 Privacy & Data Protection
* 📄 Enterprise Documentation

Instead of manually searching through different documents, users can interact with a single AI assistant using natural language.

The system retrieves relevant information from the knowledge base, provides it as context to the LLM, generates a grounded response, and optionally transforms the response into the format requested by the user.

---

# 🎯 Problem Statement

Enterprise information is often distributed across multiple departments, policies, documents, and knowledge bases.

Employees and business users may need to:

1. Find the correct document.
2. Search for relevant information.
3. Understand the policy.
4. Interpret the information.
5. Convert it into a usable business format.

This process can be time-consuming and may result in inconsistent interpretations.

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

This approach helps improve factual grounding and reduce unsupported responses.

---

## 2. Multi-Domain Enterprise Knowledge

The prototype supports multiple enterprise knowledge domains through knowledge-base documents.

Example:

```text
knowledge_base/
├── hr_policy.md
├── finance_guidelines.md
├── customer_support.md
└── privacy_policy.md
```

The architecture can be extended to additional enterprise domains without changing the fundamental conversational workflow.

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
                 │    WORKFLOW      │
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

### Document Processing

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
Semantic Index
```

### Query Processing

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

```text
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

Users can:

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
├── .venv/
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

> **Note:** `.venv/` is a local development environment and should **not** be committed to GitHub.

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

# ⚙️ Installation & Setup

## 1. Create a Python Virtual Environment

Open **PowerShell** in the project directory:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

After activation, the terminal should show:

```text
(.venv)
```

---

## 2. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

---

## 3. Install Python Dependencies

Install the core dependencies:

```powershell
python -m pip install streamlit requests langchain langchain-core langchain-ollama langgraph pypdf python-docx
```

Install the document export dependencies:

```powershell
python -m pip install openpyxl reportlab
```

### Main Dependencies

| Package            | Purpose                   |
| ------------------ | ------------------------- |
| `streamlit`        | Web-based user interface  |
| `requests`         | HTTP/API communication    |
| `langchain`        | LLM application framework |
| `langchain-core`   | LangChain core components |
| `langchain-ollama` | Ollama model integration  |
| `langgraph`        | AI workflow orchestration |
| `pypdf`            | PDF document processing   |
| `python-docx`      | DOCX document processing  |
| `openpyxl`         | Excel generation          |
| `reportlab`        | PDF generation            |

---

# 🤖 Ollama Installation

The project uses **Ollama** to run the LLM locally.

### Windows Installer

Download and install Ollama:

https://ollama.com/download/OllamaSetup.exe

After installation, verify Ollama:

```powershell
ollama --version
```

Check the Ollama service:

```powershell
ollama status
```

---

# 🧠 Required AI Models

The default configuration uses:

```text
Chat Model:
qwen2.5:3b

Embedding Model:
nomic-embed-text
```

If the models are not already installed, run:

```powershell
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
```

Verify installed models:

```powershell
ollama list
```

---

# 🧪 Run the Self-Test

Before launching the application, run the built-in core self-test:

```powershell
python kohler_agent_core.py --self-test
```

A successful test should report:

```text
CORE SELF-TEST PASSED
```

The self-test validates important functionality including:

* Text chunking
* JSON extraction
* Email-format detection
* Conversation-reference handling
* XML generation
* Multi-format export

---

# ▶️ Run the Application

Launch the Streamlit application:

```powershell
streamlit run kohler_unified_agent_app.py
```

If the `streamlit` command is not recognized, use:

```powershell
python -m streamlit run kohler_unified_agent_app.py
```

Streamlit will provide a local URL, normally:

```text
http://localhost:8501
```

Open the URL in your browser to access the **KOHLER Unified Enterprise AI Agent**.

---

# 🚀 Quick Start

For a fresh Windows setup:

```powershell
python -m venv .venv

.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

python -m pip install streamlit requests langchain langchain-core langchain-ollama langgraph pypdf python-docx openpyxl reportlab
```

Install and verify Ollama:

```powershell
ollama --version
ollama status
ollama list
```

Install the required models if necessary:

```powershell
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
```

Run the self-test:

```powershell
python kohler_agent_core.py --self-test
```

Start the application:

```powershell
streamlit run kohler_unified_agent_app.py
```

---

# 🛠️ Troubleshooting

## PowerShell Execution Policy Error

If PowerShell blocks:

```powershell
.venv\Scripts\Activate.ps1
```

run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again:

```powershell
.venv\Scripts\Activate.ps1
```

---

## Ollama Is Not Running

Check:

```powershell
ollama status
```

If Ollama is not running, start the Ollama application and retry.

Then verify:

```powershell
ollama list
```

---

## Model Not Found

If the application reports that a model is unavailable:

```powershell
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
```

Then verify:

```powershell
ollama list
```

---

## Streamlit Command Not Found

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Then run:

```powershell
python -m streamlit run kohler_unified_agent_app.py
```

---

# 🔧 Configuration

The application supports environment-based configuration.

Example:

```powershell
$env:KOHLER_CHAT_MODEL="qwen2.5:3b"
$env:KOHLER_EMBED_MODEL="nomic-embed-text"
$env:OLLAMA_BASE_URL="http://127.0.0.1:11434"
$env:KOHLER_TOP_K="5"
$env:KOHLER_KNOWLEDGE_DIR="./knowledge_base"
$env:KOHLER_MEMORY_FILE="./conversation_memory.json"
```

This allows the application to be configured without modifying the source code.

---

# 💡 Example Queries

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

---

# 🔄 Multi-Turn Example

```text
User:
What are the reimbursement requirements?

AI:
[Grounded response]

User:
Summarize this in three bullet points.

AI:
[Summary]

User:
Convert this into JSON.

AI:
[Structured JSON]

User:
Now draft an email based on it.

AI:
[Ready-to-send email]
```

This demonstrates:

```text
Retrieval
   ↓
Reasoning
   ↓
Conversation Memory
   ↓
Context Resolution
   ↓
Output Transformation
```

---

# 🏢 Enterprise Use Cases

## Employee Self-Service

Employees can quickly access HR policies and internal procedures through natural language.

## Finance Operations

Employees can retrieve reimbursement and finance guidelines without manually searching multiple documents.

## Customer Support

Support teams can retrieve escalation procedures and generate standardized responses.

## Privacy Operations

Employees can retrieve approved privacy procedures and identify appropriate escalation paths.

## Enterprise Knowledge Search

Organizations can provide conversational access to distributed documentation through one interface.

---

# 🔐 Security & Trust Considerations

The prototype follows a local-first approach.

### Local Model Inference

The default setup uses Ollama for local LLM inference.

### Knowledge Grounding

Enterprise responses are based on retrieved knowledge-base context.

### Source Awareness

Source filenames are preserved during retrieval.

### Prompt Injection Awareness

Retrieved documents are treated as information/data rather than higher-priority system instructions.

### Memory Control

Conversation memory is bounded to prevent unlimited context growth.

### Secrets

No API keys, passwords, credentials, or other secrets should be committed to the repository.

---

# ⚠️ Prototype Disclaimer

The documents included in the demonstration knowledge base are:

> **Synthetic demonstration content and NOT official KOHLER policies, procedures, legal documents, financial guidelines, or customer-support documentation.**

For production deployment, these documents would be replaced with authorized and version-controlled enterprise sources.

This prototype should not be used to make real legal, financial, HR, privacy, or compliance decisions.

---

# 📊 KOHLER Evaluation Alignment

The project is designed around the four evaluation dimensions specified in the KOHLER–MIT WPU challenge.

| Evaluation Criterion                 |  Weight | Project Alignment                                                                |
| ------------------------------------ | ------: | -------------------------------------------------------------------------------- |
| **Approach & Innovation**            | **45%** | RAG, local AI, multi-turn reasoning, dynamic formatting, source grounding        |
| **Technical Execution**              | **25%** | LangGraph, Ollama, semantic retrieval, document ingestion, exports, self-tests   |
| **User Experience & Feasibility**    | **20%** | Streamlit UI, conversational workflow, document uploads, downloads               |
| **Business & Sustainability Impact** | **10%** | Enterprise knowledge accessibility, operational efficiency, standardized outputs |

---

# 💎 Innovation Highlights

## 1. Unified Enterprise Knowledge

One conversational interface across multiple enterprise domains.

## 2. Local-First RAG

The prototype can perform LLM inference locally through Ollama.

## 3. Context-Aware Conversations

The system maintains conversational context and resolves references to previous responses.

## 4. Dynamic Output Generation

The same knowledge can be transformed into different formats:

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

Generated results can be exported as:

```text
PDF
Excel
Word
JSON
XML
CSV
HTML
ZIP
```

## 6. Grounded Responses

The system prioritizes retrieved enterprise evidence and discourages unsupported claims.

## 7. Human Escalation

When sufficient information is unavailable, the system is designed to avoid guessing and recommend appropriate human/team review.

---

# 🔮 Future Enhancements

The current prototype provides a foundation for a production-grade enterprise AI platform.

Potential improvements include:

### Hybrid Search

Combine:

```text
Semantic Search + Keyword Search
```

to improve retrieval precision.

### Reranking

Introduce a dedicated reranking stage after initial retrieval.

### Persistent Vector Database

Replace the current in-memory retrieval index with a persistent vector database.

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

for enterprise auditing and traceability.

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

For the required **1–3 minute demonstration video**, the following sequence demonstrates the strongest capabilities.

### Step 1 — Introduce the Agent

Show:

```text
KOHLER Unified Enterprise AI Agent
Track 3
```

### Step 2 — Ask an Enterprise Question

Example:

```text
What information is required for an expense claim?
```

Show the grounded response and source.

### Step 3 — Demonstrate Multi-Turn Context

Ask:

```text
Summarize that in three points.
```

### Step 4 — Demonstrate Dynamic Formatting

Ask:

```text
Convert this into JSON.
```

Then:

```text
Draft an email based on this.
```

### Step 5 — Demonstrate Export

Show:

```text
Download → PDF / Excel / JSON / Word
```

### Step 6 — Demonstrate Knowledge Ingestion

Upload an additional document and rebuild the knowledge index.

### Step 7 — Show the Architecture

Finish with:

```text
User
 ↓
Semantic Retrieval
 ↓
RAG Context
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
* [ ] `.venv/` excluded from Git
* [ ] Repository can be cloned and executed by an evaluator
* [ ] Self-test passes successfully

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

**Evaluation:**

```text
Approach & Innovation       45%
Technical Execution         25%
User Experience             20%
Business & Sustainability   10%
```

**Core Technology:**

```text
RAG
+
Semantic Retrieval
+
LangGraph
+
Ollama
+
Local LLM
+
Conversation Memory
+
Dynamic Output Formatting
+
Enterprise Exports
```

**Core Pitch:**

> **One enterprise conversation, multiple knowledge domains, and any output format — powered by grounded local AI.**
