# Protocol Amendment V1.1 (Master Document)

## 1. Executive Summary

This document represents the official **Methodological Amendment V1.1** to the frozen ResearchNexus experimental protocol.

All V1.0 documents in `research_artifacts/paper_experiment_protocol/` remain intact and unchanged.

---

## 2. Summary of Protocol V1.1 Corrections

1. **Claim Verification Metrics**:
   - Replaced ambiguous overall accuracy string with per-class Precision, Recall, F1 across 4 NLI classes (`SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNSUPPORTED`, `CONTRADICTED`).
   - Added Macro-aggregated Precision/Recall/F1 and $4 \times 4$ Confusion Matrix.
   - Defined dedicated Unsupported/Contradicted Claim Detection Precision, Recall, and F1.

2. **Generation Comparison Statistics**:
   - Defined bootstrap 95% confidence intervals and Chi-square / Fisher's tests for independent claim sets.
   - Restricted McNemar's test strictly to paired query-level binary outcomes.

3. **Human Evaluation Scope**:
   - Explicitly separated Automated Evaluation ($N=100$) from Human-Grounded Evaluation ($N=30$) and TEST Human Evaluation ($N=15$).

4. **Secondary Citation Metric**:
   - Added Citation Coverage ($\text{claims with valid citations} / \text{claims requiring citation}$) alongside Citation Precision and Citation Completeness.

5. **Ablation Matrix Repair**:
   - Replaced confounded ablations with single-factor interventions A0–A6 isolating Iteration, Citation Repair, Verification, BGE, and Retrieval.

6. **Expanded XAI Provenance**:
   - Defined Local Database Trace Chain and Online Web Search Trace Chain down to raw provider/chunk offsets.

7. **Dual-Cohort Generation Policy**:
   - Established Cohort A (Full Benchmark $N=100$) and Cohort B (Evidence-Eligible Subset) reporting rules.

---

## 3. Protocol Status

```
PROTOCOL_V1_1_STATUS = AMENDED_AND_READY
```
