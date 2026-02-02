import faiss
from collections import defaultdict
from workflows.product_ideas_embeddings import embed_product_ideas
from services.logger import get_logger

logger = get_logger('PRODUCT_CLUSTER')

def cluster_product_ideas(k=5):
    vectors, meta = embed_product_ideas()

    if len(vectors) == 0:
        logger.warning('No vectors to cluster')
        return {}

    dim = vectors.shape[1]

    # Adjust k if fewer ideas than clusters
    k = min(k, len(vectors))

    # Proper FAISS KMeans
    kmeans = faiss.Kmeans(d=dim, k=k, niter=20, verbose=False)
    kmeans.train(vectors)

    # Assign each vector to a centroid
    _, labels = kmeans.index.search(vectors, 1)

    clusters = defaultdict(list)
    for label, idea in zip(labels.flatten(), meta):
        clusters[int(label)].append(idea)

    logger.info(f'Clustered ideas into {len(clusters)} groups')
    return clusters
