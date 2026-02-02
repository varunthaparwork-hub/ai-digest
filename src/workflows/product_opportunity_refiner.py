import json
import re
from services.llm import ask_llm
from services.logger import get_logger

logger = get_logger('OPPORTUNITY_REFINER')

PROMPT = '''
You are a startup analyst.

Given a group of related product ideas, synthesize ONE clear product opportunity.

Return ONLY valid JSON in this exact format:
{{
  "opportunity_name": "",
  "core_problem": "",
  "target_users": "",
  "why_now": "",
  "mvp_direction": ""
}}

Ideas:
\"\"\"{ideas}\"\"\"
'''

def _extract_json(text: str):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return match.group(0) if match else None

def refine_opportunity(ideas: list) -> dict:
    ideas_text = '\n'.join(f"- {i}" for i in ideas)
    response = ask_llm(PROMPT.format(ideas=ideas_text))

    if not response:
        return None

    json_text = _extract_json(response)
    if not json_text:
        logger.error('No JSON found in opportunity refinement')
        return None

    try:
        return json.loads(json_text)
    except Exception as e:
        logger.error(f'Opportunity JSON parse failed: {e}')
        return None
