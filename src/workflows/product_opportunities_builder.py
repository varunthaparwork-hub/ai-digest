from workflows.product_ideas_clusterer import cluster_product_ideas
from services.logger import get_logger

logger = get_logger('OPPORTUNITY_BUILDER')

def build_opportunities_markdown() -> str:
    clusters = cluster_product_ideas(k=5)

    lines = []
    lines.append('# 🚀 Product Opportunities\n')

    for idx, ideas in clusters.items():
        lines.append(f'## Opportunity {idx + 1}\n')

        core_problem = ideas[0].get('problem_statement', '')
        lines.append(f'**Core Problem:** {core_problem}\n')
        lines.append('**Candidate Ideas:**')

        for idea in ideas:
            lines.append(f"- {idea.get('solution_summary', '')}")

        lines.append('')

    md = '\n'.join(lines)
    logger.info('Opportunity markdown generated')
    return md
