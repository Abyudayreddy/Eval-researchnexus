import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import sys
sys.path.insert(0, os.path.abspath('backend'))
from app.db.session import get_chroma_client
from sentence_transformers import SentenceTransformer, CrossEncoder

print("=== 1. TESTING CHROMADB & EMBEDDINGS ===")
client = get_chroma_client()
coll = client.get_collection('papers')
print("Chroma collection 'papers' count:", coll.count())

embedder = SentenceTransformer('BAAI/bge-base-en-v1.5')
vec = embedder.encode(['continual learning in neural networks']).tolist()
print("Embedding generated, dimension:", len(vec[0]))

res = coll.query(query_embeddings=vec, n_results=5)
print("Dense query successful! Retrieved chunk IDs:", res['ids'][0])

print("\n=== 2. TESTING CROSS-ENCODER ===")
reranker = CrossEncoder('BAAI/bge-reranker-base')
pairs = [['continual learning', 'A paper on catastrophic forgetting in neural architectures']]
scores = reranker.predict(pairs)
print("Genuine BGE CrossEncoder score:", scores)
