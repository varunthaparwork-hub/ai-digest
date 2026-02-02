from services.llm import ask_llm
from services.logger import get_logger

logger = get_logger('GENAI_SUMMARY')

PROMPT = '''
You are generating content for a DAILY TECH DIGEST.

STRICT OUTPUT RULES (must follow):
- Output ONLY the summary text
- Do NOT include introductions, explanations, or labels
- Do NOT say things like \"here is\", \"summary\", or \"below\"
- No markdown, no headings, no bullets
- 3 to 5 short lines
- Technical, factual tone
- Explain why it matters

Title:
\"\"\"{title}\"\"\"

Context:
\"\"\"{content}\"\"\"
'''

def _clean_summary(text: str) -> str:
    if not text:
        return ''

    lines = text.strip().splitlines()

    # Remove common LLM intro lines
    banned_prefixes = (
        'here is',
        'here’s',
        'here is a',
        'here is the',
        'summary',
    )

    cleaned = []
    for line in lines:
        l = line.strip()
        if l.lower().startswith(banned_prefixes):
            continue
        cleaned.append(l)

    return '\\n'.join(cleaned).strip()

def summarize_item(title: str, content: str) -> str:
    response = ask_llm(PROMPT.format(title=title, content=content))
    return _clean_summary(response)
