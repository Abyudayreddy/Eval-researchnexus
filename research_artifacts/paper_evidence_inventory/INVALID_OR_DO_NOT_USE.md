# Invalid or Do-Not-Use Artifacts Registry

## 1. Overview

This registry lists all experimental artifacts, dataset versions, and metric logs that have been audited and explicitly classified as **`INVALID_DO_NOT_USE`**.

---

## 2. Invalid Artifact Registry Table

| Artifact Path | Description | Audit Discovery Date | Root Cause / Reason for Invalidation | Replacement Artifact |
| :--- | :--- | :--- | :--- | :--- |
| `retrieval_evaluation/module_1_5/diagnostic_matrix.csv` | Legacy `ds_nexus_v10` retrieval audit | Module 1.5 Audit | Synthetic query template mismatch & retriever-dependent gold labels in benchmark v10 | `v11/e01/raw/e01_raw_per_query.json` |
| `retrieval_evaluation/e02_aggregate_results.json` (Legacy) | Legacy BGE reranking aggregate log | Module 1.8 Audit | BGE Cross-Encoder was bypassed due to empty text candidate dictionaries; reported ~0.004 ms bypass time | `v11/final_latency_analysis.json` & `v11/e02/aggregate/e02_aggregate_results.json` |
| `retrieval_evaluation/v11/module_1_9/candidate_set_equality_full.csv` | Legacy Candidate Set Equality CSV | Module 1.9.1 Audit | Script assigned `b3_cids` directly to `b4_pre_bge` column tautologically | `v11/module_1_9_1/independent_candidate_equality.csv` |
| `retrieval_evaluation/v11/module_1_9/identifier_contract_audit.csv` | Legacy Identifier Contract CSV | Module 1.9.1 Audit | Script constructed representation columns from item expected IDs tautologically | `v11/module_1_9_1/independent_identifier_trace.csv` |

---

## 3. Policy on Invalid Artifacts

Per research integrity rules, all invalid artifacts are retained in the repository history but marked with `INVALID_DO_NOT_USE`. They MUST NEVER be cited in paper drafts or used to support scientific claims.
