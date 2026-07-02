from sentence_transformers import SentenceTransformer
import chromadb

_model = None
_collection = None

def _load() -> None:
    """Load embedding model and ChromaDB collection (lazy, cached after first call)."""
    global _model, _collection
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    if _collection is None:
        client = chromadb.PersistentClient(path="./chroma_db")
        _collection = client.get_collection("my_docs")

def retrieve(query: str, k: int = 3) -> list[dict]:
    """
    Retrieve the top-k most semantically similar chunks for a given query.
    Returns a list of dicts with keys: text, distance, source.
    """
    _load()
    query_embedding = _model.encode([query]).tolist()
    results = _collection.query(query_embeddings=query_embedding, n_results=k)

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