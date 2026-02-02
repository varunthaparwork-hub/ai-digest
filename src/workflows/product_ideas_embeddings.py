import json
import numpy as np
from services.embeddings import embed_text
from workflows.product_ideas_selector import load_product_ideas
from services.logger import get_logger

logger = get_logger('PRODUCT_IDEA_EMBED')

def embed_product_ideas():
    ideas = load_product_ideas()
    vectors = []
    meta = []

    for _, _, _, eval_json in ideas:
        data = json.loads(eval_json)
        text = f"{data.get('problem_statement', '')} {data.get('solution_summary', '')}"

        vec = embed_text(text)
        if vec:
            vectors.append(vec)
            meta.append(data)

    logger.info(f'Embedded {len(vectors)} product ideas')
    return np.array(vectors).astype('float32'), meta
