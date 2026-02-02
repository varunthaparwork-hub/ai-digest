from services.embeddings import embed_text

vec = embed_text('FAISS is used for vector similarity search')

print('Vector length:', len(vec))
print('First 5 values:', vec[:5])
