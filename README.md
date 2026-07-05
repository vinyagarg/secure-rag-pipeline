\# 🛡️ RAGuard



> \*\*Smart enough to answer. Smart enough to know when not to.\*\*



\[!\[Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square\&logo=python\&logoColor=white)](https://python.org)

\[!\[FastAPI](https://img.shields.io/badge/FastAPI-backend-green?style=flat-square\&logo=fastapi)](https://raguard-api.onrender.com/docs)

\[!\[Next.js](https://img.shields.io/badge/Next.js-frontend-black?style=flat-square\&logo=next.js)](https://secure-rag-pipeline.vercel.app)

\[!\[License](https://img.shields.io/badge/license-MIT-gray?style=flat-square)](LICENSE)



\*\*\[Live Demo](https://secure-rag-pipeline.vercel.app)\*\* \&nbsp;·\&nbsp; \*\*\[API Docs](https://raguard-api.onrender.com/docs)\*\*

<br>

Demo credentials \&nbsp;→\&nbsp; User: `user123` \&nbsp;·\&nbsp; Admin: `admin123`



\---



\## Overview



RAGuard is a production-grade Retrieval-Augmented Generation system that goes beyond basic retrieve-and-generate. It answers questions grounded in real source documents — and when it doesn't know, it says so.



Built with security, evaluation, and observability as core features — not afterthoughts.



\---



\## Architecture



```

Query

&#x20; → Input Guardrail    (pattern matching)

&#x20; → Input Guardrail    (LLM intent classifier)

&#x20; → Retriever          (ChromaDB · 616 chunks)

&#x20; → Generator          (Llama 3.3 70B · grounded)

&#x20; → Output Guardrail   (PII + sanitization)

&#x20; → Grounding Check    (LLM-as-judge · 1–5 score)

&#x20; → Audit Logger       (SQLite · every request traced)

&#x20; → Response

```



\---



\## Evaluation



> All metrics are reproducible — run `python eval/run\_eval.py` anytime.



| Metric | Result |

|---|---|

| Retrieval Recall@3 | \*\*100%\*\* (15/15 golden questions) |

| Answer Relevance | \*\*4.93 / 5\*\* |

| Answer Faithfulness | \*\*4.67 / 5\*\* |

| Consistency across 3 runs | \*\*0.997 / 1.0\*\* |

| Guardrail test suite | \*\*7 / 7 passing\*\* |



\---



\## Stack



| Layer | Technology |

|---|---|

| Frontend | React · Next.js · Vercel |

| Backend | FastAPI · Uvicorn · Render |

| Embeddings | Jina AI (jina-embeddings-v3) |

| Vector Store | ChromaDB |

| LLM | Llama 3.3 70B via Groq API |

| Logging | SQLite audit log |

| Container | Docker |

| Testing | pytest |



\---



\## Quickstart



```bash

git clone https://github.com/vinyagarg/secure-rag-pipeline

cd secure-rag-pipeline

pip install -r requirements.txt

cp .env.example .env                    # Add GROQ\_API\_KEY and JINA\_API\_KEY

python retrieval/build\_index.py         # Build vector index

uvicorn api.main:app --reload           # Start API on :8000

```



```bash

\# Frontend

cd frontend

npm install

npm run dev                             # Start UI on :3000

```



```bash

\# Evaluation

python eval/run\_eval.py                 # Full eval suite + quality gates

pytest tests/ -v                        # 7 guardrail tests

```



\---



<p align="center">

&#x20; <sub>Python · FastAPI · React · ChromaDB · Llama 3.3 · Docker · Render · Vercel</sub>

</p>

