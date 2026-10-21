# E03.3 Final Validation Report

## 1. Executive Summary & Validation Decision

This report documents the final validation of candidate recall curve semantics under **E03.3: Cutoff Prefix Consistency Validation**.

```
NO_RERUN_REQUIRED = FALSE
E03_STATUS = E03_CANONICAL_CONFIRMED_WITH_MINOR_CORRECTION
```

---

## 2. Cutoff Prefix Consistency Audit Findings

1. **Prefix Match Rates**:
   - Out of 900 query/config/cutoff comparisons between live $k$-specific outputs and $k=50$ prefixes, **534 checks (59.3%) matched exactly**, while **366 checks (40.7%) exhibited minor sequence reorderings**.
   - **Cause**: RRF fusion over small cutoffs ($k=5$) limits candidate depth prior to fusion, resulting in minor rank shifts compared to merging top-50 candidate lists.
2. **Authoritative Correction**:
   - Rather than relying on $k=50$ prefixes, the authoritative canonical dataset (`e03_3_canonical_results_live.json`) was recomputed **strictly from live $k$-specific retrieval outputs** for each cutoff depth ($k \in \{5, 10, 20, 50\}$).

---

## 3. Identifier Normalization Audit

- **BM25 & Hybrid Chunk Parsing**: All 1,000 candidate IDs containing `_chunk_` successfully parsed into canonical `paper_res_XXX` paper IDs.
- **Dense Unmapped String IDs**: Chroma returned unmapped string IDs (e.g. `local:Artificial_Intelligence:...`) for 5 TEST queries (`item_v11_096` to `item_v11_100`).
- **Audit Policy**: These unmapped IDs were preserved as unmapped string IDs and **NOT forcibly converted** into valid paper IDs.

---

## 4. Authoritative `first_gold_k` & Downstream E04 Cohort Sizes (`B3_Hybrid_RRF`)

Using the live $k$-specific canonical evaluation dataset:

| Cutoff Scope ($k$) | Overall Benchmark ($N=100$) | TEST Split ($N=15$) | Downstream E04 RAG Generation Context Status |
| :--- | :--- | :--- | :--- |
| **Top-5 Context ($k=5$)** | **30 / 100 (30.0%)** | **5 / 15 (33.3%)** | Strict top-5 RAG context |
| **Top-10 Context ($k=10$)** | **62 / 100 (62.0%)** | **5 / 15 (33.3%)** | Standard top-10 RAG context |
| **Top-20 Context ($k=20$)** | **100 / 100 (100.0%)** | **15 / 15 (100.0%)** | Deep top-20 RAG context (**100% evidence-eligible**) |
| **Top-50 Context ($k=50$)** | **100 / 100 (100.0%)** | **15 / 15 (100.0%)** | Max candidate depth |

---

## 5. Summary Verdict

```
E03_STATUS = E03_CANONICAL_CONFIRMED_WITH_MINOR_CORRECTION
```

The canonical candidate-recall dataset is validated and locked based strictly on live $k$-specific retrieval outputs.

**STOPPING EXECUTION. E04 will not be launched.**
