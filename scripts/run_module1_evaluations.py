import os
import sys
import json
import time
import math
import datetime
import numpy as np
from scipy.stats import wilcoxon

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.db.session import SessionLocal
from app.models.evaluation import EvaluationDataset, EvaluationItem
from app.services.local_evidence import get_local_retriever

def compute_ir_metrics(expected_papers, expected_evidence, retrieved_papers, retrieved_evidence):
    # Hit@1
    h1 = 1.0 if (retrieved_papers and retrieved_papers[0] in expected_papers) else 0.0
    
    # Hit@5
    top5_p = retrieved_papers[:5]
    h5 = 1.0 if any(p in expected_papers for p in top5_p) else 0.0
    
    # Recall@5 & Precision@5
    if expected_papers:
        hits_p = sum(1 for p in expected_papers if p in top5_p)
        rec5 = hits_p / float(len(expected_papers))
        prec5 = hits_p / 5.0
    else:
        rec5, prec5 = 0.0, 0.0
        
    # MRR
    mrr = 0.0
    for idx, p in enumerate(retrieved_papers):
        if p in expected_papers:
            mrr = 1.0 / (idx + 1)
            break
            
    # nDCG@5
    if expected_papers:
        dcg = 0.0
        for idx, p in enumerate(top5_p):
            if p in expected_papers:
                dcg += 1.0 / math.log2(idx + 2)
        idcg = sum(1.0 / math.log2(idx + 2) for idx in range(min(len(expected_papers), 5)))
        ndcg5 = dcg / idcg if idcg > 0 else 0.0
    else:
        ndcg5 = 0.0

    # Evidence metrics
    top5_e = retrieved_evidence[:5]
    eh5 = 1.0 if any(e in expected_evidence for e in top5_e) else 0.0
    if expected_evidence:
        hits_e = sum(1 for e in expected_evidence if e in top5_e)
        erec5 = hits_e / float(len(expected_evidence))
        eprec5 = hits_e / 5.0
    else:
        erec5, eprec5 = 0.0, 0.0

    return {
        "hit_at_1": h1,
        "hit_at_5": h5,
        "recall_at_5": rec5,
        "precision_at_5": prec5,
        "mrr": mrr,
        "ndcg_at_5": ndcg5,
        "evidence_hit_at_5": eh5,
        "evidence_recall_at_5": erec5,
        "evidence_precision_at_5": eprec5
    }

def run_evaluation():
    print("Starting Real Module 1 Retrieval Evaluation...", flush=True)
    from app.db.session import engine, Base
    from app.scripts.seed_benchmark_v10 import seed_benchmark_v10

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    ds = db.query(EvaluationDataset).filter(EvaluationDataset.dataset_id == "ds_nexus_v10").first()
    if not ds:
        print("Dataset ds_nexus_v10 not found. Running seed_benchmark_v10...", flush=True)
        db.close()
        seed_benchmark_v10()
        db = SessionLocal()

    retriever = get_local_retriever()
    if retriever.init_status != "ready":
        retriever.load()
    print(f"Retriever status: {retriever.init_status}", flush=True)

    items = db.query(EvaluationItem).filter(
        EvaluationItem.dataset_id == "ds_nexus_v10",
        EvaluationItem.gold_verified == "TRUE"
    ).all()
    print(f"Loaded {len(items)} benchmark items from ds_nexus_v10 DB.", flush=True)

    out_dir = os.path.abspath("research_artifacts/retrieval_evaluation")
    e01_raw_dir = os.path.join(out_dir, "e01_raw_results")
    e02_raw_dir = os.path.join(out_dir, "e02_raw_results")
    os.makedirs(e01_raw_dir, exist_ok=True)
    os.makedirs(e02_raw_dir, exist_ok=True)

    # ----------------------------------------------------
    # E01 RUN: BM25 (B2), Dense (B1), Hybrid RRF (B3)
    # ----------------------------------------------------
    e01_raw = {"bm25": [], "dense": [], "hybrid": []}

    for it in items:
        expected_papers = json.loads(it.expected_paper_ids) if it.expected_paper_ids else []
        expected_evidence = json.loads(it.expected_evidence_ids) if it.expected_evidence_ids else []

        # 1. BM25 (B2)
        t0 = time.time()
        res_bm25, lat_bm25 = retriever.retrieve_bm25(it.question, top_k=10)
        dur_bm25 = (time.time() - t0) * 1000.0
        ret_p_bm25 = [c['paper_id'] for c in res_bm25]
        ret_e_bm25 = [c['chunk_id'] for c in res_bm25]
        m_bm25 = compute_ir_metrics(expected_papers, expected_evidence, ret_p_bm25, ret_e_bm25)
        e01_raw["bm25"].append({
            "item_id": it.item_id,
            "split": it.split,
            "question_type": it.question_type,
            "question": it.question,
            "expected_papers": expected_papers,
            "expected_evidence": expected_evidence,
            "retrieved_papers": ret_p_bm25,
            "retrieved_evidence": ret_e_bm25,
            "metrics": m_bm25,
            "latency_ms": round(dur_bm25, 2),
            "provenance": res_bm25
        })

        # 2. Dense (B1)
        t0 = time.time()
        res_dense, lat_dense = retriever.retrieve_dense(it.question, top_k=10)
        dur_dense = (time.time() - t0) * 1000.0
        ret_p_dense = [c['paper_id'] for c in res_dense]
        ret_e_dense = [c['chunk_id'] for c in res_dense]
        m_dense = compute_ir_metrics(expected_papers, expected_evidence, ret_p_dense, ret_e_dense)
        e01_raw["dense"].append({
            "item_id": it.item_id,
            "split": it.split,
            "question_type": it.question_type,
            "question": it.question,
            "expected_papers": expected_papers,
            "expected_evidence": expected_evidence,
            "retrieved_papers": ret_p_dense,
            "retrieved_evidence": ret_e_dense,
            "metrics": m_dense,
            "latency_ms": round(dur_dense, 2),
            "provenance": res_dense
        })

        # 3. Hybrid RRF (B3)
        t0 = time.time()
        cand_rrf, tr_rrf = retriever.retrieve_hybrid_rrf(it.question, top_k=10)
        ev_rrf, meta_rrf, l_build, tr_build = retriever.rerank_and_build_evidence(it.question, cand_rrf, top_k_evidence=10, use_reranker=False)
        dur_hybrid = (time.time() - t0) * 1000.0
        res_hybrid = ev_rrf if ev_rrf else meta_rrf
        ret_p_hybrid = [c.get('paper_id', c.get('id')) for c in res_hybrid]
        ret_e_hybrid = [c.get('chunk_id', c.get('id')) for c in res_hybrid]
        m_hybrid = compute_ir_metrics(expected_papers, expected_evidence, ret_p_hybrid, ret_e_hybrid)
        e01_raw["hybrid"].append({
            "item_id": it.item_id,
            "split": it.split,
            "question_type": it.question_type,
            "question": it.question,
            "expected_papers": expected_papers,
            "expected_evidence": expected_evidence,
            "retrieved_papers": ret_p_hybrid,
            "retrieved_evidence": ret_e_hybrid,
            "metrics": m_hybrid,
            "latency_ms": round(dur_hybrid, 2),
            "provenance": res_hybrid
        })

    # Write E01 Raw Artifacts
    with open(os.path.join(e01_raw_dir, "e01_bm25_raw.json"), "w") as f:
        json.dump(e01_raw["bm25"], f, indent=2)
    with open(os.path.join(e01_raw_dir, "e01_dense_raw.json"), "w") as f:
        json.dump(e01_raw["dense"], f, indent=2)
    with open(os.path.join(e01_raw_dir, "e01_hybrid_raw.json"), "w") as f:
        json.dump(e01_raw["hybrid"], f, indent=2)

    # ----------------------------------------------------
    # E02 RUN: B3 Hybrid vs B4 Hybrid + BGE Reranker
    # ----------------------------------------------------
    e02_raw = {"b3_hybrid": [], "b4_bge": []}

    for it in items:
        expected_papers = json.loads(it.expected_paper_ids) if it.expected_paper_ids else []
        expected_evidence = json.loads(it.expected_evidence_ids) if it.expected_evidence_ids else []

        # B3 Hybrid (pre-rerank)
        t0 = time.time()
        cand_rrf, tr_rrf = retriever.retrieve_hybrid_rrf(it.question, top_k=10)
        ev_b3, meta_b3, l_build3, tr_build3 = retriever.rerank_and_build_evidence(it.question, cand_rrf, top_k_evidence=10, use_reranker=False)
        dur_b3 = (time.time() - t0) * 1000.0
        res_b3 = ev_b3 if ev_b3 else meta_b3
        ret_p_b3 = [c.get('paper_id', c.get('id')) for c in res_b3]
        ret_e_b3 = [c.get('chunk_id', c.get('id')) for c in res_b3]
        m_b3 = compute_ir_metrics(expected_papers, expected_evidence, ret_p_b3, ret_e_b3)

        e02_raw["b3_hybrid"].append({
            "item_id": it.item_id,
            "split": it.split,
            "question": it.question,
            "expected_papers": expected_papers,
            "retrieved_papers": ret_p_b3,
            "metrics": m_b3,
            "latency_ms": round(dur_b3, 2)
        })

        # B4 Hybrid + BGE
        t0 = time.time()
        ev_b4, meta_b4, l_build4, tr_build4 = retriever.rerank_and_build_evidence(it.question, cand_rrf, top_k_evidence=10, use_reranker=True)
        dur_b4 = (time.time() - t0) * 1000.0
        res_b4 = ev_b4 if ev_b4 else meta_b4
        ret_p_b4 = [c.get('paper_id', c.get('id')) for c in res_b4]
        ret_e_b4 = [c.get('chunk_id', c.get('id')) for c in res_b4]
        m_b4 = compute_ir_metrics(expected_papers, expected_evidence, ret_p_b4, ret_e_b4)

        # Movement tracking for gold paper
        movement = "unchanged"
        if expected_papers:
            gold_p = expected_papers[0]
            r_b3 = ret_p_b3.index(gold_p) + 1 if gold_p in ret_p_b3 else 999
            r_b4 = ret_p_b4.index(gold_p) + 1 if gold_p in ret_p_b4 else 999
            if r_b4 < r_b3:
                movement = "improved"
            elif r_b4 > r_b3:
                movement = "worsened"

        e02_raw["b4_bge"].append({
            "item_id": it.item_id,
            "split": it.split,
            "question": it.question,
            "expected_papers": expected_papers,
            "pre_rerank_papers": ret_p_b3,
            "post_rerank_papers": ret_p_b4,
            "rank_movement": movement,
            "bge_scores": {c.get('paper_id', c.get('id')): c.get('reranker_score') for c in res_b4},
            "metrics": m_b4,
            "latency_ms": round(dur_b4, 2)
        })

    # Write E02 Raw Artifacts
    with open(os.path.join(e02_raw_dir, "e02_b3_hybrid_raw.json"), "w") as f:
        json.dump(e02_raw["b3_hybrid"], f, indent=2)
    with open(os.path.join(e02_raw_dir, "e02_b4_bge_raw.json"), "w") as f:
        json.dump(e02_raw["b4_bge"], f, indent=2)

    # ----------------------------------------------------
    # AGGREGATE E01 METRICS
    # ----------------------------------------------------
    def aggregate_runs(runs):
        mrr = [r["metrics"]["mrr"] for r in runs]
        hit1 = [r["metrics"]["hit_at_1"] for r in runs]
        hit5 = [r["metrics"]["hit_at_5"] for r in runs]
        rec5 = [r["metrics"]["recall_at_5"] for r in runs]
        prec5 = [r["metrics"]["precision_at_5"] for r in runs]
        ndcg5 = [r["metrics"]["ndcg_at_5"] for r in runs]
        erec5 = [r["metrics"]["evidence_recall_at_5"] for r in runs]
        eprec5 = [r["metrics"]["evidence_precision_at_5"] for r in runs]
        lats = [r["latency_ms"] for r in runs]

        return {
            "item_count": len(runs),
            "hit_at_1": round(float(np.mean(hit1)), 3),
            "hit_at_5": round(float(np.mean(hit5)), 3),
            "recall_at_5": round(float(np.mean(rec5)), 3),
            "precision_at_5": round(float(np.mean(prec5)), 3),
            "mrr": round(float(np.mean(mrr)), 3),
            "ndcg_at_5": round(float(np.mean(ndcg5)), 3),
            "evidence_recall_at_5": round(float(np.mean(erec5)), 3),
            "evidence_precision_at_5": round(float(np.mean(eprec5)), 3),
            "p50_latency_ms": round(float(np.percentile(lats, 50)), 2),
            "p95_latency_ms": round(float(np.percentile(lats, 95)), 2)
        }

    # E01 Aggregates (Full vs TEST split)
    e01_bm25_full = aggregate_runs(e01_raw["bm25"])
    e01_dense_full = aggregate_runs(e01_raw["dense"])
    e01_hybrid_full = aggregate_runs(e01_raw["hybrid"])

    e01_bm25_test = aggregate_runs([r for r in e01_raw["bm25"] if r["split"] == "TEST"])
    e01_dense_test = aggregate_runs([r for r in e01_raw["dense"] if r["split"] == "TEST"])
    e01_hybrid_test = aggregate_runs([r for r in e01_raw["hybrid"] if r["split"] == "TEST"])

    # Wilcoxon test: Hybrid vs Dense on Full N=100
    mrr_h = [r["metrics"]["mrr"] for r in e01_raw["hybrid"]]
    mrr_d = [r["metrics"]["mrr"] for r in e01_raw["dense"]]
    try:
        stat, pval = wilcoxon(mrr_h, mrr_d)
        w_p = float(pval)
    except Exception:
        w_p = 1.0

    e01_aggregate = {
        "experiment_id": "E01_REAL_RETRIEVAL_BASELINE",
        "dataset_version": "ds_nexus_v10",
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "full_benchmark_n100": {
            "B1_Dense_RAG": e01_dense_full,
            "B2_BM25_RAG": e01_bm25_full,
            "B3_Hybrid_RAG": e01_hybrid_full
        },
        "frozen_test_split_n15": {
            "B1_Dense_RAG": e01_dense_test,
            "B2_BM25_RAG": e01_bm25_test,
            "B3_Hybrid_RAG": e01_hybrid_test
        },
        "statistical_test": {
            "comparison": "B3 Hybrid vs B1 Dense MRR",
            "wilcoxon_p_value": w_p,
            "significant": w_p < 0.05
        }
    }

    with open(os.path.join(out_dir, "e01_aggregate_results.json"), "w") as f:
        json.dump(e01_aggregate, f, indent=2)

    # ----------------------------------------------------
    # AGGREGATE E02 METRICS
    # ----------------------------------------------------
    e02_b3_full = aggregate_runs(e02_raw["b3_hybrid"])
    e02_b4_full = aggregate_runs(e02_raw["b4_bge"])

    e02_b3_test = aggregate_runs([r for r in e02_raw["b3_hybrid"] if r["split"] == "TEST"])
    e02_b4_test = aggregate_runs([r for r in e02_raw["b4_bge"] if r["split"] == "TEST"])

    movements = [r["rank_movement"] for r in e02_raw["b4_bge"] if r["split"] == "TEST"]
    move_summary = {
        "improved": movements.count("improved"),
        "unchanged": movements.count("unchanged"),
        "worsened": movements.count("worsened")
    }

    mrr_b3_t = [r["metrics"]["mrr"] for r in e02_raw["b3_hybrid"] if r["split"] == "TEST"]
    mrr_b4_t = [r["metrics"]["mrr"] for r in e02_raw["b4_bge"] if r["split"] == "TEST"]
    try:
        stat_e02, pval_e02 = wilcoxon(mrr_b4_t, mrr_b3_t)
        w_p_e02 = float(pval_e02)
    except Exception:
        w_p_e02 = 1.0

    e02_aggregate = {
        "experiment_id": "E02_REAL_BGE_RERANKING",
        "dataset_version": "ds_nexus_v10",
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "full_benchmark_n100": {
            "B3_Hybrid_RAG": e02_b3_full,
            "B4_Hybrid_BGE": e02_b4_full
        },
        "frozen_test_split_n15": {
            "B3_Hybrid_RAG": e02_b3_test,
            "B4_Hybrid_BGE": e02_b4_test
        },
        "rank_movement_on_test_split": move_summary,
        "statistical_test": {
            "comparison": "B4 Hybrid+BGE vs B3 Hybrid MRR (TEST split N=15)",
            "wilcoxon_p_value": w_p_e02,
            "significant": w_p_e02 < 0.05
        }
    }

    with open(os.path.join(out_dir, "e02_aggregate_results.json"), "w") as f:
        json.dump(e02_aggregate, f, indent=2)

    db.close()
    print("Real Module 1 Retrieval Evaluation Completed Successfully!", flush=True)

if __name__ == "__main__":
    run_evaluation()
