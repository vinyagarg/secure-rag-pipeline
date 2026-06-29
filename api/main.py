import sys
sys.path.append("retrieval")
from fastapi import FastAPI
from pydantic import BaseModel
from rag import ask

app = FastAPI(title="Secure RAG API")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

@app.get("/")
def health_check():
    return {"status": "running"}

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    answer, chunks = ask(request.question)
    sources = [c["source"] for c in chunks]
    return QueryResponse(answer=answer, sources=sources)