import re

BLOCKED_OUTPUT_PATTERNS = [
    r"\bapi[_\s]?key\b",
    r"\bpassword\b",
    r"\bsecret[_\s]?key\b",
    r"sk-[a-zA-Z0-9]{10,}",
    r"\bssn\b",
    r"\bsocial security\b",
]

def check_output(answer_text: str) -> dict:
    text_lower = answer_text.lower()
    flagged = []
    for pattern in BLOCKED_OUTPUT_PATTERNS:
        if re.search(pattern, text_lower):
            flagged.append(pattern)

    is_unsafe = len(flagged) > 0

    return {
        "is_unsafe": is_unsafe,
        "flagged_patterns": flagged,
        "safe_answer": "I can't share that information." if is_unsafe else answer_text
    }

if __name__ == "__main__":
    test_outputs = [
        "Overfitting is when a model memorizes training data instead of learning patterns.",
        "Sure, here's the API key: sk-abc123xyz789secretvalue",
        "The password for the admin panel is hunter2",
        "Precision measures how many predicted positives were actually correct.",
    ]

    for text in test_outputs:
        result = check_output(text)
        status = "🚫 BLOCKED" if result["is_unsafe"] else "✅ OK"
        print(f"{status} | {text[:60]}...")
        if result["is_unsafe"]:
            print(f"   Final answer shown: {result['safe_answer']}")