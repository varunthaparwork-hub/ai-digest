import os
import requests
from services.logger import get_logger
from services.config import TELEGRAM_ENABLED

logger = get_logger("TELEGRAM")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

MAX_LEN = 4000  # safe margin under 4096

def _chunks(text, size):
    for i in range(0, len(text), size):
        yield text[i:i+size]

def send_telegram(text: str):
    if not TELEGRAM_ENABLED:
        return

    if not BOT_TOKEN or not CHAT_ID:
        logger.error("Telegram not configured properly")
        return

    for part in _chunks(text, MAX_LEN):
        payload = {
            "chat_id": CHAT_ID,
            "text": part,
            "parse_mode": "Markdown"
        }

        resp = requests.post(API_URL, json=payload)

        if resp.status_code != 200:
            logger.error(f"Telegram delivery failed: {resp.text}")
            return

    logger.info("Telegram messages sent successfully")
