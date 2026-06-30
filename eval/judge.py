import sys
import json
import os
sys.path.append("retrieval")
from retrieve import retrieve
from generate import generate_answer
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

JUDGE_PROMPT = """Rate this AI-generated answer on two dimensions, each 1-5.

Question: {question}
Answer: {answer}
Expected keywords that should appear if correct: {keywords}

Relevance (1-5): does the answer actually address the question asked?
Faithfulness (1-5): does the answer avoid making things up, staying consistent with what a correct answer should contain?

Respond in EXACTLY this format, nothing else:
relevance: <number>
faithfulness: <number>"""

def judge_answer(question, answer, keywords):
    prompt = JUDGE_PROMPT.format(question=question, answer=answer, keywords=", ".join(keywords))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=30
    )
    text = response.choices[0].message.content.strip()

    relevance, faithfulness = None, None
    for line in text.split("\n"):
        if "relevance" in line.lower():
            relevance = int("".join(filter(str.isdigit, line)))
        if "faithfulness" in line.lower():
            faithfulness = int("".join(filter(str.isdigit, line)))

    return {"relevance": relevance, "faithfulness": faithfulness}

def run_judge_eval():
    with open("eval/golden_set.json") as f:
        golden_set = json.load(f)

    results = []
    for item in golden_set:
        question = item["question"]
        chunks = retrieve(question, k=3)
        answer = generate_answer(question, chunks)
        scores = judge_answer(question, answer, item["expected_keywords"])

        results.append({
            "question": question,
            "answer": answer,
            "relevance": scores["relevance"],
            "faithfulness": scores["faithfulness"]
        })
        print(f"✓ {question} -> relevance={scores['relevance']}, faithfulness={scores['faithfulness']}")

    avg_relevance = sum(r["relevance"] for r in results if r["relevance"]) / len(results)
    avg_faithfulness = sum(r["faithfulness"] for r in results if r["faithfulness"]) / len(results)

    return {
        "avg_relevance": round(avg_relevance, 2),
        "avg_faithfulness": round(avg_faithfulness, 2),
        "details": results
    }

if __name__ == "__main__":
    report = run_judge_eval()
    print(f"\nAverage relevance: {report['avg_relevance']}/5")
    print(f"Average faithfulness: {report['avg_faithfulness']}/5")