import sqlite3
from backend.utils.db import get_connection

def create_memory_table():
    conn = get_connection()
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


def save_memory(user_id, question, response):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO chat_memory (user_id, question, response)
    VALUES (?, ?, ?)
    """, (user_id, question, response))

    conn.commit()
    conn.close()


def get_memory(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT question, response
    FROM chat_memory
    WHERE user_id=?
    ORDER BY id DESC
    LIMIT 5
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [{"question":r[0], "response":r[1]} for r in rows]