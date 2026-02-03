import sqlite3

from services.storage import init_db, insert_item
from services.logger import get_logger
from services.embeddings import embed_text
from services.vector_store import is_duplicate, add_vector
from services.telegramer import send_telegram

from tools.hn_adapter import HackerNewsAdapter
from workflows.genai_digest_builder import build_digest_items

logger = get_logger("Runner")


def main():
    init_db()

    adapter = HackerNewsAdapter()
    items = adapter.fetch_items()

    conn = sqlite3.connect("data/digest.db")
    cur = conn.cursor()

    inserted = 0
    skipped = 0

    for item in items:
        text = f"{item['title']} {item.get('content', '')}"
        vector = embed_text(text)

        if not vector:
            continue

        if is_duplicate(vector):
            skipped += 1
            continue

        insert_item(item)

        cur.execute(
            "SELECT id FROM items WHERE url = ?",
            (item.get("url"),)
        )
        row = cur.fetchone()

        if row:
            add_vector(vector, row[0])
            inserted += 1

    conn.close()

    # =========================
    # GENAI NEWS → TELEGRAM
    # =========================
    messages = build_digest_items()

    for msg in messages:
        send_telegram(msg)

    logger.info(f"Inserted {inserted} new items")
    logger.info(f"Skipped {skipped} duplicates")
    logger.info("Telegram messages sent successfully")


if __name__ == "__main__":
    main()
