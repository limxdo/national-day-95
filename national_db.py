#!/usr/bin/env python3

import sqlite3 as sql
import os
from typing import List, Dict, Any

conn = None
cur = None

def creat_db(path: str):
    global conn, cur
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    conn = sql.connect(path, check_same_thread=False)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        text TEXT NOT NULL
    )
    """)
    conn.commit()

def add_user(data: Dict[str, Any]) -> Dict[str, Any]:
    global conn, cur
    if cur is None:
        return {"ok": False, "error": "DB not initialized"}

    name = (data.get("name") or "").strip()
    text = (data.get("text") or "").strip()

    if not name or not text:
        return {"ok": False, "error": "name and text required"}

    cur.execute("SELECT 1 FROM messages WHERE text = ?", (text,))
    if cur.fetchone():
        return {"ok": False, "error": "duplicate"}

    cur.execute("INSERT INTO messages (name, text) VALUES (?, ?)", (name, text))
    conn.commit()
    return {"ok": True}

def pop_messages(limit: int = 200) -> List[Dict[str, Any]]:
    global conn, cur
    if cur is None:
        return []

    cur.execute("BEGIN")
    cur.execute("SELECT id, name, text FROM messages ORDER BY id ASC LIMIT ?", (limit,))
    rows = cur.fetchall()
    ids = [r[0] for r in rows]
    if ids:
        q = ",".join("?" for _ in ids)
        cur.execute(f"DELETE FROM messages WHERE id IN ({q})", ids)
    conn.commit()

    return [{"id": r[0], "name": r[1], "text": r[2]} for r in rows]
