import sqlite3
import json
from services.config import PRODUCT_IDEAS_MIN_REUSABILITY
from services.logger import get_logger

logger = get_logger('PRODUCT_SELECTOR')

def load_product_ideas():
    conn = sqlite3.connect('data/digest.db')
    cur = conn.cursor()

    cur.execute('''
    SELECT i.id, i.title, i.content, e.json
    FROM items i
    JOIN evaluations e ON i.id = e.item_id
    WHERE e.persona = 'PRODUCT_IDEAS'
      AND e.decision = 'keep'
      AND e.score >= ?
    ORDER BY e.score DESC
    ''', (PRODUCT_IDEAS_MIN_REUSABILITY,))

    rows = cur.fetchall()
    conn.close()

    logger.info(f'Loaded {len(rows)} PRODUCT_IDEAS candidates')
    return rows
