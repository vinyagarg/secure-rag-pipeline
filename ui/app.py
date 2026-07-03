import streamlit as st
import requests
import os
import sys
sys.path.append("logs")
sys.path.append("ui")

from db import init_db, save_message, load_messages, clear_messages

try:
    from audit_logger import get_recent_logs, get_stats, init_audit_db
except Exception:
    def get_recent_logs(limit=20): return []
    def get_stats(): return {"total_requests": 0, "total_blocked": 0, "block_rate": 0.0, "avg_grounding_score": None, "avg_latency_ms": None}
    def init_audit_db(): pass

st.set_page_config(page_title="RAGuard", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

init_db()
init_audit_db()

if "messages" not in st.session_state:
    st.session_state.messages = load_messages()
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
* { font-family: 'Inter', -apple-system, sans-serif !important; }
#MainMenu, footer { visibility: hidden; }

.stApp { background: #080808; }

[data-testid="stSidebar"] {
    background: #0a0a0a !important;
    border-right: 1px solid #161616 !important;
}

.block-container {
    max-width: 700px !important;
    margin: 0 auto !important;
    padding-top: 2rem !important;
    padding-bottom: 8rem !important;
}

/* Native chat message overrides */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0.25rem 0 !important;
    gap: 10px !important;
}

[data-testid="stChatMessageAvatarUser"] {
    display: none !important;
}

[data-testid="stChatMessageAvatarAssistant"] {
    background: #111 !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 6px !important;
    width: 24px !important;
    height: 24px !important;
    font-size: 11px !important;
}

[data-testid="stChatMessageContent"] p {
    color: #b0b0b0 !important;
    font-size: 0.875rem !important;
    line-height: 1.7 !important;
    margin: 0 !important;
}

/* User messages — right aligned */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
    background: #111 !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 10px 10px 2px 10px !important;
    padding: 10px 14px !important;
    margin-left: auto !important;
    max-width: 80% !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] p {
    color: #d0d0d0 !important;
}

/* Input */
[data-testid="stChatInput"] {
    background: #0a0a0a !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 10px !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #999 !important;
    font-size: 0.85rem !important;
}

/* Sidebar */
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
    color: #444 !important;
    font-size: 0.78rem !important;
}
[data-testid="stSidebar"] h3 {
    color: #fff !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}
div[data-testid="stSidebar"] button {
    background: transparent !important;
    border: 1px solid #181818 !important;
    color: #555 !important;
    border-radius: 6px !important;
    font-size: 0.78rem !important;
    text-align: left !important;
    margin-bottom: 3px !important;
    transition: all 0.1s !important;
}
div[data-testid="stSidebar"] button:hover {
    border-color: #2a2a2a !important;
    color: #999 !important;
}

/* Expander */
details summary {
    color: #333 !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.02em !important;
}
details summary:hover { color: #555 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #141414 !important;
    margin-bottom: 1.5rem !important;
}
.stTabs [data-baseweb="tab"] {
    color: #333 !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #888 !important;
    border-bottom: 1px solid #444 !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: #0d0d0d !important;
    border: 1px solid #141414 !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}
[data-testid="metric-container"] label {
    color: #333 !important;
    font-size: 0.65rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ddd !important;
    font-size: 1.4rem !important;
    font-weight: 600 !important;
}

/* Spinner */
.stSpinner { color: #333 !important; }

/* Confidence */
.conf-badge {
    display: inline-block;
    font-size: 0.68rem;
    color: #333;
    letter-spacing: 0.04em;
    margin-top: 6px;
    padding-left: 2px;
}
.conf-dot {
    display: inline-block;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    margin-right: 5px;
    vertical-align: middle;
    position: relative;
    top: -1px;
}
.dot-high { background: #22c55e; }
.dot-med { background: #f59e0b; }
.dot-low { background: #ef4444; }
</style>
""", unsafe_allow_html=True)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def confidence_label(distance):
    if distance is None: return None, None
    if distance < 0.6: return "High confidence", "high"
    elif distance < 1.0: return "Medium confidence", "med"
    else: return "Low confidence", "low"

# Sidebar
with st.sidebar:
    st.markdown("### RAGuard")
    st.markdown("<p style='color:#333;font-size:0.75rem;line-height:1.6;margin:0 0 1rem'>AI assistant grounded in source documents. Refuses to guess.</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='color:#2a2a2a;font-size:0.62rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px'>Suggested</p>", unsafe_allow_html=True)

    for q in [
        "What is RAG and how does it work?",
        "Fine-tuning vs RAG — which to use?",
        "How do guardrails protect AI systems?",
        "What are chunking strategies for RAG?",
        "How does LLM evaluation work?",
        "What is prompt injection?",
    ]:
        if st.button(q, use_container_width=True, key=f"ex_{q}"):
            st.session_state.pending_question = q

    st.markdown("---")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        clear_messages()
        st.rerun()

    st.markdown("<p style='color:#1e1e1e;font-size:0.62rem;margin-top:1.5rem'>FastAPI · ChromaDB · Llama 3.3 · Jina</p>", unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["Chat", "System"])

with tab1:
    # Header
    st.markdown("""
    <div style='margin-bottom:2rem;padding-bottom:1.5rem;border-bottom:1px solid #111'>
        <div style='display:flex;align-items:center;gap:8px;margin-bottom:4px'>
            <span style='font-size:0.95rem'>🛡️</span>
            <span style='font-size:0.95rem;font-weight:600;color:#e0e0e0;letter-spacing:-0.01em'>RAGuard</span>
        </div>
        <div style='font-size:0.78rem;color:#333;margin-bottom:10px'>Smart enough to answer. Smart enough to know when not to.</div>
        <div style='display:flex;gap:6px;flex-wrap:wrap'>
            <span style='font-size:0.65rem;color:#2a2a2a;border:1px solid #161616;padding:2px 7px;border-radius:4px'>Grounded generation</span>
            <span style='font-size:0.65rem;color:#2a2a2a;border:1px solid #161616;padding:2px 7px;border-radius:4px'>Source-cited</span>
            <span style='font-size:0.65rem;color:#2a2a2a;border:1px solid #161616;padding:2px 7px;border-radius:4px'>Injection defense</span>
            <span style='font-size:0.65rem;color:#2a2a2a;border:1px solid #161616;padding:2px 7px;border-radius:4px'>Eval pipeline</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state.messages:
        avatar = None if msg["role"] == "user" else "🛡️"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])
            if msg["role"] == "assistant":
                avg_dist = msg.get("avg_distance")
                label, level = confidence_label(avg_dist)
                if label:
                    dot_class = f"dot-{level}"
                    st.markdown(f'<div class="conf-badge"><span class="conf-dot {dot_class}"></span>{label}</div>', unsafe_allow_html=True)
                if msg.get("sources"):
                    with st.expander("sources"):
                        for s in msg["sources"]:
                            st.markdown(f"<span style='font-size:0.72rem;color:#333'>↳ {s}</span>", unsafe_allow_html=True)

    # Input
    typed_input = st.chat_input("Ask anything about RAG, LLMs, or AI engineering...")
    query_to_run = st.session_state.pending_question or typed_input
    st.session_state.pending_question = None

    if query_to_run:
        st.session_state.messages.append({"role": "user", "content": query_to_run})
        save_message("user", query_to_run)

        with st.chat_message("user", avatar=None):
            st.write(query_to_run)

        with st.chat_message("assistant", avatar="🛡️"):
            with st.spinner(""):
                try:
                    response = requests.post(f"{API_URL}/query", json={"question": query_to_run}, timeout=60)
                    data = response.json()
                    answer = data["answer"]
                    sources = data.get("sources", [])
                    distances = data.get("distances", [])
                    avg_distance = sum(distances) / len(distances) if distances else None

                    st.write(answer)

                    label, level = confidence_label(avg_distance)
                    if label:
                        dot_class = f"dot-{level}"
                        st.markdown(f'<div class="conf-badge"><span class="conf-dot {dot_class}"></span>{label}</div>', unsafe_allow_html=True)

                    if sources:
                        with st.expander("sources"):
                            for s in sources:
                                st.markdown(f"<span style='font-size:0.72rem;color:#333'>↳ {s}</span>", unsafe_allow_html=True)

                    st.session_state.messages.append({
                        "role": "assistant", "content": answer,
                        "sources": sources, "avg_distance": avg_distance
                    })
                    save_message("assistant", answer, sources, avg_distance)

                except Exception:
                    st.markdown("<span style='color:#2a2a2a;font-size:0.82rem'>Connection error. Make sure the API is running.</span>", unsafe_allow_html=True)

with tab2:
    st.markdown("<p style='font-size:0.62rem;color:#2a2a2a;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1rem'>System observability</p>", unsafe_allow_html=True)
    try:
        stats = get_stats()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Requests", stats["total_requests"])
        col2.metric("Blocked", stats["total_blocked"])
        col3.metric("Block rate", f"{stats['block_rate']*100:.0f}%")
        col4.metric("Avg grounding", f"{stats['avg_grounding_score']}/5" if stats['avg_grounding_score'] else "—")

        logs = get_recent_logs(15)
        if logs:
            import pandas as pd
            df = pd.DataFrame(logs, columns=["Time", "Query", "Blocked", "Stage", "Grounding", "Distance", "Latency ms"])
            df["Blocked"] = df["Blocked"].map({1: "blocked", 0: "—"})
            df["Time"] = df["Time"].str[:19].str.replace("T", " ")
            st.markdown("<p style='font-size:0.62rem;color:#2a2a2a;text-transform:uppercase;letter-spacing:0.1em;margin:1.5rem 0 0.5rem'>Recent requests</p>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.markdown("<p style='font-size:0.78rem;color:#2a2a2a'>No requests logged yet.</p>", unsafe_allow_html=True)
    except Exception:
        st.markdown("<p style='font-size:0.78rem;color:#2a2a2a'>Stats unavailable.</p>", unsafe_allow_html=True)
   

