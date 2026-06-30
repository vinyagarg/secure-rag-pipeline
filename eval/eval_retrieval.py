import sys
import json
sys.path.append("retrieval")
from retrieve import retrieve

def evaluate_retrieval(k=3):
    with open("eval/golden_set.json") as f:
        golden_set = json.load(f)

    results = []
    hits = 0

    for item in golden_set:
        question = item["question"]
        expected_source = item["expected_source"]

        retrieved = retrieve(question, k=k)
        retrieved_sources = [r["source"] for r in retrieved]

        hit = expected_source in retrieved_sources
        if hit:
            hits += 1

        results.append({
            "question": question,
            "expected_source": expected_source,
            "retrieved_sources": retrieved_sources,
            "hit": hit
        })

    recall_at_k = hits / len(golden_set)

    return {
        "k": k,
        "total_questions": len(golden_set),
        "hits": hits,
        "recall_at_k": round(recall_at_k, 3),
        "details": results
    }

if __name__ == "__main__":
    report = evaluate_retrieval(k=3)
    print(f"Recall@{report['k']}: {report['recall_at_k']} ({report['hits']}/{report['total_questions']})\n")

    for r in report["details"]:
        status = "✅" if r["hit"] else "❌"
        print(f"{status} {r['question']}")
        print(f"   Expected: {r['expected_source']} | Got: {r['retrieved_sources']}")