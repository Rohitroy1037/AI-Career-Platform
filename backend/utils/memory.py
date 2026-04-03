import sqlite3
import os
import tempfile

DB_PATH = os.path.join(tempfile.gettempdir(), "memory.db")

def save_memory(user_id, question, response):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO chat_memory (user_id, question, response) VALUES (?, ?, ?)",
            (user_id, question, response)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[memory] save error: {e}")

def get_memory(user_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute(
            "SELECT question, response FROM chat_memory WHERE user_id=? ORDER BY id DESC LIMIT 5",
            (user_id,)
        ).fetchall()
        conn.close()
        return [{"question": r[0], "response": r[1]} for r in rows]
    except Exception:
        return []
