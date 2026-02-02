import httpx
from services.config import OLLAMA_BASE_URL
from services.logger import get_logger

logger = get_logger('EMBEDDINGS')

EMBED_MODEL = 'nomic-embed-text'

def embed_text(text: str) -> list:
    if not text:
        return None

    payload = {
        'model': EMBED_MODEL,
        'input': text
    }

    try:
        response = httpx.post(
            f'{OLLAMA_BASE_URL}/embeddings',
            json=payload,
            timeout=60
        )
        response.raise_for_status()

        return response.json()['data'][0]['embedding']

    except Exception as e:
        logger.error(f'Embedding failed: {e}')
        return None
