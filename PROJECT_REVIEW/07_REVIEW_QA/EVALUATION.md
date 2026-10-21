# ResearchNexusAI — Evaluation Questions

### 1. What is the authoritative reproduction script?
- **Answer:** `evaluation/publication_audit_v2/v4_reconciliation/reproduce_v4.py`.

### 2. What are the key retrieval performance numbers?
- **Answer:** On the canonical 90-item benchmark:
  - BM25 Hit@20: 0.778
  - Dense Hit@20: 0.811
  - Hybrid RRF Hit@20: 0.867 (78/90)

### 3. What are the grounding metrics for Enhanced RAG?
- **Answer:** Grounding Precision of 88.4% and Grounding Recall of 81.2%, significantly outperforming Naive RAG (61.2% precision).

### 4. What was the audited finding regarding Citation Repair (Module 3)?
- **Answer:** Citation coverage was frozen at 20.0% (1/5 eligible claims) across conditions C0, C1, and C2. The finding was formally locked as: Citation improvement: NOT OBSERVED; Repair effectiveness: NOT DEMONSTRATED; Safety: NOT ESTIMABLE.
