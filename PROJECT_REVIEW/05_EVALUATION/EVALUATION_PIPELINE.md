# ResearchNexusAI — Evaluation Pipeline Execution

> **Master Reproduction Entry Point:** `reproduce_v4.py`  

---

## 1. How to Reproduce All Results
Execute the canonical V4 reproduction script:
```bash
python evaluation/publication_audit_v2/v4_reconciliation/reproduce_v4.py
```

## 2. Pipeline Stages Evaluated
1. **Module 1 (Retrieval):** BM25, Chroma Dense, Hybrid RRF, and BGE Reranker Hit@k, MRR@k, NDCG@k metrics across the 90 benchmark items.
2. **Module 2 (Generation & Grounding):** Naive vs. Enhanced RAG precision and recall evaluation.
3. **Module 3 (Citation & Repair):** Formal claim accounting verifying the 1/5 eligible claims result and 20.0% coverage baseline.
4. **Latency Benchmarking:** Millisecond timer instrumentation for CPU/GPU inference.
