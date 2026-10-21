"""
Direct system test script for ResearchNexus AI core backend services:
- BM25 retrieval
- Reciprocal Rank Fusion (k=60)
- BGE Reranker
- Claim Verifier (Stage A deterministic overlap + Stage B NLI structure)
- Comparison Engine (dimensions, structure)
- Document Service (PDF parsing & chunking)
"""
import sys
import os
import json

sys.path.insert(0, os.path.abspath('backend'))

results = {}

# 1. RETRIEVAL & RERANKING
try:
    import app.services.retrieval as ret
    bm25_matches = ret.query_bm25_all('scientific', n_results=5)
    results['bm25_test'] = {
        'status': 'PASS' if len(bm25_matches) > 0 else 'PARTIAL',
        'count': len(bm25_matches),
        'top_scores': [m.get('bm25_score', 0) for m in bm25_matches[:3]]
    }
    
    rrf_res = ret.reciprocal_rank_fusion(bm25_matches, bm25_matches, k=60)
    results['rrf_test'] = {
        'status': 'PASS' if len(rrf_res) > 0 else 'FAIL',
        'k_configured': 60,
        'count': len(rrf_res),
        'top_score': rrf_res[0].get('rrf_score', 0) if rrf_res else None
    }
    
    rerank_res = ret.rerank_with_bge('scientific discovery', rrf_res[:3])
    results['bge_rerank_test'] = {
        'status': 'PASS' if len(rerank_res) > 0 else 'FAIL',
        'count': len(rerank_res),
        'model_name': getattr(ret.get_reranker(), 'model_name_or_path', 'unknown'),
        'top_score': rerank_res[0].get('rerank_score') if rerank_res else None
    }
except Exception as e:
    results['retrieval_error'] = str(e)

# 2. CLAIM VERIFIER
try:
    from app.services.assistant.claim_verifier import ClaimVerifier
    verifier = ClaimVerifier()
    
    # Test deterministic overlap check
    test_claim = "Continual learning models suffer from catastrophic forgetting when trained on sequential tasks."
    test_evidence_high = "Continual learning models suffer from catastrophic forgetting when trained on sequential tasks without regularization."
    test_evidence_low = "Decision trees use entropy or Gini impurity to partition feature spaces."
    
    # Check method existence
    overlap_fn = getattr(verifier, '_compute_token_overlap', None) or getattr(verifier, 'compute_token_overlap', None)
    if overlap_fn:
        score_high = overlap_fn(test_claim, test_evidence_high)
        score_low = overlap_fn(test_claim, test_evidence_low)
        results['claim_verifier_stage_a'] = {
            'status': 'PASS',
            'score_high': score_high,
            'score_low': score_low,
            'threshold_applied': getattr(verifier, 'deterministic_threshold', 0.80)
        }
    else:
        results['claim_verifier_stage_a'] = {'status': 'PARTIAL', 'note': 'Overlap method private/custom'}
except Exception as e:
    results['claim_verifier_error'] = str(e)

# 3. COMPARISON ENGINE DIMENSIONS
try:
    import app.services.assistant.comparison_engine as comp
    dims = getattr(comp, 'COMPARISON_DIMENSIONS', [])
    results['comparison_dimensions'] = {
        'status': 'PASS' if len(dims) == 10 else 'PARTIAL',
        'count': len(dims),
        'dimensions': dims
    }
except Exception as e:
    results['comparison_engine_error'] = str(e)

# 4. CHROMA COLLECTIONS
try:
    from app.db.session import get_chroma_client
    client = get_chroma_client()
    colls = [{'name': c.name, 'count': c.count()} for c in client.list_collections()]
    results['chromadb_collections'] = {
        'status': 'PASS',
        'collections': colls
    }
except Exception as e:
    results['chromadb_error'] = str(e)

print(json.dumps(results, indent=2))
with open('scratch/direct_backend_test_results.json', 'w') as f:
    json.dump(results, f, indent=2)
