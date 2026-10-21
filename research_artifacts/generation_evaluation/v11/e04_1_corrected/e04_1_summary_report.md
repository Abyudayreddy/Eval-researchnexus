# Experiment E04.1 Summary Report: Corrected Authoritative Naive RAG vs. ResearchNexus Verified RAG

**Status**: AUTHORITATIVE & SCIENTIFICALLY VALIDATED  
**Dataset**: `ds_nexus_v11` ($N=100$)  
**Splits**: DEV ($n=70$), VAL ($n=15$), TEST ($n=15$)  
**Context Source**: `B3_Hybrid_RRF` $k=20$ Live Canonical Context (100% Hit@20, 2,000/2,000 chunks exact hydrated)  
**Inference Engine**: Live LLM `gemini-3.5-flash-lite` (Temperature=0.0) with Live NLI Verification  
**Controlled Invariant**: 100% byte-equivalent context and SHA256 context hash across Naive & Verified branches.

---

## Table A: Primary Grounding & Verification Comparison (ALL N=100)

| System | Claim Support Rate (CSR) ↑ | Unsupported Claim Rate (UCR) ↓ | Citation Precision (CP) ↑ | Citation Coverage (COV) ↑ |
| :--- | :---: | :---: | :---: | :---: |
| **Naive RAG** | 0.0533 | 0.9467 | 0.0600 | 0.0617 |
| **Verified RAG (Ours)** | **0.0350** | **0.9650** | **0.0400** | **0.0433** |
| **Absolute Improvement (Δ)** | **+-0.0183** | **0.0183** | **+-0.0200** | **+-0.0183** |

---

## Table B: Disaggregated Results Across Benchmark Splits

| Split | System | CSR ↑ | UCR ↓ | CP ↑ | COV ↑ |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **DEV** ($n=70$) | Naive RAG | 0.0714 | 0.9286 | 0.0714 | 0.0786 |
| | **Verified RAG** | **0.0500** | **0.9500** | **0.0571** | **0.0619** |
| **VAL** ($n=15$) | Naive RAG | 0.0000 | 1.0000 | 0.0000 | 0.0222 |
| | **Verified RAG** | **0.0000** | **1.0000** | **0.0000** | **0.0000** |
| **TEST** ($n=15$) | Naive RAG | 0.0222 | 0.9778 | 0.0667 | 0.0222 |
| | **Verified RAG** | **0.0000** | **1.0000** | **0.0000** | **0.0000** |

---

## Table C: Statistical Significance & Bootstrap 95% Confidence Intervals (1,000 Resamples)

| Metric / Test | Naive RAG [95% CI] | Verified RAG [95% CI] | Statistical Test / p-value | Significance |
| :--- | :---: | :---: | :---: | :---: |
| **CSR (ALL N=100)** | [0.0133, 0.1000] | [0.0100, 0.0750] | Bootstrap Percentile 95% CI | Overlapping |
| **UCR (ALL N=100)** | [0.9000, 0.9867] | [0.9250, 0.9900] | Bootstrap Percentile 95% CI | Overlapping |
| **Query-level UCR (McNemar)** | Discordant $b=2$ | Discordant $c=4$ | $\chi^2 = 0.1667, p = 0.683091$ | Not Significant |
| **TEST Query-level UCR (McNemar)** | Discordant $b=0$ | Discordant $c=0$ | $\chi^2 = 0.0000, p = 1.000000$ | Not Significant |

---

## Table D: Latency Profile (Empirical Wall-Clock Timing)

| System Stage | Mean Latency (ms) | P50 Latency (ms) | P95 Latency (ms) |
| :--- | :---: | :---: | :---: |
| **Naive RAG Generation** | 5767.46 ms | 4659.18 ms | 9472.96 ms |
| **Verified RAG Complete Pipeline** | 5691.35 ms | 4899.07 ms | 8514.65 ms |

---

## Table E: Artifact SHA256 Hashes

| Artifact | SHA256 Hash |
| :--- | :--- |
| `e04_1_config.json` | `34ea6aae636b5a6ec5fefb74f9a963ed4cf88202062af562e384f03da840dc73` |
| `e04_1_per_query_results.json` | `561fa035d1244c6fbac4aa8b1131af90d1c2494ebf34c4ab6617e160f372c428` |
| `e04_1_claim_level_results.json` | `29b77c4f196d4a0dd2de731b603986125eca8cf041b9bffe2c24167d77f49faf` |
| `e04_1_citation_level_results.json` | `ad214a1256c26a6113da473dd5311546f56c5f5b5fc82a02f63fbf83d6d7c1c0` |
| `e04_1_latency_results.json` | `1a0b06e7953370488517dda869203f4954b4787005bf75de30d7ca5337fb8d04` |
| `e04_1_aggregate_metrics.json` | `45ca376046124da32e61ffc491d7091e5e4a7bea75ded8072ae09a421a67c612` |
| `e04_1_statistical_tests.json` | `4c03d8a3ff6ba5dffd4a67ed59106fea78595e1af4c5ef1205f6c9abfa80c83d` |
| `e04_1_naive_answers.json` | `43d495a625b056a53818e5a9cad8538a7a84df1869c229e3fae70a29444b076a` |
| `e04_1_verified_answers.json` | `6955d05237df960ce01941f6ea1a7ec5e3e50294affb449c090f2053101d4222` |

