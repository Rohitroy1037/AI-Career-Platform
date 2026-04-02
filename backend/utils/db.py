import sqlite3

def init_db():
    conn = sqlite3.connect("memory.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        question TEXT,
        response TEXT
    )
    """)

    conn.commit()
    conn.close()