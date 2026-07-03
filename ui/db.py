import sqlite3
from datetime import datetime

DB_PATH = "chat_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT,
            sources TEXT,
            avg_distance REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_message(role, content, sources=None, avg_distance=None):
    try:
        conn = sqlite3.connect(DB_PATH)
        init_db()
        sources_str = ",".join(sources) if sources else ""
        conn.execute(
            "INSERT INTO messages (role, content, sources, avg_distance, timestamp) VALUES (?, ?, ?, ?, ?)",
            (role, content, sources_str, avg_distance, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
    except Exception:
        pass

def load_messages():
    try:
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute("SELECT role, content, sources, avg_distance FROM messages ORDER BY id ASC").fetchall()
        conn.close()
        messages = []
        for role, content, sources_str, avg_distance in rows:
            msg = {"role": role, "content": content}
            if sources_str:
                msg["sources"] = sources_str.split(",")
            if avg_distance is not None:
                msg["avg_distance"] = avg_distance
            messages.append(msg)
        return messages
    except Exception:
        return []

def clear_messages():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM messages")
    conn.commit()
    conn.close()