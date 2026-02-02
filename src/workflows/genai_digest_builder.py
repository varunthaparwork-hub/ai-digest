from workflows.genai_selector import load_genai_news
from services.logger import get_logger

logger = get_logger("GENAI_DIGEST")

def build_digest_markdown() -> str:
    items = load_genai_news()

    lines = []
    lines.append("# 📰 AI News Digest\n")

    for item in items:
        lines.append(f"## {item['title']}")
        lines.append(item['summary'])
        lines.append("")

    digest = "\n".join(lines)
    logger.info("Digest markdown generated")
    return digest
