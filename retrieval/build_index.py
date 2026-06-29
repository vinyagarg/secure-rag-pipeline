import sys
sys.path.append("ingestion")
from ingest import load_documents, chunk_text
from sentence_transformers import SentenceTransformer
import chromadb

def build_index():
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    docs = load_documents()
    all_chunks = []
    for doc in docs:
        for chunk in chunk_text(doc["text"]):
            all_chunks.append({"source": doc["filename"], "text": chunk})

    print(f"Embedding {len(all_chunks)} chunks...")
    texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts).tolist()

    client = chromadb.PersistentClient(path="./chroma_db")
    try:
        client.delete_collection("my_docs")
    except Exception:
        pass
    collection = client.create_collection(name="my_docs")

    collection.add(
        ids=[str(i) for i in range(len(all_chunks))],
        embeddings=embeddings,
        documents=texts,
        metadatas=[{"source": c["source"]} for c in all_chunks]
    )
    print(f"Index built and saved to ./chroma_db with {len(all_chunks)} chunks.")

if __name__ == "__main__":
    build_index()