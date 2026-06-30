import sys
sys.path.append("retrieval")
from fastapi import FastAPI
from pydantic import BaseModel
from rag import ask
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Secure RAG API")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]
    distances: list[float]

@app.get("/")
def health_check():
    return {"status": "running"}

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    answer, chunks = ask(request.question)
    sources = [c["source"] for c in chunks]
    distances = [c["distance"] for c in chunks]
    return QueryResponse(answer=answer, sources=sources, distances=distances)