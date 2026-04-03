import sqlite3
import os
import tempfile

# Vercel filesystem is read-only except /tmp
DB_PATH = os.path.join(tempfile.gettempdir(), "memory.db")

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            question TEXT,
            response TEXT
        )""")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[db] init_db warning: {e}")
