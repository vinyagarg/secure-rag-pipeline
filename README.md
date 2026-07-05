\# 🛡️ RAGuard



> \*\*A secure Retrieval-Augmented Generation (RAG) pipeline that answers only from trusted documents—and knows when to say "I don't know."\*\*



\[!\[Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square\&logo=python\&logoColor=white)](https://python.org)

\[!\[FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square\&logo=fastapi)](https://raguard-api.onrender.com/docs)

\[!\[Next.js](https://img.shields.io/badge/Next.js-Frontend-black?style=flat-square\&logo=next.js)](https://secure-rag-pipeline.vercel.app)

\[!\[License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](LICENSE)



\## 🚀 Live Demo



🌐 \*\*Frontend:\*\* https://secure-rag-pipeline.vercel.app



📖 \*\*API Documentation:\*\* https://raguard-api.onrender.com/docs



\### Demo Credentials



| Role | Username |

|------|----------|

| User | `user123` |

| Admin | `admin123` |



\---



\# 📖 Overview



RAGuard is a production-ready Retrieval-Augmented Generation system focused on \*\*security, reliability, and transparency\*\*.



Unlike traditional RAG systems that attempt to answer every question, RAGuard answers \*\*only when sufficient evidence exists\*\* in the retrieved documents. Every response passes through multiple validation stages, ensuring it is grounded, sanitized, and fully traceable.



\### Key Features



\- 🔒 Multi-layer input and output guardrails

\- 📚 Retrieval using semantic vector search (ChromaDB)

\- 🤖 Grounded answer generation with Llama 3.3 70B

\- ✅ LLM-based grounding verification

\- 📊 Built-in evaluation framework

\- 📝 Complete audit logging for every request

\- 🐳 Dockerized deployment

\- ⚡ FastAPI backend with Next.js frontend



\---



\# 🏗️ System Architecture



```text

&#x20;                User Query

&#x20;                     │

&#x20;                     ▼

&#x20;       Pattern-based Input Guardrail

&#x20;                     │

&#x20;                     ▼

&#x20;       LLM Intent Classification

&#x20;                     │

&#x20;                     ▼

&#x20;     ChromaDB Semantic Retrieval

&#x20;          (616 document chunks)

&#x20;                     │

&#x20;                     ▼

&#x20;      Llama 3.3 70B Generation

&#x20;                     │

&#x20;                     ▼

&#x20;    Output Guardrail (PII Filtering)

&#x20;                     │

&#x20;                     ▼

&#x20;     LLM Grounding Verification

&#x20;          (Faithfulness Score)

&#x20;                     │

&#x20;                     ▼

&#x20;     SQLite Audit Logging

&#x20;                     │

&#x20;                     ▼

&#x20;             Final Response

```



\---



\# 📊 Evaluation



All metrics are fully reproducible.



```bash

python eval/run\_eval.py

```



| Metric | Result |

|---------|--------|

| Retrieval Recall@3 | \*\*100%\*\* (15/15 golden questions) |

| Answer Relevance | \*\*4.93 / 5.00\*\* |

| Answer Faithfulness | \*\*4.67 / 5.00\*\* |

| Consistency (3 runs) | \*\*0.997 / 1.00\*\* |

| Guardrail Test Suite | \*\*7 / 7 Passing\*\* |



\---



\# 🛠️ Tech Stack



| Layer | Technology |

|--------|------------|

| Frontend | Next.js, React |

| Backend | FastAPI, Uvicorn |

| LLM | Llama 3.3 70B (Groq) |

| Embeddings | Jina Embeddings v3 |

| Vector Database | ChromaDB |

| Evaluation | LLM-as-Judge |

| Logging | SQLite |

| Testing | Pytest |

| Deployment | Render, Vercel |

| Containerization | Docker |



\---



\# ⚡ Quick Start



\## Clone the repository



```bash

git clone https://github.com/vinyagarg/secure-rag-pipeline.git



cd secure-rag-pipeline

```



\## Install dependencies



```bash

pip install -r requirements.txt

```



\## Configure environment variables



```bash

cp .env.example .env

```



Add:



```

GROQ\_API\_KEY=your\_key

JINA\_API\_KEY=your\_key

```



\## Build the vector index



```bash

python retrieval/build\_index.py

```



\## Run the backend



```bash

uvicorn api.main:app --reload

```



API will be available at:



```

http://localhost:8000

```



\---



\# 💻 Frontend



```bash

cd frontend



npm install



npm run dev

```



Frontend runs at:



```

http://localhost:3000

```



\---



\# 🧪 Evaluation



Run the complete evaluation suite:



```bash

python eval/run\_eval.py

```



Run unit tests:



```bash

pytest tests -v

```



\---



\# 📁 Project Structure



```text

secure-rag-pipeline

│

├── api/

├── frontend/

├── retrieval/

├── eval/

├── tests/

├── logs/

├── chroma\_db/

├── requirements.txt

└── README.md

```



\---



\# 🔒 Security Features



\- Pattern-based prompt injection detection

\- LLM intent classification

\- Retrieval grounding

\- Hallucination detection

\- Output sanitization

\- PII filtering

\- Audit logging

\- Confidence scoring



\---



\# 📄 License



This project is licensed under the MIT License.



\---



<p align="center">

Built with ❤️ using Python • FastAPI • ChromaDB • Llama 3.3 • Next.js • Docker

</p>

