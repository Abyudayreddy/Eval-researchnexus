# E03.1 Final Reconciliation & Metric Validation Report

## 1. Executive Summary & Status

This report completes **E03.1: Candidate Recall Reconciliation & Metric Validation** for ResearchNexus.

```
E03_FINAL_STATUS = E03_VERIFIED_WITH_CORRECTION
```

---

## 2. Key Reconciliation & Correction Accomplishments

1. **E01 vs. E03 Reconciliation**:
   - Reconciled E01 $k=5$ and E03 $k=5$ outputs across all 100 queries. Identified that paper-level deduplication timing (deduplicating chunks before selecting top-$k$ paper IDs) accounts for the slight $+0.0500$ recall shift in E03.
2. **Corrected `first_gold_k` Evaluation**:
   - Fixed the `first_gold_k` diagnostic by calculating minimum rank across **ALL `expected_paper_ids`** (rather than just `gold_pids[0]`).
   - Re-evaluated B3_Hybrid_RRF evidence eligibility: **25% at $k=5$**, **57% at $k=10$**, and **95% at $k=20$** overall (**66.7% at $k=20$ on TEST**).
3. **Cutoff & Aggregation Semantics**:
   - Documented exact chunk-to-paper deduplication sequence and verified that $k \in \{5, 10, 20, 50\}$ are unpadded live retrieval calls.
4. **Downstream E04 Cohort Recommendations**:
   - Formally documented top-5, top-10, and top-20 evidence-eligible query counts to inform E04 generation evaluation.

---

## 3. Index of Reconciliation Artifacts

All E03.1 reconciliation files are available in `research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/reconciliation/`:
- [e01_vs_e03_reconciliation.md](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/reconciliation/e01_vs_e03_reconciliation.md)
- [e03_1_corrected_first_gold_k.csv](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/reconciliation/e03_1_corrected_first_gold_k.csv)
- [e03_1_independent_metric_check.json](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/reconciliation/e03_1_independent_metric_check.json)
- [e03_1_cutoff_semantics.md](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/reconciliation/e03_1_cutoff_semantics.md)
- [e03_1_paper_chunk_aggregation.md](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/reconciliation/e03_1_paper_chunk_aggregation.md)
- [e03_1_downstream_cohort_analysis.md](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/reconciliation/e03_1_downstream_cohort_analysis.md)
- [E03_1_FINAL_RECONCILIATION_REPORT.md](file:///c:/Users/Abyureddy/OneDrive/Desktop/SDC2/research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/reconciliation/E03_1_FINAL_RECONCILIATION_REPORT.md)

---

```
E03_FINAL_STATUS = E03_VERIFIED_WITH_CORRECTION
```

**STOPPING EXECUTION. E04 will not be launched.**
