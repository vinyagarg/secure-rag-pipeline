"""
retrieve.py — retrieves top-k semantically similar chunks using Jina AI embeddings API.
"""
import os
import requests as req
import chromadb
from dotenv import load_dotenv

load_dotenv()
JINA_API_KEY = os.getenv("JINA_API_KEY")
_collection = None

def _load():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path="./chroma_db")
        _collection = client.get_collection("my_docs")

def get_embedding(text: str) -> list[float]:
    response = req.post(
        "https://api.jina.ai/v1/embeddings",
        headers={
            "Authorization": f"Bearer {JINA_API_KEY}",
            "Content-Type": "application/json"
        },
        json={"model": "jina-embeddings-v3", "input": [text]}
    )
    return response.json()["data"][0]["embedding"]

def retrieve(query: str, k: int = 3) -> list[dict]:
    _load()
    query_embedding = get_embedding(query)
    results = _collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    matches = []
    for doc, distance, meta in zip(
        results["documents"][0],
        results["distances"][0],
        results["metadatas"][0]
    ):
        # Use URL from metadata if available, else filename
        url = meta.get("url", "").strip()
        source = url if url.startswith("http") else meta.get("source", "")
        matches.append({
            "text": doc,
            "distance": distance,
            "source": source
        })
    return matches

if __name__ == "__main__":
    test_queries = [
        "what is retrieval augmented generation",
        "how does chromadb work",
        "what is prompt injection",
    ]
    for q in test_queries:
        print(f"\nQuery: {q}")
        for m in retrieve(q, k=2):
            print(f"  source: {m['source']}")
            print(f"  distance: {m['distance']:.3f}")