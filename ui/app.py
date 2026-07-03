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

st.set_page_config(
    page_title="RAGuard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()
init_audit_db()

if "messages" not in st.session_state:
    st.session_state.messages = load_messages()
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

* { font-family: 'Inter', sans-serif; }
#MainMenu, footer { visibility: hidden; }

.stApp {
    background-color: #080808;
}

[data-testid="stSidebar"] {
    background-color: #0d0d0d;
    border-right: 1px solid #1a1a1a;
}

[data-testid="stSidebar"] * {
    color: #888 !important;
}

[data-testid="stSidebar"] h3 {
    color: #fff !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

[data-testid="stSidebar"] hr {
    border-color: #1a1a1a !important;
    margin: 1rem 0 !important;
}

div[data-testid="stSidebar"] button {
    background: transparent !important;
    border: 1px solid #1e1e1e !important;
    color: #666 !important;
    border-radius: 6px !important;
    font-size: 0.8rem !important;
    padding: 0.4rem 0.75rem !important;
    text-align: left !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
    margin-bottom: 4px !important;
}

div[data-testid="stSidebar"] button:hover {
    border-color: #333 !important;
    color: #ccc !important;
    background: #111 !important;
}

.block-container {
    padding-top: 3rem;
    padding-bottom: 6rem;
    max-width: 680px;
    margin: 0 auto;
}

.raguard-header {
    margin-bottom: 2.5rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid #141414;
}

.raguard-wordmark {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
}

.raguard-name {
    font-size: 1.1rem;
    font-weight: 600;
    color: #fff;
    letter-spacing: -0.01em;
}

.raguard-tagline {
    font-size: 0.82rem;
    color: #444;
    letter-spacing: 0.01em;
}

.raguard-pills {
    display: flex;
    gap: 6px;
    margin-top: 14px;
    flex-wrap: wrap;
}

.pill {
    font-size: 0.7rem;
    color: #555;
    border: 1px solid #1e1e1e;
    padding: 2px 8px;
    border-radius: 4px;
    letter-spacing: 0.02em;
}

.msg-user {
    display: flex;
    justify-content: flex-end;
    margin: 1rem 0 0.5rem 0;
}

.msg-user-bubble {
    background: #141414;
    border: 1px solid #1e1e1e;
    color: #e0e0e0;
    padding: 10px 14px;
    border-radius: 10px 10px 2px 10px;
    font-size: 0.88rem;
    max-width: 85%;
    line-height: 1.5;
}

.msg-assistant {
    display: flex;
    gap: 10px;
    margin: 0.5rem 0 1rem 0;
    align-items: flex-start;
}

.msg-icon {
    width: 22px;
    height: 22px;
    background: #141414;
    border: 1px solid #1e1e1e;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    flex-shrink: 0;
    margin-top: 2px;
}

.msg-content {
    color: #c0c0c0;
    font-size: 0.88rem;
    line-height: 1.65;
    flex: 1;
}

.msg-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 8px;
}

.conf-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    flex-shrink: 0;
}

.conf-high { background: #22c55e; }
.conf-med { background: #f59e0b; }
.conf-low { background: #ef4444; }

.conf-text {
    font-size: 0.7rem;
    color: #444;
    letter-spacing: 0.02em;
}

.divider {
    border: none;
    border-top: 1px solid #111;
    margin: 2rem 0;
}

[data-testid="stChatInput"] textarea {
    background: #0d0d0d !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 8px !important;
    color: #ccc !important;
    font-size: 0.85rem !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: #333 !important;
    box-shadow: none !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #141414 !important;
    gap: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #444 !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1rem !important;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    color: #fff !important;
    border-bottom: 1px solid #fff !important;
}

.admin-card {
    background: #0d0d0d;
    border: 1px solid #141414;
    border-radius: 8px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}

.admin-label {
    font-size: 0.65rem;
    color: #444;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 4px;
}

.admin-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: #e0e0e0;
}

.streamlit-expanderHeader {
    font-size: 0.72rem !important;
    color: #444 !important;
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def confidence_label(distance):
    if distance is None:
        return None, None
    if distance < 0.6:
        return "High confidence", "high"
    elif distance < 1.0:
        return "Medium confidence", "med"
    else:
        return "Low confidence", "low"

with st.sidebar:
    st.markdown("### RAGuard")
    st.markdown("<p style='font-size:0.78rem;color:#444;line-height:1.6;margin-bottom:0'>AI assistant grounded in source documents. Refuses to guess.</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='font-size:0.65rem;color:#333;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px'>Suggested</p>", unsafe_allow_html=True)

    examples = [
        "What is RAG and how does it work?",
        "Fine-tuning vs RAG — which to use?",
        "How do guardrails protect AI systems?",
        "What are chunking strategies for RAG?",
        "How does LLM evaluation work?",
        "What is prompt injection?",
    ]
    for q in examples:
        if st.button(q, use_container_width=True, key=f"ex_{q}"):
            st.session_state.pending_question = q

    st.markdown("---")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        clear_messages()
        st.rerun()

    st.markdown("<p style='font-size:0.65rem;color:#2a2a2a;margin-top:1rem'>Built with FastAPI · ChromaDB · Llama 3.3</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Chat", "System"])

with tab1:
    st.markdown("""
    <div class="raguard-header">
        <div class="raguard-wordmark">
            <span>🛡️</span>
            <span class="raguard-name">RAGuard</span>
        </div>
        <div class="raguard-tagline">Smart enough to answer. Smart enough to know when not to.</div>
        <div class="raguard-pills">
            <span class="pill">Grounded generation</span>
            <span class="pill">Source-cited</span>
            <span class="pill">Injection defense</span>
            <span class="pill">Eval pipeline</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-user">
                <div class="msg-user-bubble">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            avg_dist = msg.get("avg_distance")
            label, level = confidence_label(avg_dist)
            conf_html = ""
            if label and level:
                conf_html = f'<span class="conf-dot conf-{level}"></span><span class="conf-text">{label}</span>'

            st.markdown(f"""
            <div class="msg-assistant">
                <div class="msg-icon">🛡</div>
                <div>
                    <div class="msg-content">{msg["content"]}</div>
                    <div class="msg-meta">{conf_html}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if msg.get("sources"):
                with st.expander("Sources", expanded=False):
                    for s in msg["sources"]:
                        st.markdown(f"<span style='font-size:0.72rem;color:#444'>↳ {s}</span>", unsafe_allow_html=True)

    typed_input = st.chat_input("Ask anything about RAG, LLMs, or AI engineering...")
    query_to_run = st.session_state.pending_question or typed_input
    st.session_state.pending_question = None

    if query_to_run:
        st.session_state.messages.append({"role": "user", "content": query_to_run})
        save_message("user", query_to_run)

        st.markdown(f"""
        <div class="msg-user">
            <div class="msg-user-bubble">{query_to_run}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner(""):
            try:
                response = requests.post(f"{API_URL}/query", json={"question": query_to_run}, timeout=60)
                data = response.json()
                answer = data["answer"]
                sources = data.get("sources", [])
                distances = data.get("distances", [])
                avg_distance = sum(distances) / len(distances) if distances else None
                label, level = confidence_label(avg_distance)

                conf_html = ""
                if label and level:
                    conf_html = f'<span class="conf-dot conf-{level}"></span><span class="conf-text">{label}</span>'

                st.markdown(f"""
                <div class="msg-assistant">
                    <div class="msg-icon">🛡</div>
                    <div>
                        <div class="msg-content">{answer}</div>
                        <div class="msg-meta">{conf_html}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if sources:
                    with st.expander("Sources", expanded=False):
                        for s in sources:
                            st.markdown(f"<span style='font-size:0.72rem;color:#444'>↳ {s}</span>", unsafe_allow_html=True)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                    "avg_distance": avg_distance
                })
                save_message("assistant", answer, sources, avg_distance)

            except Exception as e:
                st.markdown(f"""
                <div class="msg-assistant">
                    <div class="msg-icon">🛡</div>
                    <div class="msg-content" style="color:#444">Connection error. Make sure the API is running.</div>
                </div>
                """, unsafe_allow_html=True)

with tab2:
    st.markdown("<p style='font-size:0.65rem;color:#333;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1.5rem'>System</p>", unsafe_allow_html=True)

    try:
        stats = get_stats()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""<div class="admin-card"><div class="admin-label">Requests</div><div class="admin-value">{stats['total_requests']}</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="admin-card"><div class="admin-label">Blocked</div><div class="admin-value">{stats['total_blocked']}</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class="admin-card"><div class="admin-label">Block rate</div><div class="admin-value">{stats['block_rate']*100:.0f}%</div></div>""", unsafe_allow_html=True)
        with col4:
            grounding = f"{stats['avg_grounding_score']}/5" if stats['avg_grounding_score'] else "—"
            st.markdown(f"""<div class="admin-card"><div class="admin-label">Avg grounding</div><div class="admin-value">{grounding}</div></div>""", unsafe_allow_html=True)

        st.markdown("<p style='font-size:0.65rem;color:#333;text-transform:uppercase;letter-spacing:0.1em;margin:1.5rem 0 0.75rem 0'>Recent requests</p>", unsafe_allow_html=True)
        logs = get_recent_logs(15)
        if logs:
            import pandas as pd
            df = pd.DataFrame(logs, columns=["Time", "Query", "Blocked", "Stage", "Grounding", "Distance", "Latency ms"])
            df["Blocked"] = df["Blocked"].map({1: "blocked", 0: "—"})
            df["Time"] = df["Time"].str[:19].str.replace("T", " ")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.markdown("<p style='font-size:0.78rem;color:#333'>No requests yet.</p>", unsafe_allow_html=True)
    except Exception:
        st.markdown("<p style='font-size:0.78rem;color:#333'>Stats unavailable in this environment.</p>", unsafe_allow_html=True)
   

