import sqlite3
from typing import List, Dict

DB_PATH = "cyberbullying.db"

# Ensure the table exists
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                message TEXT,
                timestamp TEXT,
                risk_score REAL
            )
        """)
        conn.commit()

def log_message(user_id: str, message: str, timestamp: str, risk_score: float):
    # Each call uses its own connection + cursor
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO logs (user_id, message, timestamp, risk_score)
            VALUES (?, ?, ?, ?)
        """, (user_id, message, timestamp, float(risk_score)))
        conn.commit()

def fetch_flagged_messages(limit: int = 200, min_risk: float = 0.0) -> List[Dict]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("""
            SELECT user_id, message, timestamp, risk_score
            FROM logs
            WHERE risk_score >= ?
            ORDER BY id DESC
            LIMIT ?
        """, (min_risk, limit))
        rows = cursor.fetchall()
        return [
            {"user_id": r[0], "message": r[1], "timestamp": r[2], "risk_score": float(r[3])}
            for r in rows
        ]

# Initialize once
init_db()
