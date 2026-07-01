import sys
import time
sys.path.append("retrieval")
sys.path.append("guardrails")
sys.path.append("logs")

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from rag_secure import ask_secure
from audit_logger import init_audit_db, log_request

load_dotenv()

app = FastAPI(title="RAGuard API")
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