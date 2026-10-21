"""
Accurate Error Analysis generator for Module 1
Categorizes per-query rank dynamics across B1, B2, B3, and B4.
"""
import json

with open('evaluation/module_01/benchmark_manifest.json') as f:
    manifest = json.load(f)

with open('evaluation/module_01/raw/B1_bm25.jsonl') as f:
    b1_raw = [json.loads(line) for line in f]
with open('evaluation/module_01/raw/B2_dense.jsonl') as f:
    b2_raw = [json.loads(line) for line in f]
with open('evaluation/module_01/raw/B3_rrf.jsonl') as f:
    b3_raw = [json.loads(line) for line in f]
with open('evaluation/module_01/raw/B4_bge.jsonl') as f:
    b4_raw = [json.loads(line) for line in f]

errors = {
    'total_queries': len(manifest['queries']),
    'unanswerable_queries': [q['query_id'] for q in manifest['queries'] if not q['expected_paper_ids']],
    'queries_where_dense_missed_completely': [],
    'queries_where_bm25_retrieved_in_top10': [],
    'queries_where_rrf_placed_gold_in_top20': [],
    'queries_where_bge_promoted_gold_rank': [],
    'queries_where_bge_demoted_gold_rank': [],
    'queries_where_bge_rank_unchanged': [],
    'detailed_rank_table': []
}

for q in manifest['queries']:
    qid = q['query_id']
    gp = q['expected_paper_ids']
    ge = q['expected_evidence_ids']
    
    if not gp:
        continue # Unanswerable / adversarial
        
    gold_p = gp[0]
    
    b1_item = next(x for x in b1_raw if x['query_id'] == qid)
    b2_item = next(x for x in b2_raw if x['query_id'] == qid)
    b3_item = next(x for x in b3_raw if x['query_id'] == qid)
    b4_item = next(x for x in b4_raw if x['query_id'] == qid)
    
    b1_pids = [c['paper_id'] for c in b1_item['retrieved_chunks']]
    b2_pids = [c['paper_id'] for c in b2_item['retrieved_chunks']]
    b3_pids = [c['paper_id'] for c in b3_item['retrieved_chunks']]
    b4_pids = [c['paper_id'] for c in b4_item['retrieved_chunks']]
    
    r1 = b1_pids.index(gold_p) + 1 if gold_p in b1_pids else None
    r2 = b2_pids.index(gold_p) + 1 if gold_p in b2_pids else None
    r3 = b3_pids.index(gold_p) + 1 if gold_p in b3_pids else None
    r4 = b4_pids.index(gold_p) + 1 if gold_p in b4_pids else None
    
    if r2 is None:
        errors['queries_where_dense_missed_completely'].append(qid)
    if r1 is not None and r1 <= 10:
        errors['queries_where_bm25_retrieved_in_top10'].append(qid)
    if r3 is not None and r3 <= 20:
        errors['queries_where_rrf_placed_gold_in_top20'].append(qid)
        
    if r3 is not None and r4 is not None:
        if r4 < r3:
            errors['queries_where_bge_promoted_gold_rank'].append(qid)
        elif r4 > r3:
            errors['queries_where_bge_demoted_gold_rank'].append(qid)
        else:
            errors['queries_where_bge_rank_unchanged'].append(qid)
            
    errors['detailed_rank_table'].append({
        'query_id': qid,
        'gold_paper': gold_p,
        'gold_evidence': ge,
        'bm25_rank': r1,
        'dense_rank': r2,
        'rrf_rank': r3,
        'bge_rank': r4
    })

with open('evaluation/module_01/error_analysis/error_cases.json', 'w', encoding='utf-8') as f:
    json.dump(errors, f, indent=2)

print("Error analysis cases JSON updated successfully!")
print("Queries where Dense missed completely:", len(errors['queries_where_dense_missed_completely']))
print("Queries where BM25 retrieved in top 10:", len(errors['queries_where_bm25_retrieved_in_top10']))
print("Queries where RRF placed gold in top 20:", len(errors['queries_where_rrf_placed_gold_in_top20']))
print("Queries where BGE promoted rank:", len(errors['queries_where_bge_promoted_gold_rank']))
print("Queries where BGE demoted rank:", len(errors['queries_where_bge_demoted_gold_rank']))
print("Queries where BGE rank unchanged:", len(errors['queries_where_bge_rank_unchanged']))
