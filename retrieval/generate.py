import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert AI engineer assistant that answers questions using ONLY the context provided below.

Rules:
- Answer in depth and detail — do not give one-line answers
- Use numbered steps, bullet points, and structure whenever explaining a process or comparison
- For case studies and real-world scenarios, explain the problem, the solution approach, and the outcome
- Show your reasoning — explain WHY things work, not just WHAT they are
- If comparing two things, use a structured comparison
- If explaining a pipeline or flow, describe each step clearly in order
- If the answer is not in the context, say exactly: "I don't have enough information to answer that"
- Never make up information not present in the context"""

def generate_answer(query, context_chunks):
    context_text = "\n\n".join([f"[{c['source']}]: {c['text']}" for c in context_chunks])

    user_prompt = f"""Context:
{context_text}

Question: {query}

Answer using only the context above."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    from retrieve import retrieve
    query = "why does a model fail on new data"
    chunks = retrieve(query, k=3)
    answer = generate_answer(query, chunks)
    print(f"Question: {query}\n")
    print(f"Answer: {answer}")