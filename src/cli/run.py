from services.storage import init_db, insert_item, insert_digest
from tools.hn_adapter import HackerNewsAdapter
from services.logger import get_logger
from services.embeddings import embed_text
from services.vector_store import is_duplicate, add_vector
from workflows.genai_digest_builder import build_digest_markdown
from workflows.product_ideas_builder import build_product_ideas_markdown
from workflows.refined_opportunities_builder import build_refined_opportunities_markdown
from services.telegramer import send_telegram
import sqlite3

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

        cur.execute("SELECT id FROM items WHERE url = ?", (item.get("url"),))
        row = cur.fetchone()

        if row:
            add_vector(vector, row[0])
            inserted += 1

    conn.close()

    # -------- GENAI NEWS DIGEST --------
    genai_digest = build_digest_markdown()
    with open("data/genai_daily_digest.md", "w", encoding="utf-8") as f:
        f.write(genai_digest)

    insert_digest("GENAI_NEWS", genai_digest)

    send_telegram("📰 *AI NEWS DIGEST*\n\n" + genai_digest)

    # -------- PRODUCT IDEAS DIGEST --------
    product_digest = build_product_ideas_markdown()
    with open("data/product_ideas_digest.md", "w", encoding="utf-8") as f:
        f.write(product_digest)

    insert_digest("PRODUCT_IDEAS", product_digest)

    send_telegram("💡 *PRODUCT IDEAS*\n\n" + product_digest)

    # -------- REFINED OPPORTUNITIES (OPTIONAL) --------
    refined = build_refined_opportunities_markdown()
    with open("data/refined_product_opportunities.md", "w", encoding="utf-8") as f:
        f.write(refined)

    send_telegram("🚀 *REFINED OPPORTUNITIES*\n\n" + refined)

    logger.info(f"Inserted {inserted} new items")
    logger.info(f"Skipped {skipped} duplicates")
    logger.info("Daily digests sent to Telegram successfully")

if __name__ == "__main__":
    main()
