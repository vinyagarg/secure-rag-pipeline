import sqlite3
import json
from datetime import datetime

DB_PATH = "audit_log.db"

def init_audit_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            query TEXT,
            blocked INTEGER,
            blocked_stage TEXT,
            blocked_reason TEXT,
            answer TEXT,
            sources TEXT,
            grounding_score INTEGER,
            is_grounded INTEGER,
            avg_distance REAL,
            latency_ms REAL
        )
    """)
    conn.commit()
    conn.close()

def log_request(query, result, latency_ms):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO audit_log (
            timestamp, query, blocked, blocked_stage, blocked_reason,
            answer, sources, grounding_score, is_grounded, avg_distance, latency_ms
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        query,
        1 if result.get("blocked") else 0,
        result.get("blocked_stage"),
        result.get("blocked_reason"),
        result.get("answer"),
        json.dumps(result.get("sources", [])),
        result.get("grounding_score"),
        1 if result.get("is_grounded") else 0,
        sum(result.get("distances", [])) / len(result["distances"]) if result.get("distances") else None,
        latency_ms
    ))
    conn.commit()
    conn.close()

def get_recent_logs(limit=20):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT timestamp, query, blocked, blocked_stage,
               grounding_score, avg_distance, latency_ms
        FROM audit_log
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return rows

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    stats = conn.execute("""
        SELECT
            COUNT(*) as total_requests,
            SUM(blocked) as total_blocked,
            AVG(CASE WHEN blocked=0 THEN grounding_score END) as avg_grounding,
            AVG(CASE WHEN blocked=0 THEN latency_ms END) as avg_latency_ms
        FROM audit_log
    """).fetchone()
    conn.close()
    return {
        "total_requests": stats[0],
        "total_blocked": stats[1],
        "block_rate": round(stats[1]/stats[0], 3) if stats[0] else 0,
        "avg_grounding_score": round(stats[2], 2) if stats[2] else None,
        "avg_latency_ms": round(stats[3], 2) if stats[3] else None
    }

if __name__ == "__main__":
    init_audit_db()
    print("Audit log database initialized.")
    print(f"Stats: {get_stats()}")