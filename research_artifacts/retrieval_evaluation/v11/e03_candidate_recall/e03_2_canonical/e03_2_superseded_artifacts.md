# E03.2 Superseded Artifacts Registry

## 1. Overview

This document records the official list of historical retrieval evaluation artifacts that have been superseded by the **Canonical Paper-Level Evaluation Semantics (E03.2)**.

---

## 2. Superseded Artifacts Registry Table

| Artifact Path | Superseded Metric / Content | Superseded By | Reason for Supersedence | Classification Status |
| :--- | :--- | :--- | :--- | :--- |
| `retrieval_evaluation/v11/e01/e01_results.md` | Legacy E01 multi-chunk raw paper list metrics | `e03_2_e01_canonical_recomputed.json` & `E03_CANONICAL_SUMMARY.md` | Legacy E01 evaluated raw chunk paper extractions without pre-cutoff paper-level deduplication | `SUPERSEDED_BY_CANONICAL_PAPER_LEVEL_EVALUATION` |
| `retrieval_evaluation/v11/e01/aggregate/e01_aggregate_results.json` | Legacy E01 aggregate JSON | `e03_2_e01_canonical_recomputed.json` | Multi-chunk raw paper lists caused minor metric discrepancies ($+0.0500$) | `SUPERSEDED_BY_CANONICAL_PAPER_LEVEL_EVALUATION` |
| `retrieval_evaluation/v11/e03_candidate_recall/e03_first_gold_k.csv` | Early E03 `first_gold_k` CSV | `e03_2_first_gold_k_authoritative.csv` | Used `gold_pids[0]` single-gold paper lookup instead of minimum rank across ALL `expected_paper_ids` | `SUPERSEDED_BY_CANONICAL_PAPER_LEVEL_EVALUATION` |
| `retrieval_evaluation/v11/e03_candidate_recall/e03_aggregate_results.json` | Unreconciled E03 aggregate JSON | `e03_2_canonical_results.json` | Superseded by canonical paper-level recomputation | `SUPERSEDED_BY_CANONICAL_PAPER_LEVEL_EVALUATION` |

---

## 3. Publication Policy

Per scientific audit rules, legacy files remain preserved in the repository history. However, any citation in future paper drafts MUST use the authoritative values from `E03_CANONICAL_SUMMARY.md` and `e03_2_canonical_results.json`.
