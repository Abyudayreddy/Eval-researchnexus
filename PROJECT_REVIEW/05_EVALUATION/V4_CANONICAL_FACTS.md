# ResearchNexusAI — V4 Canonical Experimental Facts (Authoritative Ground Truth)

> **Status:** ✅ Authoritative V4 Canonical Evidence  
> **Source Directory:** `evaluation/Re-evaluation of mistakes/`  
> **Key Gate Status:** `paper_readiness_gate.md` (READY_WITH_EXPLICIT_LIMITATIONS)  

---

## 1. Canonical Dataset & Split Definitions

- **Benchmark Name:** `ds_nexus_v11`
- **Total Dataset Size:** $N = 100$ items
- **Split Distribution:**
  - **DEV Split:** 70 items (`item_v11_001` through `item_v11_070`)
  - **VAL Split:** 15 items (`item_v11_071` through `item_v11_085`)
  - **TEST Split:** **15 items** (`item_v11_086` through `item_v11_100`)
- **Canonical TEST Split Breakdown ($N = 15$):**
  - **10 Answerable Items:**
    - `item_v11_086`–`090`: Multi-document Synthesis
    - `item_v11_091`–`095`: Adversarial distractor queries
  - **5 Unanswerable Items:**
    - `item_v11_096`–`100`: True unanswerable queries (have zero gold papers/chunks)

> ⚠️ **Denominator Rule:**
> - **Hit@k** uses all **15 TEST queries** (denominator = 15).
> - **Recall@20** uses only the **10 answerable queries** (denominator = 10).
> - **MRR** uses all **15 queries** unless explicitly designated as answerable-only.

---

## 2. Authoritative Retrieval Metrics (TEST Split, $N=15$)

*Source:* `evaluation/Re-evaluation of mistakes/canonical_retrieval_metrics.csv`

| Strategy | Hit@5 (All 15) | Hit@10 (All 15) | Hit@20 (All 15) | Recall@20 (Ans 10) | MRR (All 15) | MRR (Ans 10) | NDCG@20 (All 15) | Latency p50 |
|---|---|---|---|---|---|---|---|---|
| **B1: BM25 Lexical** | 0.0000 | 0.6667 (10/15) | **0.6667 (10/15)** | **1.0000 (10/10)** | 0.0759 | 0.1139 | 0.2026 | 0.69 ms |
| **B2: Dense Chroma (BGE-Base)** | 0.0000 | 0.0000 | **0.0000 (0/15)** | **0.0000 (0/10)** | 0.0000 | 0.0000 | 0.0000 | 13.51 ms |
| **B3: Hybrid RRF ($k=60$)** | 0.0000 | 0.0000 | **0.6667 (10/15)** | **1.0000 (10/10)** | 0.0431 | 0.0647 | 0.1648 | 6.56 ms |
| **B4: BGE Cross-Encoder Rerank** | 0.0000 | 0.0000 | **0.6667 (10/15)** | **1.0000 (10/10)** | 0.0480 | 0.0720 | 0.1708 | 535.06 ms |

### Key Reconciled Findings:
1. **Hit@20 is 66.7% (10/15 queries)** across BM25, Hybrid RRF, and BGE Rerank. The remaining 5 queries are unanswerable queries that legitimately have 0 hits.
2. **Recall@20 on answerable queries is 100.0% (10/10 queries)** for BM25, Hybrid, and BGE Rerank.
3. **Dense Chroma alone failed on this TEST split:** Achieved 0/15 hits in Top-20. The older report claiming 0.6000 was synthetic.
4. **BGE Reranker improvement is modest:** BGE reranking shifts MRR from 0.0431 to 0.0480 (+0.0049 absolute shift). The historical claim of MRR 0.5444 (+47.7% gain) was synthetic and is **permanently withdrawn**.

---

## 3. Authoritative Factual Grounding & Epistemic Metrics

*Source:* `evaluation/Re-evaluation of mistakes/canonical_grounding_metrics.json`

- **Total Candidate Sentences Extracted across TEST Split:** 56 sentences
- **Epistemic Sentence Classification:**
  - **Appropriate Abstentions:** 30 sentences (53.6%)
  - **Insufficient-Evidence Findings:** 19 sentences (33.9%)
  - **Factual Assertions:** **7 sentences** (12.5%)

### System Factual Assertions & Automated NLI Precision:
- **Naive RAG:** 4 factual assertions asserted $\rightarrow$ 4 supported $\rightarrow$ **Automated NLI Precision = 100.0% (4/4)**
- **Verified RAG:** 3 factual assertions asserted $\rightarrow$ 3 supported $\rightarrow$ **Automated NLI Precision = 100.0% (3/3)**

> 📝 **Critical Limitation to State in Review/Paper:**
> The factual assertion sample size is **$N=7$ claims total**. Do NOT claim generalized 100% factual accuracy. Precision is 100% under automated NLI specifically for these 7 evaluated claims.

### Unanswerable Query Abstention:
- **Refusal Count:** **5 out of 5** unanswerable queries (100.0% abstention accuracy).

### Human Ground-Truth Grounding:
- **Status:** **BLOCKED / NOT MEASURED (0 human annotators).**
- Must be explicitly designated as future work.

---

## 4. Authoritative Citation Repair Findings (Module 3 Lock)

*Source:* `evaluation/Re-evaluation of mistakes/canonical_claim_accounting.csv` & `v4_reconciliation_report.md`

- **Observed Test Baseline:**
  - Citation Improvement: **NOT OBSERVED**
  - Repair Effectiveness: **NOT DEMONSTRATED**
  - Successful-Repair Safety: **NOT ESTIMABLE** (Denominator is 0 applied repairs)
- **Applied Repairs:** **0** (4 candidate repairs were conservatively rejected due to 10-chunk ambiguity).
- **Citation Coverage:** Frozen at **20.0% (1 out of 5 eligible claims grounded)** across C0, C1, and C2 conditions.

---

## 5. Authoritative Iterative Refinement Findings (E07 / E07.1)

- **Net Grounding Gain:** **0.0%** (1 query improved, 98 unchanged, 1 degraded; McNemar $p = 1.000$).
- **Latency Penalty:** **+106% latency increase** with zero statistically significant grounding benefit.
- **Scientific Interpretation:** Iterative refinement is an optional safety mechanism, not an empirical quality driver.

---

## 6. Authoritative Latency Results

*Source:* `evaluation/Re-evaluation of mistakes/canonical_latency_results.csv`

| Operation | Scope | Latency p50 | Latency p95 | Notes |
|---|---|---|---|---|
| **BM25 Search** | Component | 0.69 ms | 2.47 ms | In-memory tokenization & scoring |
| **Dense ANN Search** | Component | 13.51 ms | 78.78 ms | Embedding + Chroma cosine distance |
| **Hybrid RRF Fusion** | Component | 6.56 ms | 19.12 ms | Candidate rank combination ($k=60$) |
| **BGE Cross-Encoder** | Component | 531.41 ms | 4246.05 ms | Neural query-passage cross-attention |
| **Hybrid + BGE Pipeline**| Component | 535.06 ms | 4252.00 ms | Total retrieval + rerank stage |
| **Complete RAG Request** | End-to-End | - | - | **Mean = 12.12 s** (LLM generation dominated) |

> ⚠️ **Rule:** Component percentiles are non-additive. Do not add component p50s to calculate end-to-end latency.
