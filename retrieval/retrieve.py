"""
retrieve.py — retrieves top-k semantically similar chunks using Jina AI embeddings API.
"""
import os
import requests as req
import chromadb
import numpy as np
from dotenv import load_dotenv

load_dotenv()
JINA_API_KEY = os.getenv("JINA_API_KEY")
_collection = None

def _load() -> None:
    """Load ChromaDB collection (lazy, cached after first call)."""
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path="./chroma_db")
        _collection = client.get_collection("my_docs")

def get_embedding(text: str) -> list[float]:
    """Get a single embedding from Jina AI API."""
    response = req.post(
        "https://api.jina.ai/v1/embeddings",
        headers={
            "Authorization": f"Bearer {JINA_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "jina-embeddings-v3",
            "input": [text]
        }
    )
    return response.json()["data"][0]["embedding"]

def retrieve(query: str, k: int = 3) -> list[dict]:
    """
    Retrieve the top-k most semantically similar chunks for a given query.
    Returns a list of dicts with keys: text, distance, source.
    """
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
        matches.append({"text": doc, "distance": distance, "source": meta["source"]})
    return matches

if __name__ == "__main__":
    test_queries = [
        "why does a model fail on new data",
        "how to evaluate a classifier",
        "what is bayes theorem used for"
    ]
    for q in test_queries:
        print(f"\nQuery: {q}")
        for m in retrieve(q, k=2):
            print(f"  [{m['source']}] distance={m['distance']:.3f} -> {m['text'][:100]}...")