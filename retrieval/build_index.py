"""
build_index.py — builds and saves the ChromaDB vector index using Jina AI embeddings API.
Run once after adding/changing documents in the data/ folder.
"""
import os
import sys
import requests as req
from dotenv import load_dotenv
sys.path.append("ingestion")
from ingest import load_documents, chunk_text
import chromadb

load_dotenv()
JINA_API_KEY = os.getenv("JINA_API_KEY")

def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Get embeddings from Jina AI API."""
    response = req.post(
        "https://api.jina.ai/v1/embeddings",
        headers={
            "Authorization": f"Bearer {JINA_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "jina-embeddings-v3",
            "input": texts
        }
    )
    data = response.json()
    return [item["embedding"] for item in data["data"]]

def build_index():
    print("Loading documents...")
    docs = load_documents()
    all_chunks = []
    for doc in docs:
        for chunk in chunk_text(doc["text"]):
            all_chunks.append({"source": doc["filename"], "text": chunk})

    print(f"Getting embeddings for {len(all_chunks)} chunks via Jina API...")
    texts = [c["text"] for c in all_chunks]

    batch_size = 8
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        embeddings = get_embeddings(batch)
        all_embeddings.extend(embeddings)
        print(f"  Embedded {min(i+batch_size, len(texts))}/{len(texts)} chunks")

    client = chromadb.PersistentClient(path="./chroma_db")
    try:
        client.delete_collection("my_docs")
    except Exception:
        pass
    collection = client.create_collection(name="my_docs")

    collection.add(
        ids=[str(i) for i in range(len(all_chunks))],
        embeddings=all_embeddings,
        documents=texts,
        metadatas=[{"source": c["source"]} for c in all_chunks]
    )
    print(f"Index built and saved to ./chroma_db with {len(all_chunks)} chunks.")

if __name__ == "__main__":
    build_index()