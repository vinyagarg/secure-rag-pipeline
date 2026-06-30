import sys
import json
sys.path.append("retrieval")
from retrieve import retrieve
from generate import generate_answer
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def check_consistency(question, runs=3):
    answers = []
    for _ in range(runs):
        chunks = retrieve(question, k=3)
        answer = generate_answer(question, chunks)
        answers.append(answer)

    embeddings = model.encode(answers).tolist()

    similarities = []
    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            similarities.append(cosine_similarity(embeddings[i], embeddings[j]))

    avg_similarity = sum(similarities) / len(similarities)

    return {
        "question": question,
        "answers": answers,
        "avg_similarity": round(avg_similarity, 3)
    }

if __name__ == "__main__":
    test_questions = [
        "What is overfitting?",
        "Explain KNN in simple terms",
        "What is Bayes theorem used for?"
    ]

    for q in test_questions:
        result = check_consistency(q)
        print(f"\nQuestion: {result['question']}")
        print(f"Avg similarity across 3 runs: {result['avg_similarity']}")
        for i, a in enumerate(result["answers"], 1):
            print(f"  Run {i}: {a[:90]}...")