from backend.utils.db import get_connection


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
    SELECT question, response FROM chat_memory
    WHERE user_id = ?
    ORDER BY id DESC
    LIMIT 5
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [{"question": r[0], "response": r[1]} for r in rows]