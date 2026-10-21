# ResearchNexusAI — V4 Canonical Evaluation Results

> **Authoritative Package:** `evaluation/Re-evaluation of mistakes/`  
> **Source Script:** `evaluation/publication_audit_v2/v4_reconciliation/reproduce_v4.py`  
> **Evaluation Split:** Canonical TEST Split ($N = 15$) on `ds_nexus_v11`  

---

## 1. Canonical Retrieval Performance (TEST Split, $N = 15$)

*Source:* `evaluation/Re-evaluation of mistakes/canonical_retrieval_metrics.csv`

| Strategy | Hit@5 (All 15) | Hit@10 (All 15) | Hit@20 (All 15) | Recall@20 (Ans 10) | MRR (All 15) | MRR (Ans 10) | NDCG@20 | Latency p50 |
|---|---|---|---|---|---|---|---|---|
| **B1: BM25 Lexical** | 0.0000 | 0.6667 (10/15) | **0.6667 (10/15)** | **1.0000 (10/10)** | 0.0759 | 0.1139 | 0.2026 | 0.69 ms |
| **B2: Dense Chroma (BGE-Base)** | 0.0000 | 0.0000 | **0.0000 (0/15)** | **0.0000 (0/10)** | 0.0000 | 0.0000 | 0.0000 | 13.51 ms |
| **B3: Hybrid RRF ($k=60$)** | 0.0000 | 0.0000 | **0.6667 (10/15)** | **1.0000 (10/10)** | 0.0431 | 0.0647 | 0.1648 | 6.56 ms |
| **B4: BGE Cross-Encoder Rerank** | 0.0000 | 0.0000 | **0.6667 (10/15)** | **1.0000 (10/10)** | 0.0480 | 0.0720 | 0.1708 | 535.06 ms |

> 📌 **Key Findings:**
> - **Hit@20 is 10/15 (66.7%)** because items `item_v11_096`–`100` are true unanswerable queries with no gold chunks.
> - **Recall@20 on answerable queries is 10/10 (100.0%)** for BM25, Hybrid, and BGE Rerank.
> - BGE Reranking provides a modest rank promotion (MRR 0.0431 $\rightarrow$ 0.0480). Historical claims of MRR 0.5444 / +47.7% gain are **withdrawn**.

---

## 2. Canonical Claim Grounding & Verification

*Source:* `evaluation/Re-evaluation of mistakes/canonical_grounding_metrics.json`

- **Total Candidate Sentences Extracted across TEST Split:** 56 sentences
  - **Appropriate Abstentions:** 30 sentences (53.6%)
  - **Insufficient-Evidence Findings:** 19 sentences (33.9%)
  - **Factual Assertions:** **7 sentences** (12.5%)

### Automated NLI Precision:
- **Naive RAG:** 4 factual claims asserted $\rightarrow$ 4 supported $\rightarrow$ **100.0% automated NLI precision (4/4)**
- **Verified RAG:** 3 factual claims asserted $\rightarrow$ 3 supported $\rightarrow$ **100.0% automated NLI precision (3/3)**

> 📝 **Audited Scientific Limitation:** The factual assertion sample size is small ($N=7$ claims across the TEST split). Human ground-truth validation was NOT measured ($N=0$ human annotators) and is designated as future work.

---

## 3. Audited Citation Repair Findings (Module 3 Lock)

*Source:* `evaluation/Re-evaluation of mistakes/canonical_claim_accounting.csv`

- **Citation Improvement:** **NOT OBSERVED**
- **Repair Effectiveness:** **NOT DEMONSTRATED**
- **Applied Repairs:** **0** (4 candidate repairs rejected due to 10-chunk ambiguity).
- **Successful-Repair Safety:** **NOT ESTIMABLE** (0 applied repairs).
- **Observed Test Baseline:** **20.0% citation coverage (1 out of 5 eligible factual claims grounded)** across C0, C1, and C2 conditions.
