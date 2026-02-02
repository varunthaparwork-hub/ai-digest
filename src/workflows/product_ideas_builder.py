import json
from collections import defaultdict
from workflows.product_ideas_selector import load_product_ideas
from services.logger import get_logger

logger = get_logger('PRODUCT_IDEA_BUILDER')

# Canonical idea type mapping
TYPE_MAP = {
    'product': 'Product',
    'software': 'Product',
    'tool': 'Tooling',
    'tooling': 'Tooling',
    'library': 'Tooling',
    'chrome extension': 'Tooling',
    'developer tool': 'Tooling',
    'research paper': 'Research',
    'news-based product idea': 'Product',
    'ai-powered job automation': 'AI Product',
    'data breach alert': 'Security',
    'security': 'Security',
    'market trend analysis': 'Analytics',
    'mathematics': 'Research',
    'retro gaming': 'Gaming'
}

def _normalize_type(raw_type: str) -> str:
    if not raw_type:
        return 'Misc'

    key = raw_type.strip().lower()
    return TYPE_MAP.get(key, raw_type.title())

def build_product_ideas_markdown() -> str:
    ideas = load_product_ideas()
    grouped = defaultdict(list)

    for _, _, _, eval_json in ideas:
        data = json.loads(eval_json)
        raw_type = data.get('idea_type', 'Misc')
        idea_type = _normalize_type(raw_type)

        grouped[idea_type].append(data)

    lines = []
    lines.append('# 💡 Product Ideas Digest\n')

    for idea_type, entries in grouped.items():
        lines.append(f'## {idea_type}\n')

        for i, idea in enumerate(entries, 1):
            lines.append(f'### Idea {i}')
            lines.append(f'**Problem:** {idea.get("problem_statement", "")}')
            lines.append(f'**Solution:** {idea.get("solution_summary", "")}')
            lines.append(f'**Maturity:** {idea.get("maturity_level", "")}')
            lines.append(f'**Reusability Score:** {idea.get("reusability_score", "")}')
            lines.append('')

    digest = '\n'.join(lines)
    logger.info('Normalized product ideas markdown generated')
    return digest
