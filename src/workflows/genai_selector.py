from services.config import GENAI_NEWS_MIN_RELEVANCE
from services.logger import get_logger
import sqlite3
import json

logger = get_logger("GENAI_SELECTOR")

def _load_genai_news_internal():
    conn = sqlite3.connect('data/digest.db')
    cur = conn.cursor()

    cur.execute("""
    SELECT i.title, e.json
    FROM items i
    JOIN evaluations e ON i.id = e.item_id
    WHERE e.persona = 'GENAI_NEWS'
      AND e.decision = 'keep'
      AND e.score >= ?
    ORDER BY e.score DESC
    """, (GENAI_NEWS_MIN_RELEVANCE,))

    rows = cur.fetchall()
    conn.close()

    results = []
    for title, eval_json in rows:
        data = json.loads(eval_json)
        results.append({
            "title": title,
            "summary": data.get("why_it_matters", "")
        })

    logger.info(f"Loaded {len(results)} relevant GENAI_NEWS items")
    return results


# ✅ PUBLIC, STABLE API (this fixes your error)
def load_genai_news():
    return _load_genai_news_internal()
