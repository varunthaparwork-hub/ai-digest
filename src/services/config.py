import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# PERSONA TOGGLES
# =========================
PERSONA_GENAI_NEWS_ENABLED = os.getenv("PERSONA_GENAI_NEWS_ENABLED", "false").lower() == "true"
PERSONA_PRODUCT_IDEAS_ENABLED = os.getenv("PERSONA_PRODUCT_IDEAS_ENABLED", "false").lower() == "true"

# =========================
# LLM CONFIG
# =========================
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

# =========================
# THRESHOLDS
# =========================
GENAI_NEWS_MIN_RELEVANCE = float(os.getenv("GENAI_NEWS_MIN_RELEVANCE", "0.5"))
PRODUCT_IDEAS_MIN_REUSABILITY = float(os.getenv("PRODUCT_IDEAS_MIN_REUSABILITY", "0.5"))

# =========================
# SUMMARY LENGTH CONTROL
# =========================
GENAI_SUMMARY_MODE = os.getenv("GENAI_SUMMARY_MODE", "LONG").upper()

SUMMARY_WORD_LIMITS = {
    "SHORT": 40,
    "MEDIUM": 80,
    "LONG": 200,
}

GENAI_SUMMARY_MAX_WORDS = SUMMARY_WORD_LIMITS.get(
    GENAI_SUMMARY_MODE,
    200
)

# =========================
# TELEGRAM
# =========================
TELEGRAM_ENABLED = os.getenv("TELEGRAM_ENABLED", "false").lower() == "true"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
