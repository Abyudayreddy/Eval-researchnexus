"""
Module 1 Controlled Retrieval Evaluation Runner

Evaluates 4 configurations against ds_nexus_v11 frozen TEST split (15 queries):
- B1: BM25 (rank_bm25)
- B2: Dense Retrieval (BAAI/bge-base-en-v1.5 in ChromaDB)
- B3: Hybrid RRF (k=60 fusion)
- B4: B3 Candidate Pool -> BAAI/bge-reranker-base Cross-Encoder

Generates raw outputs, metrics, latency logs, and consistency checks.
"""

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import sys
import json
import time
import math
import hashlib
from datetime import datetime
import numpy as np

sys.path.insert(0, os.path.abspath('backend'))
from app.services.local_evidence import get_local_retriever

CUTOFFS = [5, 10, 20, 50]
TOP_K_RETRIEVAL = 50

def compute_metrics_for_entity(gold_items, retrieved_items, cutoffs):
    """
    Computes Hit@K, Recall@K, Precision@K, MRR, nDCG@K for an entity list (papers or evidence).
    """
    res = {}
    
    # Hit@1
    h1 = 1.0 if (len(retrieved_items) > 0 and retrieved_items[0] in gold_items) else 0.0
    res["hit_at_1"] = h1
    
    # MRR (over full list)
    mrr = 0.0
    for idx, item in enumerate(retrieved_items):
        if item in gold_items:
            mrr = 1.0 / (idx + 1)
            break
    res["mrr"] = mrr
    
    for k in cutoffs:
        top_k = retrieved_items[:k]
        hits = [it for it in top_k if it in gold_items]
        n_hits = len(set(hits)) # Unique hits in top k
        
        hit_k = 1.0 if n_hits > 0 else 0.0
        
        if len(gold_items) > 0:
            rec_k = float(n_hits) / float(len(gold_items))
        else:
            rec_k = 0.0 # Unanswerable/adversarial queries have 0 gold items
            
        prec_k = float(n_hits) / float(k)
        
        # nDCG@K
        dcg = 0.0
        for idx, item in enumerate(top_k):
            if item in gold_items:
                dcg += 1.0 / math.log2(idx + 2)
        idcg = sum(1.0 / math.log2(idx + 2) for idx in range(min(len(gold_items), k)))
        ndcg_k = (dcg / idcg) if idcg > 0.0 else 0.0
        
        res[f"hit_at_{k}"] = hit_k
        res[f"recall_at_{k}"] = rec_k
        res[f"precision_at_{k}"] = prec_k
        res[f"ndcg_at_{k}"] = ndcg_k
        
    return res

def deduplicate_papers_preserving_rank(ranked_chunks):
    """
    Takes a list of chunk dicts or chunk IDs, extracts unique paper IDs preserving first-seen rank.
    """
    seen_papers = set()
    deduped_pids = []
    for c in ranked_chunks:
        pid = c.get('paper_id') if isinstance(c, dict) else c
        # Clean prefix if attached
        if pid and pid not in seen_papers:
            seen_papers.add(pid)
            deduped_pids.append(pid)
    return deduped_pids

def run_module_1_experiment():
    print("="*60)
    print("STARTING MODULE 1: CONTROLLED SCIENTIFIC RETRIEVAL EVALUATION")
    print("="*60)
    
    run_id = f"m01_eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f"Run ID: {run_id}")
    
    # 1. Load benchmark manifest
    with open('evaluation/module_01/benchmark_manifest.json', 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    queries = manifest['queries']
    print(f"Loaded {len(queries)} TEST queries from benchmark manifest.")
    
    # 2. Initialize real LocalEvidenceRetriever
    retriever = get_local_retriever()
    retriever.load()
    if retriever.init_status != "ready":
        print(f"FATAL: LocalEvidenceRetriever failed: {retriever.init_status}")
        sys.exit(1)
    print("LocalEvidenceRetriever initialized and ready.")
    
    raw_b1 = []
    raw_b2 = []
    raw_b3 = []
    raw_b4 = []
    
    per_query_paper_metrics = []
    per_query_evidence_metrics = []
    latency_per_query = []
    
    # Warmup pass (1 query)
    print("Executing warmup pass...")
    _ = retriever.retrieve_bm25(queries[0]['query_text'], top_k=5)
    _ = retriever.retrieve_dense(queries[0]['query_text'], top_k=5)
    print("Warmup complete. Beginning controlled evaluation...")
    
    for q_idx, q in enumerate(queries, 1):
        qid = q['query_id']
        qtext = q['query_text']
        gold_papers = q['expected_paper_ids']
        gold_evidence = q['expected_evidence_ids']
        
        print(f"[{q_idx}/{len(queries)}] Evaluating {qid}...")
        
        # --- B1: BM25 ---
        t0 = time.time()
        res_bm25, lat_bm25_inner = retriever.retrieve_bm25(qtext, top_k=TOP_K_RETRIEVAL)
        lat_bm25_total = (time.time() - t0) * 1000.0
        
        b1_raw_item = {
            'run_id': run_id,
            'query_id': qid,
            'configuration': 'B1_BM25',
            'retrieved_chunks': res_bm25,
            'latency_ms': lat_bm25_total
        }
        raw_b1.append(b1_raw_item)
        
        # --- B2: Dense (BAAI/bge-base-en-v1.5) ---
        t0 = time.time()
        res_dense, lat_dense_inner = retriever.retrieve_dense(qtext, top_k=TOP_K_RETRIEVAL)
        lat_dense_total = (time.time() - t0) * 1000.0
        
        b2_raw_item = {
            'run_id': run_id,
            'query_id': qid,
            'configuration': 'B2_Dense',
            'retrieved_chunks': res_dense,
            'latency_ms': lat_dense_total
        }
        raw_b2.append(b2_raw_item)
        
        # --- B3: Hybrid RRF (k=60) ---
        t0 = time.time()
        # Pure algorithmic fusion of res_bm25 and res_dense candidates
        rrf_scores = {}
        bm25_ranks = {}
        dense_ranks = {}
        chunk_map = {}
        
        for item in res_bm25:
            cid = item['chunk_id']
            chunk_map[cid] = item
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (60 + item['rank']))
            bm25_ranks[cid] = item['rank']
            
        for item in res_dense:
            cid = item['chunk_id']
            chunk_map[cid] = item
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (60 + item['rank']))
            dense_ranks[cid] = item['rank']
            
        sorted_rrf = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:TOP_K_RETRIEVAL]
        res_rrf = []
        for rank, (cid, score) in enumerate(sorted_rrf, 1):
            base_item = chunk_map[cid]
            res_rrf.append({
                'rank': rank,
                'chunk_id': cid,
                'paper_id': base_item['paper_id'],
                'rrf_score': score,
                'bm25_rank': bm25_ranks.get(cid),
                'dense_rank': dense_ranks.get(cid)
            })
        lat_rrf_total = (time.time() - t0) * 1000.0
        
        b3_raw_item = {
            'run_id': run_id,
            'query_id': qid,
            'configuration': 'B3_Hybrid_RRF',
            'retrieved_chunks': res_rrf,
            'latency_ms': lat_rrf_total
        }
        raw_b3.append(b3_raw_item)
        
        # --- B4: BGE Cross-Encoder Reranker ---
        # Starts from EXACT Top-20 B3 candidate pool
        t0 = time.time()
        b3_top20 = res_rrf[:20]
        
        # Reconstruct text for candidate pairs
        # In LocalEvidenceRetriever, collection.get provides chunk texts
        cids_top20 = [c['chunk_id'] for c in b3_top20]
        docs_fetched = retriever.collection.get(ids=cids_top20, include=['documents'])
        id_to_doc = {cid: doc for cid, doc in zip(docs_fetched['ids'], docs_fetched['documents'])}
        
        pairs = [[qtext, id_to_doc.get(c['chunk_id'], '')] for c in b3_top20]
        cross_scores = retriever.rerank_model.predict(pairs)
        
        b4_scored = []
        for orig_item, score in zip(b3_top20, cross_scores):
            b4_scored.append({
                'chunk_id': orig_item['chunk_id'],
                'paper_id': orig_item['paper_id'],
                'b3_rank': orig_item['rank'],
                'bge_score': float(score)
            })
        b4_sorted = sorted(b4_scored, key=lambda x: x['bge_score'], reverse=True)
        res_b4 = []
        for rank, item in enumerate(b4_sorted, 1):
            item['rank'] = rank
            res_b4.append(item)
            
        lat_b4_total = (time.time() - t0) * 1000.0
        
        b4_raw_item = {
            'run_id': run_id,
            'query_id': qid,
            'configuration': 'B4_BGE_Reranked',
            'retrieved_chunks': res_b4,
            'latency_ms': lat_b4_total
        }
        raw_b4.append(b4_raw_item)
        
        # Latency record
        latency_per_query.append({
            'run_id': run_id,
            'query_id': qid,
            'bm25_latency_ms': lat_bm25_total,
            'dense_latency_ms': lat_dense_total,
            'rrf_latency_ms': lat_rrf_total,
            'bge_latency_ms': lat_b4_total,
            'b4_end_to_end_ms': lat_bm25_total + lat_dense_total + lat_rrf_total + lat_b4_total
        })
        
        # --- COMPUTE METRICS FOR ALL 4 CONFIGURATIONS ---
        configs = [
            ('B1_BM25', res_bm25),
            ('B2_Dense', res_dense),
            ('B3_Hybrid_RRF', res_rrf),
            ('B4_BGE_Reranked', res_b4)
        ]
        
        for cfg_name, chunk_list in configs:
            # Evidence-Level evaluation (raw chunks)
            ret_cids = [c['chunk_id'] for c in chunk_list]
            ev_metrics = compute_metrics_for_entity(gold_evidence, ret_cids, CUTOFFS)
            per_query_evidence_metrics.append({
                'run_id': run_id,
                'query_id': qid,
                'configuration': cfg_name,
                'gold_count': len(gold_evidence),
                'metrics': ev_metrics
            })
            
            # Paper-Level evaluation (deduplicated papers)
            ret_pids = deduplicate_papers_preserving_rank(chunk_list)
            p_metrics = compute_metrics_for_entity(gold_papers, ret_pids, CUTOFFS)
            per_query_paper_metrics.append({
                'run_id': run_id,
                'query_id': qid,
                'configuration': cfg_name,
                'gold_count': len(gold_papers),
                'metrics': p_metrics
            })

    # Save raw outputs
    print("\nSaving raw evaluation JSONL files...")
    with open('evaluation/module_01/raw/B1_bm25.jsonl', 'w', encoding='utf-8') as f:
        for r in raw_b1: f.write(json.dumps(r) + '\n')
    with open('evaluation/module_01/raw/B2_dense.jsonl', 'w', encoding='utf-8') as f:
        for r in raw_b2: f.write(json.dumps(r) + '\n')
    with open('evaluation/module_01/raw/B3_rrf.jsonl', 'w', encoding='utf-8') as f:
        for r in raw_b3: f.write(json.dumps(r) + '\n')
    with open('evaluation/module_01/raw/B4_bge.jsonl', 'w', encoding='utf-8') as f:
        for r in raw_b4: f.write(json.dumps(r) + '\n')
        
    with open('evaluation/module_01/per_query/paper_level_metrics.jsonl', 'w', encoding='utf-8') as f:
        for r in per_query_paper_metrics: f.write(json.dumps(r) + '\n')
    with open('evaluation/module_01/per_query/evidence_level_metrics.jsonl', 'w', encoding='utf-8') as f:
        for r in per_query_evidence_metrics: f.write(json.dumps(r) + '\n')
        
    with open('evaluation/module_01/latency/latency_per_query.jsonl', 'w', encoding='utf-8') as f:
        for r in latency_per_query: f.write(json.dumps(r) + '\n')
        
    # Aggregate Paper-Level Metrics
    paper_agg = aggregate_metrics(per_query_paper_metrics, len(queries))
    with open('evaluation/module_01/metrics/paper_level_metrics.json', 'w', encoding='utf-8') as f:
        json.dump(paper_agg, f, indent=2)
        
    # Aggregate Evidence-Level Metrics
    evidence_agg = aggregate_metrics(per_query_evidence_metrics, len(queries))
    with open('evaluation/module_01/metrics/evidence_level_metrics.json', 'w', encoding='utf-8') as f:
        json.dump(evidence_agg, f, indent=2)
        
    # Latency Summary
    lat_summary = aggregate_latency(latency_per_query)
    with open('evaluation/module_01/latency/latency_summary.json', 'w', encoding='utf-8') as f:
        json.dump(lat_summary, f, indent=2)
        
    # Run Consistency Audit
    run_consistency_audit(per_query_paper_metrics, per_query_evidence_metrics)
    
    # Run Statistical Tests
    run_statistical_tests(per_query_paper_metrics, per_query_evidence_metrics)
    
    # Run Error Analysis
    run_error_analysis(manifest, raw_b1, raw_b2, raw_b3, raw_b4, per_query_paper_metrics, per_query_evidence_metrics)
    
    # Save Run Manifest
    save_run_manifest(run_id, manifest)
    
    print("="*60)
    print("MODULE 1 EVALUATION COMPLETE!")
    print("="*60)

def aggregate_metrics(per_query_records, n_queries):
    agg = {}
    cfg_groups = {}
    for r in per_query_records:
        cfg = r['configuration']
        cfg_groups.setdefault(cfg, []).append(r)
        
    for cfg, recs in cfg_groups.items():
        agg[cfg] = {'n_queries': len(recs)}
        sample_metrics = recs[0]['metrics']
        
        # Macro averages
        for m_name in sample_metrics.keys():
            # For recall, only average over queries with gold_count > 0
            if 'recall' in m_name:
                valid_vals = [r['metrics'][m_name] for r in recs if r['gold_count'] > 0]
                avg = float(np.mean(valid_vals)) if valid_vals else 0.0
            else:
                avg = float(np.mean([r['metrics'][m_name] for r in recs]))
            agg[cfg][m_name] = round(avg, 4)
    return agg

def aggregate_latency(latency_records):
    keys = ['bm25_latency_ms', 'dense_latency_ms', 'rrf_latency_ms', 'bge_latency_ms', 'b4_end_to_end_ms']
    summary = {}
    for k in keys:
        vals = [r[k] for r in latency_records]
        summary[k] = {
            'mean': round(float(np.mean(vals)), 2),
            'std': round(float(np.std(vals)), 2),
            'p50': round(float(np.percentile(vals, 50)), 2),
            'p90': round(float(np.percentile(vals, 90)), 2),
            'p95': round(float(np.percentile(vals, 95)), 2),
            'p99': round(float(np.percentile(vals, 99)), 2)
        }
    return summary

def run_consistency_audit(paper_records, evidence_records):
    print("\nRunning Metric Consistency Audit...")
    violations = []
    
    for entity_name, records in [('paper_level', paper_records), ('evidence_level', evidence_records)]:
        for r in records:
            qid = r['query_id']
            cfg = r['configuration']
            gold_cnt = r['gold_count']
            metrics = r['metrics']
            
            for k in CUTOFFS:
                hit = metrics[f'hit_at_{k}']
                rec = metrics[f'recall_at_{k}']
                
                # Rule 1: If gold_count > 0, Hit == 1 iff Recall > 0
                if gold_cnt > 0:
                    if hit == 1.0 and rec == 0.0:
                        violations.append({
                            'query_id': qid,
                            'configuration': cfg,
                            'entity': entity_name,
                            'cutoff': k,
                            'violation': 'Hit=1 but Recall=0',
                            'reason': 'Contradiction: Item claimed hit but 0% recall recorded.'
                        })
                    if hit == 0.0 and rec > 0.0:
                        violations.append({
                            'query_id': qid,
                            'configuration': cfg,
                            'entity': entity_name,
                            'cutoff': k,
                            'violation': 'Hit=0 but Recall>0',
                            'reason': 'Contradiction: Recall > 0 implies at least one gold item hit.'
                        })
                # Rule 2: If gold_count == 0, Hit must be 0 and Recall must be 0
                else:
                    if hit != 0.0 or rec != 0.0:
                        violations.append({
                            'query_id': qid,
                            'configuration': cfg,
                            'entity': entity_name,
                            'cutoff': k,
                            'violation': 'Hit/Recall > 0 on query with 0 gold items',
                            'reason': 'Ghost hit on unanswerable/adversarial query.'
                        })
                        
    audit_res = {
        'total_checks': len(paper_records + evidence_records) * len(CUTOFFS),
        'violations_count': len(violations),
        'status': 'PASS' if len(violations) == 0 else 'FAIL',
        'violations': violations
    }
    
    with open('evaluation/module_01/consistency/consistency_audit.json', 'w', encoding='utf-8') as f:
        json.dump(audit_res, f, indent=2)
        
    print(f"Consistency Audit Status: {audit_res['status']} ({audit_res['violations_count']} violations found)")
    if audit_res['status'] == 'FAIL':
        print("FATAL: Metric consistency audit failed! Check consistency_audit.json")
        sys.exit(1)

def run_statistical_tests(paper_records, evidence_records):
    from scipy.stats import wilcoxon
    print("\nRunning Paired Statistical Tests...")
    
    pairs = [
        ('B1_BM25', 'B2_Dense'),
        ('B2_Dense', 'B3_Hybrid_RRF'),
        ('B3_Hybrid_RRF', 'B4_BGE_Reranked')
    ]
    
    stat_results = {'paper_level': {}, 'evidence_level': {}}
    
    for entity_name, records in [('paper_level', paper_records), ('evidence_level', evidence_records)]:
        # Group by config
        cfg_map = {}
        for r in records:
            cfg_map.setdefault(r['configuration'], {})[r['query_id']] = r
            
        for base_cfg, new_cfg in pairs:
            pair_key = f"{base_cfg}_vs_{new_cfg}"
            stat_results[entity_name][pair_key] = {}
            
            # Metrics to test: MRR, hit_at_5, recall_at_5, hit_at_20, recall_at_20
            test_metrics = ['mrr', 'hit_at_5', 'recall_at_5', 'hit_at_20', 'recall_at_20']
            for m in test_metrics:
                # Queries where gold > 0 if recall
                qids = sorted(list(cfg_map[base_cfg].keys()))
                if 'recall' in m:
                    qids = [qid for qid in qids if cfg_map[base_cfg][qid]['gold_count'] > 0]
                    
                v_base = [cfg_map[base_cfg][qid]['metrics'][m] for qid in qids]
                v_new = [cfg_map[new_cfg][qid]['metrics'][m] for qid in qids]
                
                diffs = np.array(v_new) - np.array(v_base)
                mean_diff = float(np.mean(diffs))
                
                # Check if all diffs are zero
                if np.all(diffs == 0):
                    stat_results[entity_name][pair_key][m] = {
                        'mean_baseline': round(float(np.mean(v_base)), 4),
                        'mean_new': round(float(np.mean(v_new)), 4),
                        'mean_delta': round(mean_diff, 4),
                        'test': 'Wilcoxon signed-rank test',
                        'p_value': 1.0,
                        'statistically_significant': False,
                        'note': 'Identical distributions across all queries'
                    }
                else:
                    try:
                        stat, p_val = wilcoxon(v_new, v_base, zero_method='wilcox')
                        stat_results[entity_name][pair_key][m] = {
                            'mean_baseline': round(float(np.mean(v_base)), 4),
                            'mean_new': round(float(np.mean(v_new)), 4),
                            'mean_delta': round(mean_diff, 4),
                            'statistic': float(stat),
                            'test': 'Wilcoxon signed-rank test',
                            'p_value': round(float(p_val), 5),
                            'statistically_significant': bool(p_val < 0.05)
                        }
                    except Exception as e:
                        stat_results[entity_name][pair_key][m] = {
                            'mean_delta': round(mean_diff, 4),
                            'error': str(e)
                        }
                        
    with open('evaluation/module_01/statistics/statistical_tests.json', 'w', encoding='utf-8') as f:
        json.dump(stat_results, f, indent=2)

def run_error_analysis(manifest, raw_b1, raw_b2, raw_b3, raw_b4, paper_records, evidence_records):
    print("\nRunning Retrieval Error Analysis...")
    errors = {
        'queries_gold_paper_never_retrieved': [],
        'queries_gold_evidence_never_retrieved': [],
        'queries_paper_retrieved_evidence_missed': [],
        'queries_b3_improved_over_b1_b2': [],
        'queries_b4_changed_ranking': [],
        'queries_b4_degraded_top5': [],
        'queries_b4_improved_top5': []
    }
    
    # Map by query
    q_map = {q['query_id']: q for q in manifest['queries']}
    p_recs = {}
    for r in paper_records:
        p_recs.setdefault(r['query_id'], {})[r['configuration']] = r
    e_recs = {}
    for r in evidence_records:
        e_recs.setdefault(r['query_id'], {})[r['configuration']] = r
        
    for q in manifest['queries']:
        qid = q['query_id']
        g_papers = q['expected_paper_ids']
        g_evidence = q['expected_evidence_ids']
        
        if not g_papers:
            continue # Skip unanswerable queries
            
        p_b1 = p_recs[qid]['B1_BM25']['metrics']['hit_at_50']
        p_b2 = p_recs[qid]['B2_Dense']['metrics']['hit_at_50']
        p_b3 = p_recs[qid]['B3_Hybrid_RRF']['metrics']['hit_at_50']
        p_b4 = p_recs[qid]['B4_BGE_Reranked']['metrics']['hit_at_20']
        
        e_b1 = e_recs[qid]['B1_BM25']['metrics']['hit_at_50']
        e_b2 = e_recs[qid]['B2_Dense']['metrics']['hit_at_50']
        e_b3 = e_recs[qid]['B3_Hybrid_RRF']['metrics']['hit_at_50']
        e_b4 = e_recs[qid]['B4_BGE_Reranked']['metrics']['hit_at_20']
        
        # 1. Gold paper never retrieved by any system
        if max(p_b1, p_b2, p_b3, p_b4) == 0.0:
            errors['queries_gold_paper_never_retrieved'].append(qid)
            
        # 2. Gold evidence never retrieved
        if max(e_b1, e_b2, e_b3, e_b4) == 0.0:
            errors['queries_gold_evidence_never_retrieved'].append(qid)
            
        # 3. Paper retrieved but evidence missed
        if max(p_b1, p_b2, p_b3, p_b4) == 1.0 and max(e_b1, e_b2, e_b3, e_b4) == 0.0:
            errors['queries_paper_retrieved_evidence_missed'].append(qid)
            
        # 4. B3 improved over B1 & B2
        h5_b1 = p_recs[qid]['B1_BM25']['metrics']['hit_at_5']
        h5_b2 = p_recs[qid]['B2_Dense']['metrics']['hit_at_5']
        h5_b3 = p_recs[qid]['B3_Hybrid_RRF']['metrics']['hit_at_5']
        if h5_b3 > max(h5_b1, h5_b2):
            errors['queries_b3_improved_over_b1_b2'].append(qid)
            
        # 5. B4 vs B3 top-5 changes
        h5_b4 = p_recs[qid]['B4_BGE_Reranked']['metrics']['hit_at_5']
        if h5_b4 > h5_b3:
            errors['queries_b4_improved_top5'].append(qid)
        elif h5_b4 < h5_b3:
            errors['queries_b4_degraded_top5'].append(qid)
            
    with open('evaluation/module_01/error_analysis/error_cases.json', 'w', encoding='utf-8') as f:
        json.dump(errors, f, indent=2)

def save_run_manifest(run_id, manifest):
    run_meta = {
        'run_id': run_id,
        'timestamp': datetime.now().isoformat(),
        'benchmark_version': 'ds_nexus_v11',
        'corpus_version': 'ResearchMind_LocalKB_v1',
        'test_query_count': len(manifest['queries']),
        'models': {
            'bm25': 'rank_bm25 (BM25Okapi)',
            'dense': 'BAAI/bge-base-en-v1.5',
            'rrf': 'RRF k=60',
            'reranker': 'BAAI/bge-reranker-base'
        },
        'hardware': 'Local CPU',
        'torch_version': '2.11.0+cpu',
        'cuda_available': False
    }
    with open('evaluation/module_01/run_manifest.json', 'w', encoding='utf-8') as f:
        json.dump(run_meta, f, indent=2)

if __name__ == '__main__':
    run_module_1_experiment()
