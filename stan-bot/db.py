import sqlite3
import json
from datetime import datetime

DB_FILE = "chatbot.sqlite"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS profiles (
        user_id TEXT PRIMARY KEY,
        profile_json TEXT,
        updated_at TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS chat_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        message TEXT,
        memory_json TEXT,
        created_at TEXT
    )""")
    conn.commit()
    conn.close()

def fetch_user_profile(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT profile_json FROM profiles WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return json.loads(row[0]) if row else {}

def upsert_user_profile(user_id, changes):
    existing = fetch_user_profile(user_id)
    existing.update(changes)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO profiles (user_id, profile_json, updated_at) VALUES (?, ?, ?)",
              (user_id, json.dumps(existing), datetime.now().isoformat()))
    conn.commit()
    conn.close()

def fetch_recent_memory(user_id, limit=6):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT message, memory_json FROM chat_memory WHERE user_id=? ORDER BY created_at DESC LIMIT ?", (user_id, limit))
    rows = c.fetchall()
    conn.close()
    messages, summaries = [], []
    for m, mj in rows:
        messages.append(m)
        try:
            mem = json.loads(mj) if mj else {}
            if "summary" in mem:
                summaries.append(mem["summary"])
        except Exception:
            pass
    return messages[::-1], summaries[::-1]

def store_chat_memory(user_id, message, memory_json):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO chat_memory (user_id, message, memory_json, created_at) VALUES (?, ?, ?, ?)",
              (user_id, message, json.dumps(memory_json), datetime.now().isoformat()))
    conn.commit()
    conn.close()
