import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

JUDGE_PROMPT = """You are evaluating whether an AI's answer is faithfully grounded in the given context, with no unsupported claims.

Context:
{context}

Answer to evaluate:
{answer}

Rate the faithfulness of the answer on a scale of 1 to 5:
5 = Fully grounded, every claim is directly supported by the context
3 = Partially grounded, some claims are not clearly supported
1 = Not grounded, makes claims unsupported by or contradicting the context

Respond with ONLY a single number (1-5), nothing else."""

def check_grounding(answer: str, context_chunks: list) -> dict:
    context_text = "\n\n".join([c["text"] for c in context_chunks])
    prompt = JUDGE_PROMPT.format(context=context_text, answer=answer)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=5
    )

    try:
        score = int(response.choices[0].message.content.strip())
    except ValueError:
        score = None

    return {
        "score": score,
        "is_grounded": score is not None and score >= 4
    }

if __name__ == "__main__":
    import sys
    sys.path.append("retrieval")
    from retrieve import retrieve
    from generate import generate_answer

    query = "What is overfitting?"
    chunks = retrieve(query, k=3)
    answer = generate_answer(query, chunks)

    print(f"Question: {query}")
    print(f"Answer: {answer}\n")

    result = check_grounding(answer, chunks)
    print(f"Grounding score: {result['score']}/5")
    print(f"Considered grounded: {result['is_grounded']}")

    fake_answer = "Overfitting was invented in 1995 by a team at MIT and only affects neural networks, never decision trees."
    print(f"\n--- Testing a fabricated answer ---")
    print(f"Fake answer: {fake_answer}")
    fake_result = check_grounding(fake_answer, chunks)
    print(f"Grounding score: {fake_result['score']}/5")
    print(f"Considered grounded: {fake_result['is_grounded']}")