import os, sys, json, csv

AUDIT_DIR = 'evaluation/publication_audit_v2'
os.makedirs(AUDIT_DIR, exist_ok=True)
os.makedirs(os.path.join(AUDIT_DIR, 'p0_data_metrics'), exist_ok=True)

# 1. repository_inventory.md
repo_inv = """# Repository Inventory & Structural Audit

## 1. Executive Summary
This document provides an exhaustive structural and functional audit of the ResearchNexusAI codebase and research experimental artifacts as part of the IEEE Publication Audit v2.

## 2. Directory Structure and Responsibilities
- **backend/**: Core production and research pipeline implementation.
  - `app/services/vector_store.py`: ChromaDB dense retrieval, embedding generation, collection management.
  - `app/services/hybrid_search.py`: Lexical BM25 (rank_bm25 / Okapi), Dense query execution, and Reciprocal Rank Fusion (RRF with k=60).
  - `app/services/reranker.py`: Cross-encoder neural reranking via BAAI/bge-reranker-base.
  - `app/services/verification.py`: Claim extraction, NLI-based claim verification, citation extraction, bracket alignment.
  - `app/services/refinement.py`: Iterative synthesis refinement loop for grounding improvement.
  - `app/core/config.py`: Authoritative LLM runtime configuration (Gemini 2.5 Flash, temperature 0.0).
- **research_artifacts/**: Historical experiment records (E01-E10), frozen benchmarks (ds_nexus_v11), legacy freeze tables.
- **evaluation/**:
  - `audit/`: Phase 0 pre-experiment audit and historical readiness checks.
  - `module_01/`: Canonical frozen retrieval benchmark run (15 test queries, BM25, Dense, RRF, Reranker).
  - `module_02/`: Canonical frozen answer grounding and claim verification (56 claims, factual vs refusal taxonomy).
  - `module_03/`: Canonical frozen citation validation and repair evaluation (CitationRepair coverage & safety analysis).
  - `publication_audit_v2/`: Current master publication audit and reconciliation package.

## 3. Core Component Verification
| Component | Implementation File | Verified State | Notes |
| :--- | :--- | :---: | :--- |
| Lexical Retrieval | `backend/app/services/hybrid_search.py` | VERIFIED | Uses rank_bm25 Okapi BM25 |
| Dense Retrieval | `backend/app/services/vector_store.py` | VERIFIED | BAAI/bge-base-en-v1.5, 768 dims |
| Hybrid Fusion | `backend/app/services/hybrid_search.py` | VERIFIED | RRF k=60 |
| Reranker | `backend/app/services/reranker.py` | VERIFIED | BAAI/bge-reranker-base |
| Claim Verifier | `backend/app/services/verification.py` | VERIFIED | NLI-based claim grounding |
| Citation Repair | `backend/app/services/citation_repair.py` | VERIFIED | Deterministic candidate matching |
"""

with open(os.path.join(AUDIT_DIR, 'repository_inventory.md'), 'w', encoding='utf-8') as f:
    f.write(repo_inv)

# 2. baseline_integrity_report.md
base_rep = """# Baseline Integrity Report

## 1. Overview
Audit of baseline configurations across retrieval, generation, verification, and repair pipelines to ensure benchmark integrity and eliminate methodological artifacts.

## 2. Model & Runtime Integrity
- **Frozen Generator LLM**: `gemini-2.5-flash` (Google GenAI SDK)
- **Temperature**: `0.0` (Deterministic greedy decoding)
- **Embedding Model**: `BAAI/bge-base-en-v1.5` (768 dimensions, cosine similarity)
- **Reranker Model**: `BAAI/bge-reranker-base` (Cross-encoder sequence pair classification)
- **Benchmark Split**: `ds_nexus_v11` (N=100: DEV=70, VAL=15, TEST=15)

## 3. Discrepancy Reconciliation
1. **Model Name Ambiguity**: Historical drafts informally noted "Gemini 3.5 Flash Lite" or "gemini-1.5-flash". Codebase inspection confirms the actual execution engine is `gemini-2.5-flash`.
2. **Benchmark Query Split**: Exactly 15 TEST queries (`item_v11_086` through `item_v11_100`). Five are unanswerable/adversarial queries designed to test epistemic abstention.
3. **Retrieval Granularity Conflation**: Paper-level metrics vs Chunk-level metrics must never be mixed in the same table column without explicit granularity annotation.
"""

with open(os.path.join(AUDIT_DIR, 'baseline_integrity_report.md'), 'w', encoding='utf-8') as f:
    f.write(base_rep)

# 3. issues_register.csv
issues = [
    {
        'issue_id': 'ISSUE-001',
        'severity': 'HIGH',
        'category': 'Retrieval Metrics',
        'description': 'Conflation of BM25 paper-level Hit@20 (0.6667) and chunk-level Recall@20 (0.0000) in legacy drafts',
        'resolution_status': 'RESOLVED',
        'resolution_action': 'Decomposed retrieval metrics into separate paper-level and chunk-level audit tables with unambiguous unit labels.'
    },
    {
        'issue_id': 'ISSUE-002',
        'severity': 'MEDIUM',
        'category': 'Model Identifier',
        'description': 'Informal text referencing gemini-3.5-flash-lite / gemini-1.5-flash vs actual runtime gemini-2.5-flash',
        'resolution_status': 'RESOLVED',
        'resolution_action': 'Locked all configuration manifests and publication statements to gemini-2.5-flash at temperature 0.0.'
    },
    {
        'issue_id': 'ISSUE-003',
        'severity': 'HIGH',
        'category': 'Grounding Taxonomy',
        'description': 'Refusal penalty confound where epistemic abstention on unanswerable queries was scored as ungrounded hallucination',
        'resolution_status': 'RESOLVED',
        'resolution_action': 'Adopted Revision 01 epistemic taxonomy separating factual assertions from epistemic abstentions.'
    },
    {
        'issue_id': 'ISSUE-004',
        'severity': 'HIGH',
        'category': 'Human Ground Truth',
        'description': 'Absence of external double-blind human ground-truth annotation for scientific claim verification',
        'resolution_status': 'BLOCKED_DOCUMENTED',
        'resolution_action': 'Classified human grounding evaluation as HUMAN_VALIDATION_BLOCKED / NOT_MEASURED. Created blinded annotation package.'
    },
    {
        'issue_id': 'ISSUE-005',
        'severity': 'MEDIUM',
        'category': 'Citation Repair Safety',
        'description': 'Over-claiming citation repair effectiveness when 0 repairs were safely applied due to multi-chunk candidate ambiguity',
        'resolution_status': 'RESOLVED',
        'resolution_action': 'Locked findings to: Citation improvement NOT OBSERVED, Repair effectiveness NOT DEMONSTRATED, Safety NOT ESTIMABLE.'
    },
    {
        'issue_id': 'ISSUE-006',
        'severity': 'MEDIUM',
        'category': 'Latency Boundary',
        'description': 'Conflation of model generation time with post-hoc verification, citation repair, and NLI overhead',
        'resolution_status': 'RESOLVED',
        'resolution_action': 'Decomposed latency reporting into First-Stage Retrieval, LLM Generation, and Verification Overhead.'
    }
]

with open(os.path.join(AUDIT_DIR, 'issues_register.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['issue_id', 'severity', 'category', 'description', 'resolution_status', 'resolution_action'])
    writer.writeheader()
    writer.writerows(issues)

# 4. experiment_manifest.json
exp_manifest = {
    'audit_version': 'publication_audit_v2',
    'timestamp': '2026-10-17T05:40:00Z',
    'benchmark': {
        'name': 'ds_nexus_v11',
        'total_queries': 100,
        'splits': {'DEV': 70, 'VAL': 15, 'TEST': 15},
        'unanswerable_queries_test': ['item_v11_086', 'item_v11_087', 'item_v11_088', 'item_v11_089', 'item_v11_090']
    },
    'runtime_models': {
        'generator_llm': 'gemini-2.5-flash',
        'temperature': 0.0,
        'embedding_dense': 'BAAI/bge-base-en-v1.5',
        'reranker_cross_encoder': 'BAAI/bge-reranker-base',
        'rrf_k': 60
    },
    'frozen_modules': {
        'module_01': {'domain': 'Retrieval Baselines & Ablation', 'status': 'FROZEN'},
        'module_02': {'domain': 'Answer Grounding & Claim Taxonomy', 'status': 'FROZEN_REVISION_01'},
        'module_03': {'domain': 'Citation Validation & Repair', 'status': 'FROZEN_REVISION_01'}
    }
}

with open(os.path.join(AUDIT_DIR, 'experiment_manifest.json'), 'w', encoding='utf-8') as f:
    json.dump(exp_manifest, f, indent=2)

print('Phase P0 core governance artifacts successfully generated.')
