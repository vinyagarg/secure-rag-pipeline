import sys
sys.path.append("retrieval")
from retrieve import retrieve
from generate import generate_answer

def ask(query, k=3):
    chunks = retrieve(query, k=k)
    answer = generate_answer(query, chunks)
    return answer, chunks

if __name__ == "__main__":
    while True:
        query = input("\nAsk a question (or type 'exit'): ").strip()
        if query.lower() == "exit":
            break
        if not query:
            print("Please type a question.")
            continue
        answer, chunks = ask(query)
        print(f"\nAnswer: {answer}")
        print("\nSources:")
        for c in chunks:
            print(f"  [{c['source']}] distance={c['distance']:.3f}")