import sqlite3
import json
from services.config import GENAI_SUMMARY_MAX_WORDS


def _limit_words(text: str, max_words: int) -> str:
    if not text:
        return "Not available."

    words = text.split()
    if len(words) <= max_words:
        return text.strip()

    return " ".join(words[:max_words]).strip() + "..."


def build_digest_items():
    """
    Build GENAI digest messages from SQLite.
    Evaluation details are stored inside evaluations.json.
    """
    conn = sqlite3.connect("data/digest.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT
            i.id,
            i.title,
            i.url,
            e.score,
            e.json
        FROM items i
        JOIN evaluations e ON i.id = e.item_id
        WHERE e.decision = 'keep'
          AND e.persona = 'GENAI_NEWS'
        ORDER BY e.score DESC
    """)

    rows = cur.fetchall()
    conn.close()

    messages = []

    for row in rows:
        title = row["title"]
        rating = row["score"]
        url = row["url"] or f"https://news.ycombinator.com/item?id={row['id']}"

        # Parse evaluation JSON safely
        try:
            payload = json.loads(row["json"])
        except Exception:
            payload = {}

        description = payload.get("why_it_matters") or payload.get("summary") or "Not available."
        summary = _limit_words(description, GENAI_SUMMARY_MAX_WORDS)

        message = (
            f"⭐ Rating: {rating}\n"
            f"📰 Source: Hacker News\n"
            f"📝 Title: {title}\n\n"
            f"📄 Description:\n"
            f"{description}\n\n"
            f"🧠 Summary:\n"
            f"{summary}\n\n"
            f"🔗 Link:\n"
            f"{url}"
        )

        messages.append(message)

    return messages
