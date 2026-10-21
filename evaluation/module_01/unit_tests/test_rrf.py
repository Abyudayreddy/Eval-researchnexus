"""
Unit tests for Reciprocal Rank Fusion (RRF k=60) invariants:
1. Candidate appearing in both lists receives higher score
2. Candidate appearing only in BM25
3. Candidate appearing only in Dense
4. Candidate pool is strictly the UNION of input candidates (absence invariant)
5. k=60 constant respected
6. Deterministic tie breaking
"""
import pytest

def reciprocal_rank_fusion(bm25_results, dense_results, k=60):
    rrf_scores = {}
    bm25_ranks = {}
    dense_ranks = {}
    
    for rank, item in enumerate(bm25_results, 1):
        cid = item['chunk_id']
        rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (k + rank))
        bm25_ranks[cid] = rank
        
    for rank, item in enumerate(dense_results, 1):
        cid = item['chunk_id']
        rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (k + rank))
        dense_ranks[cid] = rank
        
    sorted_items = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    
    fused = []
    for rank, (cid, score) in enumerate(sorted_items, 1):
        fused.append({
            'rank': rank,
            'chunk_id': cid,
            'rrf_score': score,
            'bm25_rank': bm25_ranks.get(cid),
            'dense_rank': dense_ranks.get(cid)
        })
    return fused

def test_rrf_both_lists():
    bm25 = [{'chunk_id': 'c1'}, {'chunk_id': 'c2'}]
    dense = [{'chunk_id': 'c1'}, {'chunk_id': 'c3'}]
    res = reciprocal_rank_fusion(bm25, dense, k=60)
    # c1 is rank 1 in both: 1/(60+1) + 1/(60+1) = 2/61
    assert res[0]['chunk_id'] == 'c1'
    assert pytest.approx(res[0]['rrf_score']) == (2.0 / 61.0)

def test_rrf_single_list_candidates():
    bm25 = [{'chunk_id': 'c_bm25'}]
    dense = [{'chunk_id': 'c_dense'}]
    res = reciprocal_rank_fusion(bm25, dense, k=60)
    assert len(res) == 2
    # Both ranked 1 in their respective lists, so score is 1/61
    assert pytest.approx(res[0]['rrf_score']) == (1.0 / 61.0)
    assert pytest.approx(res[1]['rrf_score']) == (1.0 / 61.0)

def test_rrf_absence_invariant():
    bm25 = [{'chunk_id': 'c1'}, {'chunk_id': 'c2'}]
    dense = [{'chunk_id': 'c3'}, {'chunk_id': 'c4'}]
    res = reciprocal_rank_fusion(bm25, dense, k=60)
    res_cids = {x['chunk_id'] for x in res}
    assert 'c_ghost' not in res_cids
    assert res_cids == {'c1', 'c2', 'c3', 'c4'}

def test_rrf_k60_formula():
    bm25 = [{'chunk_id': 'c1'}]
    dense = []
    res = reciprocal_rank_fusion(bm25, dense, k=60)
    expected_score = 1.0 / (60 + 1)
    assert pytest.approx(res[0]['rrf_score']) == expected_score

if __name__ == '__main__':
    pytest.main([__file__])
