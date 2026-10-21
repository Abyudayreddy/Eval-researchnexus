import sys
import os
sys.path.insert(0, os.path.abspath('backend'))
import app.services.retrieval as ret

print("=== RUNNING BM25 RETRIEVAL TEST ===")
bm25_matches = ret.query_bm25_all('Deep Learning', n_results=5)
print("BM25 matches found:", len(bm25_matches))
for idx, m in enumerate(bm25_matches[:3]):
    print(f"  Match {idx+1}: {m['chunk_id']} | Score: {m.get('bm25_score'):.4f}")

print("\n=== RUNNING RECIPROCAL RANK FUSION (k=60) ===")
rrf = ret.reciprocal_rank_fusion(bm25_matches, bm25_matches, k=60)
print("RRF fused candidates:", len(rrf))
if rrf:
    print("  Top candidate chunk_id:", rrf[0].get('chunk_id'))
    print("  Top candidate RRF score:", rrf[0].get('rrf_score'))

print("\n=== RUNNING BGE CROSS-ENCODER RERANKING ===")
rerank = ret.rerank_with_bge('deep learning architectures', rrf[:3])
print("Reranked candidate count:", len(rerank))
if rerank:
    print("  Top reranked chunk_id:", rerank[0].get('chunk_id'))
    print("  Top reranked rerank_score:", rerank[0].get('rerank_score'))
    print("  Reranker model type:", type(ret.get_reranker()).__name__)
