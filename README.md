# 🎧 Customer Support Agent — JK Data Lab

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Agentic AI](https://img.shields.io/badge/Agentic-AI-00FFD4?style=flat)](https://www.jkdatalab.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Author](https://img.shields.io/badge/Author-Kinjal%20Jayswal-blueviolet?style=flat)](https://www.jkdatalab.com)

> Multi-turn conversational AI agent for customer support with intent detection, sentiment analysis, and human escalation.

---

## What It Does

- Detects **customer intent** (pricing, services, timeline, contact, technology) from free-text messages using keyword matching
- Performs **sentiment analysis** (positive / neutral / negative) on every user message
- **Auto-escalates** to a human agent when negative sentiment is detected (configurable toggle)
- Serves answers from a structured **knowledge base** covering JK Data Lab services, pricing, timelines, and contacts
- Tracks **session statistics** (message count, negative sentiment count) in a live sidebar

---

## Architecture

```
app.py
├── KNOWLEDGE_BASE          — structured facts (pricing, services, timeline, contact, tech)
├── DEMO_RESPONSES          — pre-written markdown replies per intent
├── get_intent(message)     — keyword-based intent classifier
├── get_sentiment(message)  — keyword-based sentiment classifier
└── Streamlit UI
    ├── Sidebar             — agent settings, session stats, new session button
    ├── Chat history        — rendered with custom CSS (user / agent / escalation styles)
    └── chat_input          — processes new messages, triggers rerun
```

---

## Quick Start

### 1. Clone & install

```powershell
# Windows (PowerShell)
cd 05_customer_support_agent
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

```bash
# macOS / Linux
cd 05_customer_support_agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

---

## Configuration

All settings are available in the **sidebar** at runtime — no `.env` file needed for demo mode:

| Setting | Default | Description |
|---------|---------|-------------|
| Demo Mode | On | Use pre-built responses (no external LLM required) |
| Agent Name | Aria | Display name shown in chat |
| Company | JK Data Lab | Company name in greeting |
| Auto-escalate negative sentiment | On | Escalate to human on negative keywords |

---

## Project Structure

```
05_customer_support_agent/
├── app.py              — Streamlit app (UI + intent/sentiment logic + knowledge base)
├── requirements.txt    — Python dependencies
├── README.md           — This file
└── venv/               — Python virtual environment (not committed)
```

---

## Requirements

| Package | Purpose |
|---------|---------|
| `streamlit>=1.35.0` | Web UI framework — chat interface, sidebar, session state |
| `requests>=2.31.0` | HTTP client — for future LLM/API integration |
| `langchain>=0.2.0` | LLM orchestration — for extending beyond demo mode |
| `langchain-community>=0.2.0` | Community integrations — Ollama, HuggingFace, etc. |
| `openai>=1.30.0` | OpenAI API client — for GPT-based response generation |

---

## Extending with a Real LLM

The agent ships in **Demo Mode** (rule-based responses). To connect a live LLM:

**With Ollama (local, free):**
```bash
ollama pull llama3
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```
Then replace `DEMO_RESPONSES.get(intent, ...)` in `app.py` with a LangChain chain calling the Ollama endpoint.

**With OpenAI:**
```bash
export OPENAI_API_KEY=sk-...
```
Use `langchain_openai.ChatOpenAI` to build a retrieval chain over `KNOWLEDGE_BASE`.

---

## Module Series

This is **Module 05** of the JK Data Lab Agentic AI project series:

| # | Module |
|---|--------|
| 01 | Data Ingestion Agent |
| 02 | Data Analysis Agent |
| 03 | Report Generation Agent |
| 04 | Workflow Orchestration Agent |
| **05** | **Customer Support Agent** ← you are here |

---

## License

MIT © [Kinjal Jayswal](https://www.jkdatalab.com)

---

<div align="center">
Built with ❤️ by <strong><a href="https://www.jkdatalab.com">JK Data Lab</a></strong><br>
📧 kinjal@jkdatalab.com &nbsp;|&nbsp; 📱 +91-9157938887 &nbsp;|&nbsp; 🌐 www.jkdatalab.com
</div>
