from dotenv import load_dotenv
import os

load_dotenv()

def get_env(key: str, default=None):
    value = os.getenv(key, default)
    if value is None:
        raise RuntimeError(f'Missing required env var: {key}')
    return value

# Persona toggles
PERSONA_GENAI_NEWS_ENABLED = get_env('PERSONA_GENAI_NEWS_ENABLED') == 'true'
PERSONA_PRODUCT_IDEAS_ENABLED = get_env('PERSONA_PRODUCT_IDEAS_ENABLED') == 'true'

# LLM configuration
OLLAMA_BASE_URL = get_env('OLLAMA_BASE_URL')
OLLAMA_MODEL = get_env('OLLAMA_MODEL')

# Thresholds
GENAI_NEWS_MIN_RELEVANCE = float(get_env('GENAI_NEWS_MIN_RELEVANCE'))
PRODUCT_IDEAS_MIN_REUSABILITY = float(get_env('PRODUCT_IDEAS_MIN_REUSABILITY'))

# Delivery toggles
EMAIL_ENABLED = get_env('EMAIL_ENABLED') == 'true'
TELEGRAM_ENABLED = get_env('TELEGRAM_ENABLED') == 'true'

# Telegram configuration
TELEGRAM_ENABLED = get_env('TELEGRAM_ENABLED') == 'true'
TELEGRAM_BOT_TOKEN = get_env('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = get_env('TELEGRAM_CHAT_ID')
