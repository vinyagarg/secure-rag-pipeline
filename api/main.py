import sys
import time
sys.path.append("retrieval")
sys.path.append("guardrails")
sys.path.append("logs")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from rag_secure import ask_secure
from audit_logger import init_audit_db, log_request, get_stats, get_recent_logs

load_dotenv()

app = FastAPI(title="RAGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_audit_db()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]
    distances: list[float]
    blocked: bool
    grounding_score: int | None = None
    is_grounded: bool | None = None

@app.get("/")
def health_check():
    return {"status": "running", "project": "RAGuard"}

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    start = time.time()
    result = ask_secure(request.question)
    latency_ms = (time.time() - start) * 1000
    log_request(request.question, result, latency_ms)
    return QueryResponse(
        answer=result["answer"],
        sources=result.get("sources", []),
        distances=result.get("distances", []),
        blocked=result.get("blocked", False),
        grounding_score=result.get("grounding_score"),
        is_grounded=result.get("is_grounded")
    )

@app.get("/stats")
def get_stats_endpoint():
    return get_stats()

@app.get("/logs")
def get_logs_endpoint():
    rows = get_recent_logs(15)
    result = []
    for row in rows:
        result.append({
            "time": str(row[0])[:19].replace("T", " "),
            "query": str(row[1])[:60],
            "blocked": "blocked" if row[2] else "clean",
            "grounding": f"{row[4]}/5" if row[4] else "—",
            "latency": f"{round(row[6])}ms" if row[6] else "—"
        })
    return result