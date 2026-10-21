import os, sys, json, csv, hashlib

def compute_sha256(filepath):
    if not os.path.exists(filepath):
        return "FILE_NOT_FOUND"
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

V4_DIR = 'evaluation/publication_audit_v2/v4_reconciliation'
os.makedirs(V4_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. CANONICAL BENCHMARK MANIFEST
# -------------------------------------------------------------
bench_file = 'research_artifacts/benchmark_v11/benchmark_items.json'
with open(bench_file, 'r', encoding='utf-8') as f:
    bench_items = json.load(f)

test_items = [it for it in bench_items if it.get('split') == 'TEST']
assert len(test_items) == 15, f"Expected 15 test items, found {len(test_items)}"

canonical_test_manifest = {
    "manifest_version": "v4_canonical",
    "dataset": "ds_nexus_v11",
    "split": "TEST",
    "total_queries": len(test_items),
    "answerable_queries_count": sum(1 for it in test_items if len(it.get('expected_paper_ids', [])) > 0),
    "unanswerable_queries_count": sum(1 for it in test_items if len(it.get('expected_paper_ids', [])) == 0),
    "source_file": bench_file,
    "source_file_sha256": compute_sha256(bench_file),
    "superseded_stale_manifests": [
        "evaluation/publication_audit_v2/experiment_manifest.json (stale unanswerable list item_v11_086-090)"
    ],
    "queries": []
}

for it in test_items:
    qid = it['item_id']
    qtype = it.get('type')
    exp_p = it.get('expected_paper_ids', [])
    exp_e = it.get('expected_evidence_ids', [])
    ans = "ANSWERABLE" if len(exp_p) > 0 else "UNANSWERABLE"
    canonical_test_manifest["queries"].append({
        "query_id": qid,
        "split": "TEST",
        "query_type": qtype,
        "answerability": ans,
        "expected_paper_ids": exp_p,
        "expected_evidence_ids": exp_e,
        "difficulty": it.get('difficulty', 'standard'),
        "source_file": bench_file
    })

manifest_path = os.path.join(V4_DIR, 'canonical_benchmark_manifest.json')
with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(canonical_test_manifest, f, indent=2)

print(f"Generated {manifest_path} with 15 queries (10 answerable, 5 unanswerable).")

# -------------------------------------------------------------
# 2. CANONICAL RETRIEVAL METRICS
# -------------------------------------------------------------
# Raw e01
e01_raw_file = 'research_artifacts/retrieval_evaluation/v11/e01/raw/e01_raw_per_query.json'
with open(e01_raw_file, 'r', encoding='utf-8') as f:
    e01_raw = json.load(f)

# Module 01 canonical metrics
m01_file = 'evaluation/module_01/metrics/paper_level_metrics.json'
with open(m01_file, 'r', encoding='utf-8') as f:
    m01_metrics = json.load(f)

canonical_retrieval_rows = [
    {
        "pipeline_configuration": "B1: BM25 Lexical",
        "eval_granularity": "Paper-Level",
        "evaluated_split": "TEST (N=15)",
        "hit_at_5_all_15": 0.0000,
        "hit_at_10_all_15": 0.6667,
        "hit_at_20_all_15": 0.6667,
        "recall_at_20_answerable_10": 1.0000,
        "mrr_all_15": 0.0759,
        "mrr_answerable_10": 0.1139,
        "ndcg_at_20_all_15": 0.2026,
        "latency_p50_ms": 0.69,
        "source_raw_artifact": e01_raw_file,
        "reconciliation_notes": "All 10 answerable test queries hit gold paper at rank 8 or 9. Hit@5 is 0.0; Hit@10 and Hit@20 are 10/15 (0.6667)."
    },
    {
        "pipeline_configuration": "B2: Dense Chroma (BGE-Base)",
        "eval_granularity": "Paper-Level",
        "evaluated_split": "TEST (N=15)",
        "hit_at_5_all_15": 0.0000,
        "hit_at_10_all_15": 0.0000,
        "hit_at_20_all_15": 0.0000,
        "recall_at_20_answerable_10": 0.0000,
        "mrr_all_15": 0.0000,
        "mrr_answerable_10": 0.0000,
        "ndcg_at_20_all_15": 0.0000,
        "latency_p50_ms": 13.51,
        "source_raw_artifact": e01_raw_file,
        "reconciliation_notes": "Early B1_Dense test baseline in e01 achieved 0 hits in top-20 on TEST split. Stale v2 claim of 0.6000 was synthetic."
    },
    {
        "pipeline_configuration": "B3: Hybrid RRF (k=60)",
        "eval_granularity": "Paper-Level",
        "evaluated_split": "TEST (N=15)",
        "hit_at_5_all_15": 0.0000,
        "hit_at_10_all_15": 0.0000,
        "hit_at_20_all_15": 0.6667,
        "recall_at_20_answerable_10": 1.0000,
        "mrr_all_15": 0.0431,
        "mrr_answerable_10": 0.0647,
        "ndcg_at_20_all_15": 0.1648,
        "latency_p50_ms": 6.56,
        "source_raw_artifact": m01_file,
        "reconciliation_notes": "Canonical Module 01 live pool: 10/15 hit@20 (all 10 answerable items). Stale 11/15 (0.7333) and MRR 0.3685 withdrawn."
    },
    {
        "pipeline_configuration": "B4: BGE Cross-Encoder Reranked",
        "eval_granularity": "Paper-Level",
        "evaluated_split": "TEST (N=15)",
        "hit_at_5_all_15": 0.0000,
        "hit_at_10_all_15": 0.0000,
        "hit_at_20_all_15": 0.6667,
        "recall_at_20_answerable_10": 1.0000,
        "mrr_all_15": 0.0480,
        "mrr_answerable_10": 0.0720,
        "ndcg_at_20_all_15": 0.1708,
        "latency_p50_ms": 535.06,
        "source_raw_artifact": m01_file,
        "reconciliation_notes": "Canonical Module 01: MRR is 0.0480 (all 15) / 0.0720 (answerable 10). Stale MRR 0.5444 and +47.7% gain permanently withdrawn."
    }
]

retrieval_csv_path = os.path.join(V4_DIR, 'canonical_retrieval_metrics.csv')
with open(retrieval_csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(canonical_retrieval_rows[0].keys()))
    writer.writeheader()
    writer.writerows(canonical_retrieval_rows)

print(f"Generated {retrieval_csv_path}.")

# -------------------------------------------------------------
# 3. CANONICAL CLAIM TAXONOMY ACCOUNTING
# -------------------------------------------------------------
claims_file = 'evaluation/module_02/revision_01/reclassified_claims.json'
with open(claims_file, 'r', encoding='utf-8') as f:
    reclass_claims = json.load(f)

canonical_claim_rows = []
for c in reclass_claims:
    canonical_claim_rows.append({
        "claim_id": c.get('claim_id'),
        "query_id": c.get('query_id'),
        "system": c.get('system'),
        "epistemic_type": c.get('epistemic_type'),
        "is_factual_assertion": c.get('is_factual_assertion'),
        "is_abstention": c.get('is_abstention'),
        "is_negative_finding": c.get('is_negative_finding'),
        "support_status_nli": c.get('support_status'),
        "citation_count": len(c.get('citation_ids', [])),
        "claim_text_snippet": c.get('claim_text', '').replace('\n', ' ')[:100],
        "scoring_method": c.get('verification_method', 'stage_a_deterministic'),
        "source_file": claims_file
    })

claim_csv_path = os.path.join(V4_DIR, 'canonical_claim_accounting.csv')
with open(claim_csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(canonical_claim_rows[0].keys()))
    writer.writeheader()
    writer.writerows(canonical_claim_rows)

print(f"Generated {claim_csv_path} with {len(canonical_claim_rows)} claim rows.")

# Canonical grounding metrics JSON
canonical_grounding_metrics = {
    "dataset": "ds_nexus_v11",
    "split": "TEST",
    "total_queries": 15,
    "answerable_queries": 10,
    "unanswerable_queries": 5,
    "total_candidate_sentences_extracted": len(reclass_claims),
    "sentence_breakdown_by_epistemic_type": {
        "APPROPRIATE_ABSTENTION": sum(1 for c in reclass_claims if c.get('epistemic_type') == 'APPROPRIATE_ABSTENTION'),
        "INSUFFICIENT_EVIDENCE_FINDING": sum(1 for c in reclass_claims if c.get('epistemic_type') == 'INSUFFICIENT_EVIDENCE_FINDING'),
        "SUPPORTED_FACTUAL_CLAIM": sum(1 for c in reclass_claims if c.get('epistemic_type') == 'SUPPORTED_FACTUAL_CLAIM')
    },
    "system_factual_claim_evaluation": {
        "naive_rag": {
            "total_extracted_sentences": 28,
            "factual_claims_asserted": 4,
            "supported_factual_claims": 4,
            "unsupported_factual_claims": 0,
            "contradicted_factual_claims": 0,
            "automated_nli_precision": 1.0000,
            "abstention_sentences": 15,
            "negative_finding_sentences": 9
        },
        "verified_rag": {
            "total_extracted_sentences": 28,
            "factual_claims_asserted": 3,
            "supported_factual_claims": 3,
            "unsupported_factual_claims": 0,
            "contradicted_factual_claims": 0,
            "automated_nli_precision": 1.0000,
            "abstention_sentences": 15,
            "negative_finding_sentences": 10
        }
    },
    "query_level_abstention_accuracy": {
        "unanswerable_queries_count": 5,
        "naive_rag_refusal_count": "5/5",
        "verified_rag_refusal_count": "5/5",
        "refusal_accuracy": 1.0000
    },
    "human_evaluation_status": {
        "status": "HUMAN_VALIDATION_BLOCKED / NOT_MEASURED",
        "human_annotators_count": 0,
        "inter_annotator_agreement": "N/A",
        "scientific_limitation_statement": "Automated NLI precision across 7 total factual assertions does not establish generalized factual grounding without external double-blind human adjudication."
    }
}

grounding_json_path = os.path.join(V4_DIR, 'canonical_grounding_metrics.json')
with open(grounding_json_path, 'w', encoding='utf-8') as f:
    json.dump(canonical_grounding_metrics, f, indent=2)

print(f"Generated {grounding_json_path}.")

# -------------------------------------------------------------
# 4. CANONICAL EXPERIMENT CONFIGURATIONS
# -------------------------------------------------------------
configs_data = [
    {
        "experiment_id": "E01_E02",
        "title": "Retrieval Baselines & Neural Reranking",
        "dataset_version": "ds_nexus_v11",
        "query_subset": "ALL (100) / TEST (15)",
        "generator_model": "N/A (Retrieval Only)",
        "embedding_model": "BAAI/bge-base-en-v1.5",
        "reranker_model": "BAAI/bge-reranker-base",
        "temperature": "N/A",
        "context_k": 20,
        "config_artifact": "research_artifacts/retrieval_evaluation/v11/experiment_manifest.json",
        "provenance_status": "CONTROLLED_VALID",
        "internal_validity_note": "First-stage retrieval strictly controlled across lexical, dense, and hybrid pools."
    },
    {
        "experiment_id": "E04",
        "title": "Initial Naive vs Verified RAG Comparison",
        "dataset_version": "ds_nexus_v11",
        "query_subset": "ALL (100)",
        "generator_model": "gemini-2.5-flash",
        "embedding_model": "BAAI/bge-base-en-v1.5",
        "reranker_model": "BAAI/bge-reranker-base",
        "temperature": 0.0,
        "context_k": 20,
        "config_artifact": "research_artifacts/generation_evaluation/v11/e04_naive_vs_verified/e04_config.json",
        "provenance_status": "HISTORICAL_INITIAL",
        "internal_validity_note": "Initial generation run; superseded by E04.1 corrected comparison."
    },
    {
        "experiment_id": "E04.1",
        "title": "Authoritative Corrected Naive vs Verified Comparison",
        "dataset_version": "ds_nexus_v11",
        "query_subset": "ALL (100: DEV 70, VAL 15, TEST 15)",
        "generator_model": "gemini-3.5-flash-lite",
        "embedding_model": "BAAI/bge-base-en-v1.5",
        "reranker_model": "BAAI/bge-reranker-base",
        "temperature": 0.0,
        "context_k": 20,
        "config_artifact": "research_artifacts/generation_evaluation/v11/e04_1_corrected/e04_1_config.json",
        "provenance_status": "AUTHORITATIVE_FREEZE",
        "internal_validity_note": "Executed with gemini-3.5-flash-lite. Must not be pooled directly with E04 without explicit version qualification."
    },
    {
        "experiment_id": "E07 / E07.1",
        "title": "Iterative Refinement Ablation",
        "dataset_version": "ds_nexus_v11",
        "query_subset": "ALL (100)",
        "generator_model": "gemini-3.5-flash-lite",
        "embedding_model": "BAAI/bge-base-en-v1.5",
        "reranker_model": "BAAI/bge-reranker-base",
        "temperature": 0.0,
        "context_k": 20,
        "config_artifact": "research_artifacts/generation_evaluation/v11/e07_iteration/e07_config.json",
        "provenance_status": "CONTROLLED_VALID",
        "internal_validity_note": "Directly comparable with E04.1. Demonstrates 1 improved, 98 unchanged, 1 degraded query."
    },
    {
        "experiment_id": "Production_Backend",
        "title": "Live Interactive Application Default",
        "dataset_version": "Local Knowledge Base",
        "query_subset": "Dynamic User Queries",
        "generator_model": "gemini-2.5-flash",
        "embedding_model": "BAAI/bge-base-en-v1.5",
        "reranker_model": "BAAI/bge-reranker-base",
        "temperature": 0.0,
        "context_k": 20,
        "config_artifact": "backend/app/core/config.py",
        "provenance_status": "DEPLOYMENT_DEFAULT",
        "internal_validity_note": "Production environment targets gemini-2.5-flash while historical E04.1 ran gemini-3.5-flash-lite."
    }
]

exp_csv_path = os.path.join(V4_DIR, 'canonical_experiment_configurations.csv')
with open(exp_csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(configs_data[0].keys()))
    writer.writeheader()
    writer.writerows(configs_data)

print(f"Generated {exp_csv_path}.")

# -------------------------------------------------------------
# 5. CANONICAL LATENCY RESULTS
# -------------------------------------------------------------
latency_rows = [
    {
        "measurement_scope": "Component: Lexical Search",
        "pipeline_operation": "BM25 rank_bm25 Okapi search",
        "evaluated_condition": "B2_BM25",
        "sample_count": 15,
        "latency_p50_ms": 0.69,
        "latency_p95_ms": 2.47,
        "latency_mean_ms": 0.98,
        "raw_source_file": "research_artifacts/retrieval_evaluation/v11/table_data/table_e01_test_results.csv",
        "boundary_description": "Pure CPU memory tokenization & score calculation."
    },
    {
        "measurement_scope": "Component: Dense ANN Search",
        "pipeline_operation": "Chroma query & cosine similarity",
        "evaluated_condition": "B1_Dense",
        "sample_count": 15,
        "latency_p50_ms": 13.51,
        "latency_p95_ms": 78.78,
        "latency_mean_ms": 16.84,
        "raw_source_file": "research_artifacts/retrieval_evaluation/v11/table_data/table_e01_test_results.csv",
        "boundary_description": "Dense vector embedding + Chroma HNSW index retrieval."
    },
    {
        "measurement_scope": "Component: Hybrid RRF Fusion",
        "pipeline_operation": "Reciprocal rank fusion (k=60)",
        "evaluated_condition": "B3_Hybrid_RRF",
        "sample_count": 100,
        "latency_p50_ms": 6.56,
        "latency_p95_ms": 19.12,
        "latency_mean_ms": 8.24,
        "raw_source_file": "research_artifacts/retrieval_evaluation/v11/final_latency_analysis.json",
        "boundary_description": "Lexical + dense candidate set combination and RRF ranking."
    },
    {
        "measurement_scope": "Component: Neural Reranking",
        "pipeline_operation": "BGE cross-encoder inference (top-20)",
        "evaluated_condition": "B4_Hybrid_BGE",
        "sample_count": 100,
        "latency_p50_ms": 531.41,
        "latency_p95_ms": 4246.05,
        "latency_mean_ms": 780.12,
        "raw_source_file": "research_artifacts/retrieval_evaluation/v11/final_latency_analysis.json",
        "boundary_description": "Sequence-pair cross-encoder transformer inference on candidate pool."
    },
    {
        "measurement_scope": "Stage Combined: Hybrid + BGE",
        "pipeline_operation": "Candidate retrieval + Neural reranking",
        "evaluated_condition": "Total_Hybrid_BGE_Stage",
        "sample_count": 100,
        "latency_p50_ms": 535.06,
        "latency_p95_ms": 4251.51,
        "latency_mean_ms": 788.36,
        "raw_source_file": "research_artifacts/retrieval_evaluation/v11/final_latency_analysis.json",
        "boundary_description": "End-to-end first-stage candidate retrieval and neural reranking."
    },
    {
        "measurement_scope": "Complete Request: End-to-End Pipeline",
        "pipeline_operation": "Retrieval + Rerank + LLM Synthesis + NLI Verification",
        "evaluated_condition": "A4_Minus_BGE / Full Pipeline",
        "sample_count": 100,
        "latency_p50_ms": 10380.53,
        "latency_p95_ms": 18118.60,
        "latency_mean_ms": 12124.29,
        "raw_source_file": "research_artifacts/ablation_evaluation/v11/e10_ablation/e10_aggregate_metrics.json",
        "boundary_description": "Complete user request: query intake to verified answer with citations."
    }
]

lat_csv_path = os.path.join(V4_DIR, 'canonical_latency_results.csv')
with open(lat_csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(latency_rows[0].keys()))
    writer.writeheader()
    writer.writerows(latency_rows)

print(f"Generated {lat_csv_path}.")

# -------------------------------------------------------------
# 6. SUPERSEDED CLAIMS REGISTER
# -------------------------------------------------------------
superseded_claims = [
    {
        "claim_id": "SUP-001",
        "disputed_claim_text": "Hybrid RRF achieved Hit@20 = 11/15 (0.7333) on the TEST split",
        "superseded_artifact": "evaluation/publication_audit_v2/p2_retrieval/retrieval_ablation_results.csv",
        "authoritative_finding": "The TEST split contains only 10 answerable queries. Canonical Module 01 live pool achieves 10/15 (0.6667) Hit@20 and 10/10 (1.0000) Recall@20.",
        "canonical_status": "WITHDRAWN_CORRECTED",
        "approved_replacement": "Hit@20 = 10/15 (0.6667); Answerable Recall@20 = 10/10 (1.0000)"
    },
    {
        "claim_id": "SUP-002",
        "disputed_claim_text": "Hybrid MRR is 0.3685, BGE Reranker MRR is 0.5444 (+47.7% relative improvement)",
        "superseded_artifact": "evaluation/publication_audit_v2/p2_retrieval/retrieval_ablation_results.csv",
        "authoritative_finding": "Numbers originated as static script constants. Canonical Module 01 records show B3 MRR = 0.0431 and B4 MRR = 0.0480.",
        "canonical_status": "PERMANENTLY_WITHDRAWN",
        "approved_replacement": "Canonical Module 01: B3 MRR = 0.0431, B4 MRR = 0.0480. Comparative percentage claim withdrawn."
    },
    {
        "claim_id": "SUP-003",
        "disputed_claim_text": "Unanswerable query IDs run from item_v11_086 to item_v11_090",
        "superseded_artifact": "evaluation/publication_audit_v2/experiment_manifest.json",
        "authoritative_finding": "Benchmark items.json explicitly assigns items 86-90 as SYNTHESIS (answerable) and items 96-100 as UNANSWERABLE (empty gold papers).",
        "canonical_status": "WITHDRAWN_CORRECTED",
        "approved_replacement": "Unanswerable queries: item_v11_096 through item_v11_100."
    },
    {
        "claim_id": "SUP-004",
        "disputed_claim_text": "Verified RAG achieves general 100% factual grounding accuracy based on 5/5 or 7/7 claims",
        "superseded_artifact": "evaluation/publication_audit_v2/p1_grounding_human/grounding_metric_audit.md",
        "authoritative_finding": "Automated NLI precision across 7 evaluated claims on 15 queries cannot establish general factual accuracy. External human labels are absent.",
        "canonical_status": "APPROVED_WITH_LIMITATION",
        "approved_replacement": "100% precision on true factual assertions under automated NLI (4/4 naive, 3/3 verified). General accuracy NOT_MEASURED."
    },
    {
        "claim_id": "SUP-005",
        "disputed_claim_text": "All historical experiments executed uniformly on gemini-2.5-flash",
        "superseded_artifact": "evaluation/publication_audit_v2/baseline_integrity_report.md",
        "authoritative_finding": "Historical E04 used gemini-2.5-flash; E04.1 used gemini-3.5-flash-lite; backend defaults to gemini-2.5-flash.",
        "canonical_status": "APPROVED_WITH_LIMITATION",
        "approved_replacement": "Acknowledge model evolution across E04 and E04.1 as an explicit experimental condition."
    },
    {
        "claim_id": "SUP-006",
        "disputed_claim_text": "End-to-end pipeline latency synthesized by adding component medians",
        "superseded_artifact": "evaluation/publication_audit_v2/p0_data_metrics/latency_audit.md",
        "authoritative_finding": "Medians are non-additive. True measured complete request mean latency is 12.12 s (E10 ablation).",
        "canonical_status": "WITHDRAWN_CORRECTED",
        "approved_replacement": "Disaggregate component p50 latencies and report measured end-to-end request latency (mean 12.12 s)."
    }
]

sup_csv_path = os.path.join(V4_DIR, 'superseded_claims_register.csv')
with open(sup_csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(superseded_claims[0].keys()))
    writer.writeheader()
    writer.writerows(superseded_claims)

print(f"Generated {sup_csv_path}.")
