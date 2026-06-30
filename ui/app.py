import streamlit as st
import requests
from db import init_db, save_message, load_messages, clear_messages

st.set_page_config(page_title="RAGuard", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

init_db()

if "messages" not in st.session_state:
    st.session_state.messages = load_messages()
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stApp {
    background: radial-gradient(circle at 20% 0%, #1a2740 0%, #0a0e14 55%);
}

[data-testid="stSidebar"] {
    background-color: #11151c;
    border-right: 1px solid #232a36;
}

.block-container {
    padding-top: 2rem;
    max-width: 820px;
    margin: 0 auto;
}

.hero-card {
    background: linear-gradient(135deg, #161d2b, #0f1420);
    border: 1px solid #2a3650;
    border-radius: 20px;
    padding: 1.8rem 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
    box-shadow: 0 0 40px rgba(79, 139, 249, 0.08);
}

.hero-title {
    font-size: 2.5rem;
    font-weight: 900;
    background: linear-gradient(90deg, #4F8BF9, #A855F7, #EC4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.hero-tagline {
    color: #9AA4B2;
    font-size: 1rem;
    margin-top: 0.4rem;
}

.badge-row {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 1rem;
    flex-wrap: wrap;
}

.badge {
    background: #1c2333;
    border: 1px solid #2e3a52;
    color: #8AB4F8;
    font-size: 0.78rem;
    padding: 5px 12px;
    border-radius: 20px;
}

.confidence-pill {
    display: inline-block;
    font-size: 0.72rem;
    padding: 2px 10px;
    border-radius: 12px;
    margin-top: 8px;
    font-weight: 600;
}

.conf-high { background: #0F3D2A; color: #4ADE80; }
.conf-med { background: #3D330F; color: #FACC15; }
.conf-low { background: #3D1A1A; color: #F87171; }

div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
    background: linear-gradient(135deg, #1e2a4a, #161d33);
    border: 1px solid #2e3f66;
    border-radius: 16px;
    padding: 0.75rem 1.1rem;
}

div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
    background: #161a24;
    border: 1px solid #262d3d;
    border-radius: 16px;
    padding: 0.75rem 1.1rem;
}

[data-testid="stChatInput"] {
    border-radius: 14px;
}

.streamlit-expanderHeader {
    font-size: 0.85rem;
    color: #A855F7;
}

div[data-testid="stSidebar"] button {
    text-align: left;
    background: #1a1f2b;
    border: 1px solid #262d3d;
    color: #c9d1d9;
    border-radius: 10px;
}

div[data-testid="stSidebar"] button:hover {
    border-color: #4F8BF9;
    color: #4F8BF9;
}
</style>
""", unsafe_allow_html=True)

def confidence_label(distance):
    if distance < 0.8:
        return "High confidence", "conf-high"
    elif distance < 1.4:
        return "Medium confidence", "conf-med"
    else:
        return "Low confidence", "conf-low"

with st.sidebar:
    st.markdown("### 🛡️ RAGuard")
    st.markdown("A retrieval-augmented AI assistant that only answers from real source documents — and says so when it doesn't know.")
    st.markdown("---")
    st.markdown("**Try asking:**")

    for q in ["What is overfitting?", "What does precision mean?", "Explain KNN in simple terms", "What is the capital of France?"]:
        if st.button(q, use_container_width=True, key=f"ex_{q}"):
            st.session_state.pending_question = q

    st.markdown("---")
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        clear_messages()
        st.rerun()

    st.markdown("---")
    st.caption("Built with FastAPI, ChromaDB, and Llama 3.3")

st.markdown("""
<div class="hero-card">
    <div class="hero-title">🛡️ RAGuard</div>
    <div class="hero-tagline">Smart enough to answer. Smart enough to know when not to.</div>
    <div class="badge-row">
        <span class="badge">Grounded generation</span>
        <span class="badge">Source-cited</span>
        <span class="badge">Refuses unknowns</span>
    </div>
</div>
""", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🛡️"):
        st.write(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            if msg.get("avg_distance") is not None:
                label, css_class = confidence_label(msg["avg_distance"])
                st.markdown(f'<span class="confidence-pill {css_class}">{label}</span>', unsafe_allow_html=True)
            with st.expander("📄 Sources"):
                for s in msg["sources"]:
                    st.write(f"• {s}")

typed_input = st.chat_input("Ask a question about the documents...")
query_to_run = st.session_state.pending_question or typed_input
st.session_state.pending_question = None

if query_to_run:
    st.session_state.messages.append({"role": "user", "content": query_to_run})
    save_message("user", query_to_run)
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(query_to_run)

    with st.chat_message("assistant", avatar="🛡️"):
        with st.spinner("Thinking..."):
            response = requests.post("http://127.0.0.1:8000/query", json={"question": query_to_run})
            data = response.json()
            st.write(data["answer"])

            avg_distance = None
            if "distances" in data and data["distances"]:
                avg_distance = sum(data["distances"]) / len(data["distances"])
                label, css_class = confidence_label(avg_distance)
                st.markdown(f'<span class="confidence-pill {css_class}">{label}</span>', unsafe_allow_html=True)

            with st.expander("📄 Sources"):
                for s in data["sources"]:
                    st.write(f"• {s}")

    st.session_state.messages.append({
        "role": "assistant", "content": data["answer"],
        "sources": data["sources"], "avg_distance": avg_distance
    })
    save_message("assistant", data["answer"], data["sources"], avg_distance)