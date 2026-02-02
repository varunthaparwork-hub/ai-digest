import sqlite3
from pathlib import Path

DB_PATH = Path('data') / 'digest.db'


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Raw ingested items
    cur.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT,
        url TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # LLM evaluations
    cur.execute('''
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        persona TEXT,
        score REAL,
        decision TEXT,
        json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(item_id) REFERENCES items(id)
    )
    ''')

    # Generated digests
    cur.execute('''
    CREATE TABLE IF NOT EXISTS digests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        persona TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Delivery tracking
    cur.execute('''
    CREATE TABLE IF NOT EXISTS deliveries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        digest_id INTEGER,
        channel TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(digest_id) REFERENCES digests(id)
    )
    ''')

    conn.commit()
    conn.close()


def insert_item(item: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
    INSERT OR IGNORE INTO items (source, title, content, url)
    VALUES (?, ?, ?, ?)
    ''', (
        item['source'],
        item['title'],
        item.get('content'),
        item.get('url')
    ))

    conn.commit()
    conn.close()


def insert_evaluation(item_id: int, persona: str, score: float, decision: str, json_data: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
    INSERT INTO evaluations (item_id, persona, score, decision, json)
    VALUES (?, ?, ?, ?, ?)
    ''', (item_id, persona, score, decision, json_data))

    conn.commit()
    conn.close()


def insert_digest(persona: str, content: str) -> int:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
    INSERT INTO digests (persona, content)
    VALUES (?, ?)
    ''', (persona, content))

    digest_id = cur.lastrowid
    conn.commit()
    conn.close()

    return digest_id
