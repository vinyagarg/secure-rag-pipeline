<h1 align="center">🛡️ RAGuard</h1>

<p align="center">
  <em><strong>Smart enough to answer. Smart enough to know when not to.</strong></em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white" />
</p>

<p align="center">
  <a href="https://secure-rag-pipeline.vercel.app"><strong>Live Demo</strong></a> &nbsp;·&nbsp;
  <a href="https://raguard-api.onrender.com/docs"><strong>API Docs</strong></a>
</p>

<p align="center">
  Demo login — User: <code>user123</code> &nbsp;·&nbsp; Admin: <code>admin123</code>
</p>

---

## What is RAGuard?

RAGuard is a production-grade **Retrieval-Augmented Generation (RAG)** system that goes beyond basic retrieve-and-generate. Most RAG projects stop there — RAGuard adds security guardrails, automated evaluation, audit logging, and a live observability dashboard, making it trustworthy, not just functional.

---

## Pipeline

```text
User Query
  │
  ├── Input Guardrail    → Pattern-based injection detection
  ├── Input Guardrail    → LLM intent classifier
  ├── Retriever          → ChromaDB vector search (616 chunks)
  ├── Generator          → Llama 3.3 70B, grounded generation
  ├── Output Guardrail   → PII + sensitive data sanitization
  ├── Grounding Check    → LLM-as-judge faithfulness score (1–5)
  └── Audit Logger       → SQLite, every request traced
```

---

## Evaluation Results

> Fully reproducible — run `python eval/run_eval.py` anytime

| Metric | Score |
|:--|:--:|
| 🎯 Retrieval Recall@3 | **100%** (15/15 golden questions) |
| 💬 Answer Relevance | **4.93 / 5** |
| ✅ Answer Faithfulness | **4.67 / 5** |
| 🔁 Consistency (3× runs) | **0.997 / 1.0** |
| 🧪 Guardrail Test Suite | **7 / 7 passing** |

---

## Features

| Capability | Basic RAG | RAGuard |
|:--|:--:|:--:|
| Grounded generation | ✅ | ✅ |
| Refuses out-of-scope questions | ❌ | ✅ |
| Prompt injection defense | ❌ | ✅ |
| Hallucination scoring | ❌ | ✅ |
| Automated eval pipeline | ❌ | ✅ |
| Audit logging + dashboard | ❌ | ✅ |
| Admin / user login system | ❌ | ✅ |

---

## Tech Stack

| Layer | Technology |
|:--|:--|
| Frontend | React · Next.js · Tailwind CSS |
| Backend | FastAPI · Uvicorn |
| Embeddings | Jina AI — `jina-embeddings-v3` |
| Vector Store | ChromaDB |
| LLM | Llama 3.3 70B via Groq API |
| Logging | SQLite |
| Deployment | Render (API) · Vercel (UI) |
| Container | Docker |

---

## Quickstart

```bash
# Clone and install
git clone https://github.com/vinyagarg/secure-rag-pipeline
cd secure-rag-pipeline
pip install -r requirements.txt
cp .env.example .env          # Add GROQ_API_KEY + JINA_API_KEY

# Build index and start API
python retrieval/build_index.py
uvicorn api.main:app --reload

# Frontend (separate terminal)
cd frontend && npm install && npm run dev

# Run eval suite
python eval/run_eval.py

# Run tests
pytest tests/ -v
```

---

<p align="center">
  Made with Python · FastAPI · React · ChromaDB · Llama 3.3 · Docker
</p>

