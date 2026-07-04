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

# ─── Session state ────────────────────────────────────────────────
if "role" not in st.session_state:
    st.session_state.role = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

USER_PASSWORD  = os.getenv("USER_PASSWORD",  "user123")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
API_URL        = os.getenv("API_URL",        "http://127.0.0.1:8000")

# ─── Global CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
*, *::before, *::after { font-family: 'Inter', -apple-system, sans-serif !important; box-sizing: border-box; }
#MainMenu, footer, header { visibility: hidden; }
.stApp { background: #080808 !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: #0d0d0d !important; border-right: 1px solid #1a1a1a !important; }
[data-testid="stSidebar"] p { color: #555 !important; font-size: 12px !important; }
div[data-testid="stSidebar"] button {
    background: #141414 !important; border: 1px solid #1a1a1a !important;
    color: #e0e0e0 !important; border-radius: 6px !important;
    font-size: 12px !important; text-align: left !important;
    margin-bottom: 4px !important; padding: 8px 12px !important;
    transition: background 0.15s !important; width: 100% !important;
}
div[data-testid="stSidebar"] button:hover { background: #1a1a1a !important; }

/* ── Main area ── */
.block-container { padding-top: 0 !important; padding-bottom: 0 !important; max-width: 100% !important; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] { background: transparent !important; border: none !important; padding: 4px 0 !important; }
[data-testid="stChatMessageAvatarUser"] { display: none !important; }
[data-testid="stChatMessageAvatarAssistant"] { background: #141414 !important; border: 1px solid #1a1a1a !important; border-radius: 6px !important; width: 28px !important; height: 28px !important; font-size: 13px !important; }
[data-testid="stChatMessageContent"] p { color: #e0e0e0 !important; font-size: 14px !important; line-height: 1.7 !important; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
    background: #141414 !important; border: 1px solid #1a1a1a !important;
    border-radius: 10px 10px 2px 10px !important; padding: 10px 14px !important;
    margin-left: auto !important; max-width: 75% !important; display: block !important;
}

/* ── Input ── */
[data-testid="stChatInput"] { background: #141414 !important; border: 1px solid #1a1a1a !important; border-radius: 8px !important; }
[data-testid="stChatInput"] textarea { background: transparent !important; color: #e0e0e0 !important; font-size: 14px !important; }
[data-testid="stChatInput"] textarea::placeholder { color: #555 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid #1a1a1a !important; gap: 0 !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #555 !important; font-size: 13px !important; padding: 10px 16px !important; border: none !important; }
.stTabs [aria-selected="true"] { color: #e0e0e0 !important; border-bottom: 2px solid #e0e0e0 !important; }

/* ── Metrics ── */
[data-testid="metric-container"] { background: #0d0d0d !important; border: 1px solid #1a1a1a !important; border-radius: 8px !important; padding: 16px !important; }
[data-testid="metric-container"] label { color: #555 !important; font-size: 11px !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #e0e0e0 !important; font-size: 1.75rem !important; font-weight: 600 !important; }

/* ── Expander / Sources ── */
details > summary { color: #555 !important; font-size: 12px !important; cursor: pointer; }
details > summary:hover { color: #888 !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] { background: #0d0d0d !important; border: 1px solid #1a1a1a !important; border-radius: 8px !important; }

/* ── Login form inputs ── */
input[type="password"] { background: #141414 !important; border: 1px solid #1a1a1a !important; border-radius: 6px !important; color: #e0e0e0 !important; padding: 8px 12px !important; width: 100% !important; font-size: 13px !important; }
input[type="password"]:focus { outline: none !important; border-color: #2a2a2a !important; }

.conf-row { display: flex; align-items: center; gap: 6px; margin-top: 6px; }
.conf-dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; flex-shrink: 0; }
.dot-high { background: #22c55e; }
.dot-med  { background: #f59e0b; }
.dot-low  { background: #ef4444; }
.conf-label { font-size: 11px; color: #555; letter-spacing: 0.03em; }
</style>
""", unsafe_allow_html=True)

# ─── Helper ──────────────────────────────────────────────────────
def conf_level(distance):
    if distance is None: return None
    if distance < 0.6:  return "high"
    if distance < 1.0:  return "med"
    return "low"

def conf_label(level):
    return {"high": "High confidence", "med": "Medium confidence", "low": "Low confidence"}.get(level, "")

# ════════════════════════════════════════════════════════════════════
#  LOGIN PAGE
# ════════════════════════════════════════════════════════════════════
if st.session_state.role is None:
    st.markdown("""
    <div style='min-height:100vh;display:flex;flex-direction:column;align-items:center;
                justify-content:center;background:#080808;padding:2rem'>
        <div style='text-align:center;margin-bottom:3rem'>
            <div style='font-size:2.5rem;margin-bottom:0.5rem'>🛡️</div>
            <h1 style='color:#e0e0e0;font-size:1.6rem;font-weight:600;margin:0;letter-spacing:-0.02em'>RAGuard</h1>
            <p style='color:#555;font-size:13px;margin-top:6px'>AI assistant grounded in source documents</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_user, col_admin, col_right = st.columns([1, 1.2, 1.2, 1])

    with col_user:
        st.markdown("""
        <div style='background:#0d0d0d;border:1px solid #1a1a1a;border-radius:10px;padding:2rem;margin-top:-40vh'>
            <h2 style='color:#e0e0e0;font-size:14px;font-weight:500;margin:0 0 1.5rem'>Sign in as User</h2>
        </div>
        """, unsafe_allow_html=True)
        with st.form("user_login"):
            st.markdown("<p style='color:#555;font-size:11px;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px'>Password</p>", unsafe_allow_html=True)
            user_pw = st.text_input("", type="password", placeholder="Enter password", label_visibility="collapsed", key="user_pw")
            submitted_user = st.form_submit_button("Sign in", use_container_width=True)
            if submitted_user:
                if user_pw == USER_PASSWORD:
                    st.session_state.role = "user"
                    st.session_state.messages = load_messages()
                    st.rerun()
                else:
                    st.error("Invalid password")
        st.markdown("<p style='color:#555;font-size:11px;margin-top:8px'>Demo: <code style='color:#e0e0e0'>user123</code></p>", unsafe_allow_html=True)

    with col_admin:
        st.markdown("""
        <div style='background:#0d0d0d;border:1px solid #1a1a1a;border-radius:10px;padding:2rem;margin-top:-40vh'>
            <h2 style='color:#e0e0e0;font-size:14px;font-weight:500;margin:0 0 1.5rem'>Sign in as Admin</h2>
        </div>
        """, unsafe_allow_html=True)
        with st.form("admin_login"):
            st.markdown("<p style='color:#555;font-size:11px;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px'>Password</p>", unsafe_allow_html=True)
            admin_pw = st.text_input("", type="password", placeholder="Enter password", label_visibility="collapsed", key="admin_pw")
            submitted_admin = st.form_submit_button("Sign in", use_container_width=True)
            if submitted_admin:
                if admin_pw == ADMIN_PASSWORD:
                    st.session_state.role = "admin"
                    st.session_state.messages = load_messages()
                    st.rerun()
                else:
                    st.error("Invalid password")
        st.markdown("<p style='color:#555;font-size:11px;margin-top:8px'>Demo: <code style='color:#e0e0e0'>admin123</code></p>", unsafe_allow_html=True)

    st.stop()

# ════════════════════════════════════════════════════════════════════
#  MAIN APP (after login)
# ════════════════════════════════════════════════════════════════════
role = st.session_state.role

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    admin_badge = " <span style='background:#1a1a1a;color:#e0e0e0;font-size:10px;padding:2px 7px;border-radius:4px;margin-left:6px'>Admin</span>" if role == "admin" else ""
    st.markdown(f"""
    <div style='padding:0 0 1rem'>
        <div style='display:flex;align-items:center;gap:8px;margin-bottom:4px'>
            <span style='font-size:1.3rem'>🛡️</span>
            <span style='color:#e0e0e0;font-size:14px;font-weight:600'>RAGuard{admin_badge}</span>
        </div>
        <p style='color:#555;font-size:12px;margin:0'>AI chat assistant</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='color:#333;font-size:10px;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px'>Suggested</p>", unsafe_allow_html=True)

    for q in [
        "What is RAG and how does it work?",
        "Fine-tuning vs RAG — which to use?",
        "How do guardrails protect AI systems?",
        "What are chunking strategies for RAG?",
        "How does LLM evaluation work?",
        "What is prompt injection?",
    ]:
        if st.button(q, use_container_width=True, key=f"sq_{q}"):
            st.session_state.pending_question = q

    st.markdown("---")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        clear_messages()
        st.rerun()

    if st.button("Sign out", use_container_width=True):
        st.session_state.role = None
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()

    st.markdown("<p style='color:#1e1e1e;font-size:10px;margin-top:1.5rem'>FastAPI · ChromaDB · Llama 3.3</p>", unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────────
tabs = ["Chat", "System"] if role == "admin" else ["Chat"]
tab_objects = st.tabs(tabs)
tab_chat = tab_objects[0]
tab_system = tab_objects[1] if role == "admin" else None

# ════════ CHAT TAB ════════
with tab_chat:
    # Header
    st.markdown("""
    <div style='padding:1.25rem 0 1rem;border-bottom:1px solid #111;margin-bottom:1rem'>
        <div style='display:flex;align-items:center;gap:8px;margin-bottom:4px'>
            <span style='font-size:1rem'>🛡️</span>
            <span style='color:#e0e0e0;font-size:15px;font-weight:600;letter-spacing:-0.01em'>RAGuard</span>
        </div>
        <p style='color:#333;font-size:12px;margin:0 0 10px'>Smart enough to answer. Smart enough to know when not to.</p>
        <div style='display:flex;gap:6px;flex-wrap:wrap'>
            <span style='font-size:11px;color:#2a2a2a;border:1px solid #161616;padding:2px 8px;border-radius:4px'>Grounded generation</span>
            <span style='font-size:11px;color:#2a2a2a;border:1px solid #161616;padding:2px 8px;border-radius:4px'>Source-cited</span>
            <span style='font-size:11px;color:#2a2a2a;border:1px solid #161616;padding:2px 8px;border-radius:4px'>Injection defense</span>
            <span style='font-size:11px;color:#2a2a2a;border:1px solid #161616;padding:2px 8px;border-radius:4px'>Eval pipeline</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat history
    if not st.session_state.messages:
        st.markdown("""
        <div style='text-align:center;padding:4rem 0;'>
            <div style='font-size:2rem;margin-bottom:0.75rem'>🛡️</div>
            <p style='color:#333;font-size:13px'>Ask anything about RAG, LLMs, or AI engineering</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            avatar = "🛡️" if msg["role"] == "assistant" else None
            with st.chat_message(msg["role"], avatar=avatar):
                st.write(msg["content"])
                if msg["role"] == "assistant":
                    level = conf_level(msg.get("avg_distance"))
                    if level:
                        st.markdown(f'<div class="conf-row"><span class="conf-dot dot-{level}"></span><span class="conf-label">{conf_label(level)}</span></div>', unsafe_allow_html=True)
                    if msg.get("sources"):
                        with st.expander(f"Sources ({len(msg['sources'])})"):
                            for s in msg["sources"]:
                                st.markdown(f"<span style='font-size:12px;color:#555'>• {s}</span>", unsafe_allow_html=True)

    # Input — always at bottom
    typed = st.chat_input("Ask anything about RAG, LLMs, or AI engineering...")
    query = st.session_state.pending_question or typed
    st.session_state.pending_question = None

    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        save_message("user", query)
        with st.chat_message("user", avatar=None):
            st.write(query)

        with st.chat_message("assistant", avatar="🛡️"):
            with st.spinner(""):
                try:
                    resp = requests.post(f"{API_URL}/query", json={"question": query}, timeout=60)
                    data = resp.json()
                    answer    = data["answer"]
                    sources   = data.get("sources", [])
                    distances = data.get("distances", [])
                    avg_dist  = sum(distances) / len(distances) if distances else None

                    st.write(answer)

                    level = conf_level(avg_dist)
                    if level:
                        st.markdown(f'<div class="conf-row"><span class="conf-dot dot-{level}"></span><span class="conf-label">{conf_label(level)}</span></div>', unsafe_allow_html=True)

                    if sources:
                        with st.expander(f"Sources ({len(sources)})"):
                            for s in sources:
                                st.markdown(f"<span style='font-size:12px;color:#555'>• {s}</span>", unsafe_allow_html=True)

                    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources, "avg_distance": avg_dist})
                    save_message("assistant", answer, sources, avg_dist)

                except Exception:
                    st.markdown("<span style='color:#333;font-size:13px'>Connection error — make sure the API is running.</span>", unsafe_allow_html=True)

# ════════ SYSTEM TAB (admin only) ════════
if tab_system:
    with tab_system:
        st.markdown("<p style='color:#555;font-size:11px;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1.5rem'>System Metrics</p>", unsafe_allow_html=True)
        try:
            stats = get_stats()
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Requests", stats["total_requests"])
            c2.metric("Blocked",        stats["total_blocked"])
            c3.metric("Block Rate",     f"{stats['block_rate']*100:.0f}%")
            c4.metric("Avg Grounding",  f"{stats['avg_grounding_score']}/5" if stats["avg_grounding_score"] else "—")

            logs = get_recent_logs(15)
            st.markdown("<p style='color:#555;font-size:11px;text-transform:uppercase;letter-spacing:0.1em;margin:1.5rem 0 0.5rem'>Recent Requests</p>", unsafe_allow_html=True)
            if logs:
                import pandas as pd
                df = pd.DataFrame(logs, columns=["Time", "Query", "Blocked", "Stage", "Grounding", "Distance", "Latency ms"])
                df["Blocked"] = df["Blocked"].map({1: "🔴 Yes", 0: "🟢 No"})
                df["Time"]    = df["Time"].str[:19].str.replace("T", " ")
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.markdown("<p style='color:#333;font-size:13px'>No requests logged yet.</p>", unsafe_allow_html=True)
        except Exception:
            st.markdown("<p style='color:#333;font-size:13px'>Stats unavailable.</p>", unsafe_allow_html=True)
   

