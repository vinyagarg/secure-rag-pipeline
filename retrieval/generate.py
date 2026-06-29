import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful assistant that answers questions using ONLY the context provided below.
If the answer is not in the context, say "I don't have enough information to answer that" - do not make up an answer.
Be concise and clear."""

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