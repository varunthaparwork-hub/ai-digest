import httpx
from services.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from services.logger import get_logger

logger = get_logger('LLM')

def ask_llm(prompt: str) -> str:
    payload = {
        'model': OLLAMA_MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.1
    }

    try:
        response = httpx.post(
            f'{OLLAMA_BASE_URL}/chat/completions',
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

    except Exception as e:
        logger.error(f'LLM call failed: {e}')
        return ''
