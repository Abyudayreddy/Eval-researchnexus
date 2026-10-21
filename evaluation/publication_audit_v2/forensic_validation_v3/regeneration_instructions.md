# Deterministic Metric Regeneration Instructions (V3)

## 1. Overview
This document specifies how an independent researcher can deterministically verify and recalculate every publication-approved metric in `validated_results_v3.json` directly from the raw experimental records without executing new LLM or embedding API calls.

## 2. Input Artifacts and Verification Hashes
Ensure the following files are present and match their SHA-256 hashes:
1. `research_artifacts/benchmark_v11/benchmark_items.json` (`8be898396a3821c902d3fb5f095ca964c17c1dcb437125e05524d13d42c51d40`)
2. `research_artifacts/retrieval_evaluation/v11/e01/raw/e01_raw_per_query.json` (`6f546f96859f53f3ebfa7545436fb7c62e2c736e092184df94d64658d82cd248`)
3. `evaluation/module_01/metrics/paper_level_metrics.json` (`ac142c9094b45c61454149ef7604ad10b35045a4193eca1fc57bc37220159838`)
4. `evaluation/module_02/revision_01/corrected_metrics.json` (`6e8438aad485397a0b2f1af299b154983a7db1eb8e8c0cc3521f577e013787f9`)
5. `evaluation/module_03/analysis/repair_metrics.json` (`45175c57e6482cc0efa0fe14b341788d2bb816ed397818c7241bb857df9cf117`)

## 3. Step-by-Step Regeneration Command
Execute the deterministic recalculation script from the workspace root:

```bash
python evaluation/publication_audit_v2/forensic_validation_v3/deterministic_recalculate.py
```

## 4. Script Verification Output
The script will assert equality between the recomputed values from raw JSON files and the approved entries in `validated_results_v3.json`. Any divergence will trigger an `AssertionError`.
