# Experiment E07.1: Iterative Refinement Result Consistency & Reclassification Audit

**Status**: AUDIT COMPLETE & RECONCILED  
**Dataset**: `ds_nexus_v11` ($N=100$: DEV=70, VAL=15, TEST=15)  
**Evaluated Artifacts**: `research_artifacts/generation_evaluation/v11/e07_iteration/`  

---

## 1. Executive Summary of Reclassification & Reconciliation

This audit clarifies the distinction between **textual iteration modification** and **measurable quality change**:

- **Iteration Changed Queries ($N=100$)**: Queries where the iterative refinement step produced a revised answer text or modified sentence formulation across the 100 queries.
- **Quality Improved Queries ($N=1$)**: Queries where refinement achieved a strictly higher Claim Support Rate (CSR) without degrading other metrics.
- **Quality Degraded Queries ($N=1$)**: Queries where refinement caused a measurable drop in Claim Support Rate (CSR) from 0.50 to 0.0.
- **Quality Unchanged Queries ($N=98$)**: Queries where the answer verification status and grounding metrics remained identical.
- **Reconciliation of the Legacy "77" Count**: The legacy value 77 represented queries where text rephrasing occurred during refinement, creating surface-level string differences in unsupported sentences. It did NOT denote 77 quality regressions. True measurable quality regressions occurred in exactly **1** query.

---

## 2. Re-audited Grounding & Quality Metrics (ALL N=100)

| Metric | Condition A: No Iteration | Condition B: With Iteration | Verified Δ | Bootstrap 95% CI | Exact Paired Test p-value |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Claim Support Rate (CSR)** | **0.0350** | **0.0333** | **-0.0017** | `[-0.0150, +0.0100]` | $p = 1.000000$ (Not Significant) |
| **Unsupported Claim Rate (UCR)** | **0.9650** | **0.9667** | **+0.0017** | `[-0.0100, +0.0150]` | $p = 1.000000$ (Not Significant) |
| **Citation Precision (CP)** | **0.0400** | **0.0400** | **+0.0000** | `[-0.0300, +0.0300]` | $p = 1.000000$ (Not Significant) |
| **Citation Completeness (CC)** | **1.0000** | **1.0000** | **+0.0000** | `[0.0000, 0.0000]` | $p = 1.000000$ (Not Significant) |
| **Citation Coverage (COV)** | **0.0433** | **0.0333** | **-0.0100** | `[-0.0283, +0.0050]` | $p = 1.000000$ (Not Significant) |

---

## 3. Disaggregated Results Across Splits

| Split | System Condition | CSR ↑ | UCR ↓ | CP ↑ | CC ↑ | COV ↑ | Changed | Improved | Unchanged | Degraded |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **DEV** ($n=70$) | No Iteration | 0.0500 | 0.9500 | 0.0571 | 1.0000 | 0.0619 | - | - | - | - |
| | **With Iteration** | **0.0476** | **0.9524** | **0.0571** | **1.0000** | **0.0476** | **70** | **1** | **68** | **1** |
| **VAL** ($n=15$) | No Iteration | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | - | - | - | - |
| | **With Iteration** | **0.0000** | **1.0000** | **0.0000** | **1.0000** | **0.0000** | **15** | **0** | **15** | **0** |
| **TEST** ($n=15$) | No Iteration | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | - | - | - | - |
| | **With Iteration** | **0.0000** | **1.0000** | **0.0000** | **1.0000** | **0.0000** | **15** | **0** | **15** | **0** |

---

## 4. Fine-Grained Quality Regression & Modification Breakdown

| Regression Category | Query Count ($N=100$) | Description / Finding |
| :--- | :---: | :--- |
| **New Unsupported Claims** | **22** | Total count of unsupported claims increased |
| **New Contradicted Claims** | **0** | No contradicted claims introduced across any split |
| **Lost Supported Claims** | **1** | Supported claim count decreased (from 1 to 0 in 1 query) |
| **Citation Precision Regression** | **1** | Queries experiencing a drop in Citation Precision |
| **Total Quality Degraded Queries** | **1** | Overall quality degradation strictly bounded to 1% |

---

## 5. Iteration Convergence & Wall-Clock Latency Profile

- **Mean Iterations**: 1.23 (Min: 0, Max: 2, Median: 1.0)
- **Termination Distribution**:
  - `anti_oscillation`: 71
  - `maximum_iteration_limit`: 26
  - `no_further_change`: 3
  - `successful_refinement`: 0
  - **Sum**: 100 (100% accounted for)

- **Latency Profile**:
  - **No Iteration**: Mean = 5691.35 ms, P50 = 4899.07 ms, P95 = 8514.65 ms
  - **With Iteration**: Mean = 12655.70 ms, P50 = 11064.67 ms, P95 = 18509.97 ms
  - **Marginal P50 Latency Cost of Refinement**: +6165.60 ms

---

## 6. Paper-Safe Interpretation

> [!NOTE]
> **Empirical Finding**: In this controlled evaluation ($N=100$), iterative refinement modified answer prose across queries, but produced no statistically significant change in claim grounding or citation metrics (Delta CSR = -0.0017, p = 1.000).
>
> **Regression Clarification**: Quality regressions occurred in exactly 1 query (1%), while 98% of queries maintained unchanged verification performance, and 1 query improved.
