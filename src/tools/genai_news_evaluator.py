import json
import re
from services.llm import ask_llm
from services.logger import get_logger

logger = get_logger('GENAI_EVAL')

PROMPT_TEMPLATE = '''
You are evaluating a technology news item.

Return ONLY valid JSON in this exact format:
{{
  "relevance_score": 0.0,
  "topic": "",
  "why_it_matters": "",
  "target_audience": "",
  "decision": "keep" or "drop"
}}

News item title:
\"\"\"{title}\"\"\"
'''

def _extract_json(text: str) -> str:
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return match.group(0) if match else None

def evaluate_item(item: dict) -> dict:
    prompt = PROMPT_TEMPLATE.format(title=item['title'])

    response = ask_llm(prompt)
    if not response:
        logger.error('Empty response from LLM')
        return None

    json_text = _extract_json(response)
    if not json_text:
        logger.error(f'No JSON found in LLM output: {response}')
        return None

    try:
        return json.loads(json_text)
    except Exception as e:
        logger.error(f'JSON parse failed: {e}')
        logger.error(f'Raw JSON text: {json_text}')
        return None
