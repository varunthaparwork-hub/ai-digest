from workflows.product_ideas_clusterer import cluster_product_ideas
from workflows.product_opportunity_refiner import refine_opportunity
from services.logger import get_logger

logger = get_logger('REFINED_OPPORTUNITIES')

def build_refined_opportunities_markdown() -> str:
    clusters = cluster_product_ideas(k=5)

    lines = []
    lines.append('# 🚀 Refined Product Opportunities\n')

    for idx, ideas in clusters.items():
        summaries = [i.get('solution_summary', '') for i in ideas]
        refined = refine_opportunity(summaries)

        if not refined:
            continue

        lines.append(f"## {refined.get('opportunity_name','Opportunity')}\n")
        lines.append(f"**Core Problem:** {refined.get('core_problem','')}")
        lines.append(f"**Target Users:** {refined.get('target_users','')}")
        lines.append(f"**Why Now:** {refined.get('why_now','')}")
        lines.append(f"**MVP Direction:** {refined.get('mvp_direction','')}")
        lines.append('')

    md = '\n'.join(lines)
    logger.info('Refined opportunities markdown generated')
    return md
