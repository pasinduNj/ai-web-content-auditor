import sqlite3
import json

DB_NAME = "cache.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            url TEXT PRIMARY KEY,
            data TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_cache(url, data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO results (url, data) VALUES (?, ?)",
        (url, json.dumps(data))
    )
    conn.commit()
    conn.close()

def get_cached_result(url):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT data FROM results WHERE url = ?", (url,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None