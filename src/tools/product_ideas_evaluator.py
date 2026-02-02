import json
import re
from services.llm import ask_llm
from services.logger import get_logger

logger = get_logger('PRODUCT_EVAL')

PROMPT_TEMPLATE = '''
You are evaluating a product idea from a startup or indie builder perspective.

Return ONLY valid JSON in this exact format:
{{
  "idea_type": "",
  "problem_statement": "",
  "solution_summary": "",
  "maturity_level": "",
  "reusability_score": 0.0,
  "decision": "keep" or "drop"
}}

Input text:
\"\"\"{text}\"\"\"
'''

def _extract_json(text: str) -> str:
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return match.group(0) if match else None

def evaluate_idea(text: str) -> dict:
    response = ask_llm(PROMPT_TEMPLATE.format(text=text))
    if not response:
        return None

    json_text = _extract_json(response)
    if not json_text:
        logger.error('No JSON found in PRODUCT_IDEAS output')
        return None

    try:
        return json.loads(json_text)
    except Exception as e:
        logger.error(f'PRODUCT_IDEAS JSON parse failed: {e}')
        return None
