import faiss
import pickle
from pathlib import Path
import numpy as np
from services.logger import get_logger

logger = get_logger('FAISS')

VECTOR_DIM = 768  # MATCHES nomic-embed-text
FAISS_DIR = Path('data') / 'faiss'
INDEX_FILE = FAISS_DIR / 'index.bin'
META_FILE = FAISS_DIR / 'meta.pkl'

FAISS_DIR.mkdir(parents=True, exist_ok=True)

def _load_index():
    if INDEX_FILE.exists():
        logger.info('Loading existing FAISS index')
        return faiss.read_index(str(INDEX_FILE))
    logger.info('Creating new FAISS index')
    return faiss.IndexFlatL2(VECTOR_DIM)

def _load_meta():
    if META_FILE.exists():
        with open(META_FILE, 'rb') as f:
            return pickle.load(f)
    return []

index = _load_index()
metadata = _load_meta()

def save():
    faiss.write_index(index, str(INDEX_FILE))
    with open(META_FILE, 'wb') as f:
        pickle.dump(metadata, f)

def add_vector(vector: list, item_id: int):
    vec = np.array([vector]).astype('float32')
    index.add(vec)
    metadata.append(item_id)
    save()

def is_duplicate(vector: list, threshold: float = 0.85) -> bool:
    if index.ntotal == 0:
        return False

    vec = np.array([vector]).astype('float32')
    distances, _ = index.search(vec, 1)

    return distances[0][0] < threshold
