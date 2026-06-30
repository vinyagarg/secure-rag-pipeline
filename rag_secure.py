import sys
sys.path.append("retrieval")
sys.path.append("guardrails")

from retrieve import retrieve
from generate import generate_answer
from input_guardrail import check_input
from llm_guardrail import check_input_llm
from output_guardrail import check_output
from grounding_check import check_grounding

def ask_secure(query: str, k: int = 3) -> dict:
    pattern_check = check_input(query)
    if pattern_check["is_suspicious"]:
        return {
            "answer": "I can't process that request — it looks like an attempt to manipulate my instructions.",
            "sources": [],
            "blocked": True,
            "blocked_stage": "input_pattern",
            "blocked_reason": pattern_check["reason"]
        }

    llm_check = check_input_llm(query)
    if llm_check["is_suspicious"]:
        return {
            "answer": "I can't process that request — it looks like an attempt to manipulate my instructions.",
            "sources": [],
            "blocked": True,
            "blocked_stage": "input_llm",
            "blocked_reason": f"LLM classifier verdict: {llm_check['verdict']}"
        }

    chunks = retrieve(query, k=k)
    raw_answer = generate_answer(query, chunks)

    output_check = check_output(raw_answer)
    if output_check["is_unsafe"]:
        return {
            "answer": output_check["safe_answer"],
            "sources": [],
            "blocked": True,
            "blocked_stage": "output",
            "blocked_reason": f"Flagged patterns: {output_check['flagged_patterns']}"
        }

    grounding = check_grounding(raw_answer, chunks)

    return {
        "answer": raw_answer,
        "sources": [c["source"] for c in chunks],
        "distances": [c["distance"] for c in chunks],
        "blocked": False,
        "grounding_score": grounding["score"],
        "is_grounded": grounding["is_grounded"]
    }

if __name__ == "__main__":
    while True:
        query = input("\nAsk a question (or type 'exit'): ").strip()
        if query.lower() == "exit":
            break
        if not query:
            continue

        result = ask_secure(query)
        print(f"\nAnswer: {result['answer']}")

        if result["blocked"]:
            print(f"⚠️  BLOCKED at stage: {result['blocked_stage']}")
            print(f"   Reason: {result['blocked_reason']}")
        else:
            print(f"Sources: {result['sources']}")
            print(f"Grounding score: {result['grounding_score']}/5 ({'✅ grounded' if result['is_grounded'] else '⚠️ low grounding'})")