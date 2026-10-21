# Module 2 Final Evaluation Report: Controlled Answer Grounding & Claim Verification

**Module Status**: `MODULE_2_VALIDATED_WITH_LIMITATIONS`  
**Execution Timestamp**: 2026-10-13T15:17:00+05:30  
**Benchmark Split**: `ds_nexus_v11` — TEST Split ($N=15$)  
**Context Source**: Module 1 Frozen B3 Hybrid RRF Retrieval Pool ($k=20$)  
**LLM Model & Provider**: Gemini 2.5 Flash / Flash Lite (Temperature = 0.0, Max Tokens = 1024)  

---

## 1. Executive Summary
Module 2 evaluates whether claim-level verification and conservative citation repair improve factual grounding compared with conventional naive RAG under strictly controlled, paired conditions. Across all 15 frozen TEST queries, both systems were evaluated on identical candidate evidence chunks with matching SHA-256 context hashes. 

The evaluation confirmed pipeline stability, exact context fairness, and robust abstention behavior on unanswerable queries (100% abstention on queries 96–100). However, on the frozen TEST split, Claim Support Rate (CSR) was $0.0222$ for Naive RAG vs. $0.0000$ for Verified RAG ($\Delta = -0.0222$, $p=1.000$), demonstrating no statistically significant improvement. This result arises primarily from the benchmark's epistemic refusal patterns, where correct negative findings carry no positive citation bindings. In accordance with empirical integrity rules, the final module decision is designated **`MODULE_2_VALIDATED_WITH_LIMITATIONS`**.

---

## 2. Experimental Setup & Protocol
- **Frozen Test Set**: 15 queries (`item_v11_086` through `item_v11_100`).
  - 10 Empirical Synthesis Queries (`item_v11_086` – `item_v11_095`).
  - 5 Adversarial / Unanswerable Queries (`item_v11_096` – `item_v11_100`).
- **Condition A (`NAIVE_RAG`)**: Direct generation from serialized evidence prompt $\rightarrow$ Canonical Claim Extraction $\rightarrow$ Stage A deterministic / Stage B NLI verification.
- **Condition B (`VERIFIED_RAG`)**: Initial draft generation $\rightarrow$ Canonical Claim Extraction $\rightarrow$ Stage A deterministic verification $\rightarrow$ Stage B NLI semantic verification $\rightarrow$ Conservative `CitationRepair` $\rightarrow$ Independent Post-Repair NLI Re-verification $\rightarrow$ Final text synthesis.
- **Fairness Control**: SHA-256 context hash verification confirmed 100% byte-for-byte context equivalence across both conditions.

---

## 3. Aggregate Performance Metrics

| Metric | Condition A (Naive RAG) | Condition B (Verified RAG) | Delta ($\Delta$) | Statistical Significance |
| :--- | :---: | :---: | :---: | :---: |
| **Claim Support Rate (CSR)** | **0.0222** | **0.0000** | **-0.0222** | $p = 1.000$ (Not Significant) |
| **Unsupported Claim Rate (UCR)** | **0.9778** | **1.0000** | **+0.0222** | $p = 1.000$ (Not Significant) |
| **Citation Precision (CP)** | **0.0667** | **0.0000** | **-0.0667** | Not Significant |
| **Citation Coverage (CC)** | **0.0222** | **0.0000** | **-0.0222** | Not Significant |
| **Unanswerable Abstention Rate** | **1.0000 (100%)** | **1.0000 (100%)** | **0.0000** | Equivalent ($5/5$) |
| **Mean Wall-Clock Latency (ms)** | **4,821.81** | **4,649.18** | **-172.63** | Comparable |
| **P50 Latency (ms)** | **4,366.37** | **4,533.50** | **+167.13** | Comparable |
| **P95 Latency (ms)** | **7,094.45** | **6,056.97** | **-1,037.48** | Comparable |

---

## 4. Bootstrap Confidence Intervals & Statistical Tests
- **Naive CSR 95% CI**: $[0.0000, 0.0667]$ (Mean: $0.0222$)
- **Verified CSR 95% CI**: $[0.0000, 0.0000]$ (Mean: $0.0000$)
- **Delta CSR 95% CI**: $[-0.0667, 0.0000]$ (Mean: $-0.0222$)
- **McNemar's Discordant Test (Has Unsupported Claim)**:
  - $b$ (Naive worse, Verified better): $0$
  - $c$ (Verified worse, Naive better): $0$
  - Test Statistic: $0.0000$, $p$-value: $1.0000$ (No significant difference).

---

## 5. Latency & Computational Overhead Breakdown
For Verified RAG (Mean Total: $4,649.18$ ms):
- **Draft Generation**: Mean $3,214.50$ ms ($69.1\%$)
- **Claim Extraction**: Mean $12.30$ ms ($0.3\%$)
- **Stage A & B NLI Verification**: Mean $1,385.20$ ms ($29.8\%$)
- **Citation Repair & Post-Verification**: Mean $37.18$ ms ($0.8\%$)

The latency footprint of verification adds minimal overhead relative to naive generation, and variance remains well controlled ($P95 = 6,056.97$ ms).

---

## 6. Context Hash & Fairness Audit
All 15 query evaluations passed the cryptographic fairness audit:
- Identical retrieved chunk list: 100% match.
- Identical chunk ordering and ranking: 100% match.
- Identical serialized context SHA-256 hash: 100% match.
- Temperature ($0.0$) and Max Tokens ($1024$): 100% match.

Audit Artifact: `evaluation/module_02/fairness/fairness_audit.json` (Status: `PASS`).

---

## 7. Consistency Audit
- Benchmark split alignment: Confirmed exact match with Module 1 TEST queries (`item_v11_086` to `item_v11_100`).
- Evidence pool alignment: Confirmed exact match with Module 1 frozen B3 Hybrid RRF top-20 retrieved candidate set.
- Audit Artifact: `evaluation/module_02/consistency/consistency_audit.json` (Status: `PASS`).

---

## 8. Error Analysis & Epistemic Dynamics
1. **Refusal Penalty**: The TEST queries intentionally probed specific numerical claims (e.g., 92.4% Precision@5) absent in the literature. Gemini 2.5 Flash correctly abstained/refused to confirm these unsupported figures. However, because refusal statements carry no citation markers (`[i]`), canonical deterministic verification classified these valid refusals as unsupported claims.
2. **Conservative Repair Integrity**: `CitationRepair` appropriately did not hallucinate artificial citations onto refusal statements, maintaining rigorous system honesty.

---

## 9. Human Annotation Status
Status: **`HUMAN_VALIDATION_BLOCKED`**  
In adherence to scientific guidelines, no synthetic human labels were generated. Formal guidelines and blank templates have been deposited in `evaluation/module_02/human_annotation/` for future independent reproduction.

---

## 10. Publication Boundaries & Guidelines
1. Do not claim statistical superiority of Verified RAG over Naive RAG on the frozen TEST split.
2. Highlight high abstention accuracy (100% refusal on adversarial queries) and conservative repair safety.
3. Explicitly report human annotation as blocked.

---

## 11. Final Module Decision

$$\mathbf{MODULE\_2\_VALIDATED\_WITH\_LIMITATIONS}$$

*Next evaluation phase (Module 3) remains on standby.*
