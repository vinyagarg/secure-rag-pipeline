import sys
import json
from datetime import datetime
sys.path.append("eval")
sys.path.append("guardrails")
from eval_retrieval import evaluate_retrieval
from judge import run_judge_eval
from eval_consistency import check_consistency

def run_full_eval():
    print("Running retrieval evaluation...")
    retrieval_report = evaluate_retrieval(k=3)

    print("\nRunning LLM-as-judge evaluation...")
    judge_report = run_judge_eval()

    print("\nRunning consistency checks...")
    consistency_questions = ["What is overfitting?", "Explain KNN in simple terms"]
    consistency_results = [check_consistency(q) for q in consistency_questions]
    avg_consistency = sum(r["avg_similarity"] for r in consistency_results) / len(consistency_results)

    final_report = {
        "timestamp": datetime.now().isoformat(),
        "retrieval": {
            "recall_at_3": retrieval_report["recall_at_k"],
            "hits": retrieval_report["hits"],
            "total": retrieval_report["total_questions"]
        },
        "generation_quality": {
            "avg_relevance": judge_report["avg_relevance"],
            "avg_faithfulness": judge_report["avg_faithfulness"]
        },
        "consistency": {
            "avg_similarity": round(avg_consistency, 3)
        }
    }

    with open("eval/eval_report.json", "w") as f:
        json.dump(final_report, f, indent=2)

    print("\n" + "="*50)
    print("FINAL EVAL REPORT")
    print("="*50)
    print(f"Retrieval Recall@3: {final_report['retrieval']['recall_at_3']} ({final_report['retrieval']['hits']}/{final_report['retrieval']['total']})")
    print(f"Avg Relevance: {final_report['generation_quality']['avg_relevance']}/5")
    print(f"Avg Faithfulness: {final_report['generation_quality']['avg_faithfulness']}/5")
    print(f"Avg Consistency: {final_report['consistency']['avg_similarity']}")
    print(f"\nSaved to eval/eval_report.json")

if __name__ == "__main__":
    run_full_eval()