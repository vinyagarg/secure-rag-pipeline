import sys
sys.path.append("ingestion")
from ingest import load_documents, chunk_text
from sentence_transformers import SentenceTransformer
import chromadb

def build_vector_store():
    print("Loading model... (first run downloads it, takes a minute)")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    docs = load_documents()
    all_chunks = []
    for doc in docs:
        for chunk in chunk_text(doc["text"]):
            all_chunks.append({"source": doc["filename"], "text": chunk})

    print(f"Embedding {len(all_chunks)} chunks...")
    texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts).tolist()

    client = chromadb.Client()
    collection = client.create_collection(name="my_docs")

    collection.add(
        ids=[str(i) for i in range(len(all_chunks))],
        embeddings=embeddings,
        documents=texts,
        metadatas=[{"source": c["source"]} for c in all_chunks]
    )
    print("Stored in vector database successfully.")
    return collection, model

if __name__ == "__main__":
    collection, model = build_vector_store()

    query = "why does a model fail on new data"
    query_embedding = model.encode([query]).tolist()

    results = collection.query(query_embeddings=query_embedding, n_results=2)

    print(f"\nQuery: {query}")
    print("\nTop matching chunks:")
    for doc in results["documents"][0]:
        print(f"- {doc[:120]}...")