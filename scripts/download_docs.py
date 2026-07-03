"""
download_docs.py — scrapes LangChain documentation website directly
"""
import os
import requests
from bs4 import BeautifulSoup
import time

OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PAGES = [
    ("https://python.langchain.com/docs/concepts/rag/", "rag"),
    ("https://python.langchain.com/docs/concepts/vectorstores/", "vectorstores"),
    ("https://python.langchain.com/docs/concepts/embeddings/", "embeddings"),
    ("https://python.langchain.com/docs/concepts/retrievers/", "retrievers"),
    ("https://python.langchain.com/docs/concepts/text_splitters/", "text_splitters"),
    ("https://python.langchain.com/docs/concepts/chat_models/", "chat_models"),
    ("https://python.langchain.com/docs/concepts/prompt_templates/", "prompt_templates"),
    ("https://python.langchain.com/docs/concepts/output_parsers/", "output_parsers"),
    ("https://python.langchain.com/docs/concepts/agents/", "agents"),
    ("https://python.langchain.com/docs/concepts/tools/", "tools"),
    ("https://python.langchain.com/docs/concepts/memory/", "memory"),
    ("https://python.langchain.com/docs/concepts/callbacks/", "callbacks"),
    ("https://python.langchain.com/docs/concepts/streaming/", "streaming"),
    ("https://python.langchain.com/docs/concepts/structured_outputs/", "structured_outputs"),
    ("https://python.langchain.com/docs/concepts/document_loaders/", "document_loaders"),
    ("https://python.langchain.com/docs/concepts/few_shot_prompting/", "few_shot_prompting"),
    ("https://python.langchain.com/docs/concepts/evaluation/", "evaluation"),
    ("https://python.langchain.com/docs/tutorials/rag/", "tutorial_rag"),
    ("https://python.langchain.com/docs/tutorials/chatbot/", "tutorial_chatbot"),
    ("https://python.langchain.com/docs/tutorials/qa_chat_history/", "tutorial_qa_chat"),
]

headers = {"User-Agent": "Mozilla/5.0 (educational research bot)"}

print(f"Scraping {len(PAGES)} LangChain documentation pages...")
saved = 0
failed = 0

for url, name in PAGES:
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            main = soup.find("article") or soup.find("main") or soup.find("div", class_="markdown")
            if main:
                for tag in main.find_all(["script", "style", "nav", "footer"]):
                    tag.decompose()
                text = main.get_text(separator="\n", strip=True)
                if len(text) > 300:
                    filepath = os.path.join(OUTPUT_DIR, f"langchain_{name}.txt")
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(f"Source: {url}\n\n{text}")
                    print(f"  ✅ {name} ({len(text)} chars)")
                    saved += 1
                else:
                    print(f"  ⚠️  {name} (too short, skipping)")
                    failed += 1
            else:
                print(f"  ❌ {name} (no main content found)")
                failed += 1
        else:
            print(f"  ❌ {name} (status {response.status_code})")
            failed += 1
        time.sleep(0.5)
    except Exception as e:
        print(f"  ❌ {name} (error: {e})")
        failed += 1

print(f"\nDone: {saved} pages saved, {failed} failed")
print(f"Files saved to: {OUTPUT_DIR}/")