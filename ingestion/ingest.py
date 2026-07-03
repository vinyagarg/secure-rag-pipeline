import os

def load_documents(data_folder="data"):
    documents = []
    for filename in os.listdir(data_folder):
        if filename.endswith(".txt") or filename.endswith(".md"):
            filepath = os.path.join(data_folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
                documents.append({"filename": filename, "text": text})
    return documents

def chunk_text(text, chunk_size=60, overlap=15):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents.\n")

    all_chunks = []
    for doc in docs:
        chunks = chunk_text(doc["text"])
        print(f"{doc['filename']} -> {len(chunks)} chunk(s)")
        for chunk in chunks:
            all_chunks.append({"source": doc["filename"], "text": chunk})

    print(f"\nTotal chunks created: {len(all_chunks)}")
    print("\n--- Sample chunk ---")
    print(all_chunks[0]["text"])