# Experiment E06.1: Citation Repair Provenance and Exact Context Validation Report

## 1. Executive Summary & Status
- **Stage**: `E06.1` (Citation Repair Provenance & Exact Context Validation)
- **Status**: `VALIDATED_AFTER_CORRECTION`
- **Dataset**: `ds_nexus_v11` ($N=100$ queries: DEV=70, VAL=15, TEST=15)
- **Context Source**: 100% exact E03.3 `B3_Hybrid_RRF` $k=20$ retrieved chunk IDs and rankings.
- **Context Provenance Match**: **100 / 100 (100.0%)** exact byte-level SHA256 context hash match with E04.1.
- **Evaluated Claims**: 202 Naive RAG generated claims.
- **Repair Opportunities**: 191 claims (189 missing citations, 2 unsupported citations).
- **Repairs Attempted**: 191
- **Successful Repairs**: 0
- **Citation Repair Success Rate**: 0.0000 (0.0%)

---

## 2. Context Provenance & Forensic Audit Findings

| Audit Check | Requirement | Result | Evaluation |
|---|---|---|---|
| **E03.3 Chunk ID Preservation** | Use exact retrieved chunk IDs from ranking | 2,000 / 2,000 chunks matched | ✅ **PASSED** |
| **Context Hash Match vs. E04.1** | Match `context_hash_naive` per query | **100 / 100 (100.0%)** matches | ✅ **PASSED** |
| **Substituted Heuristic Check** | Reject `LIMIT 1` paper substitution | No paper-first substitution used | ✅ **PASSED** |
| **Independent Verification** | Evaluate post-repair status via Stage A / B | 0 candidate repairs attached | ✅ **PASSED** |

---

## 3. Primary Comparative Metrics (Before vs. After Repair)

| Metric | Split | Before Repair | After Repair | Absolute Difference (Δ) | 95% Bootstrap CI | Statistical Significance |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **Citation Precision (CP)** | ALL ($N=100$) | 0.0600 | 0.0600 | +0.0000 | [0.0000, 0.0000] | Not Significant |
| | DEV ($n=70$) | 0.0714 | 0.0714 | +0.0000 | — | — |
| | VAL ($n=15$) | 0.0000 | 0.0000 | +0.0000 | — | — |
| | TEST ($n=15$) | 0.0667 | 0.0667 | +0.0000 | — | — |
| **Citation Coverage (COV)** | ALL ($N=100$) | 0.0617 | 0.0617 | +0.0000 | [0.0000, 0.0000] | Not Significant |
| | DEV ($n=70$) | 0.0786 | 0.0786 | +0.0000 | — | — |
| | VAL ($n=15$) | 0.0222 | 0.0222 | +0.0000 | — | — |
| | TEST ($n=15$) | 0.0222 | 0.0222 | +0.0000 | — | — |
| **Citation Completeness (CC)** | ALL ($N=100$) | 0.0500 | 0.0500 | +0.0000 | [0.0000, 0.0000] | Not Significant |
| | DEV ($n=70$) | 0.0714 | 0.0714 | +0.0000 | — | — |
| | VAL ($n=15$) | 0.0000 | 0.0000 | +0.0000 | — | — |
| | TEST ($n=15$) | 0.0000 | 0.0000 | +0.0000 | — | — |

---

## 4. Latency Profile (Component Wall-Clock Timing)

> [!NOTE]
> Latencies measure the internal `CitationRepair` matching execution per claim against hydrated contexts, excluding external API network latency.

| Metric | Measured Latency |
|---|---|
| **Evaluated Claims ($N$)** | 202 |
| **Mean Latency per Claim** | 0.3766 ms |
| **P50 Latency** | 0.1634 ms |
| **P95 Latency** | 0.4818 ms |
| **Min Latency** | 0.0022 ms |
| **Max Latency** | 36.9346 ms |

---

## 5. Scientific Safety & Limitation Analysis

- **Why 0 Repairs Occurred**: `CitationRepair` enforces a conservative heuristic to prevent spurious citations (requiring $>20$ character exact/strong substring matches or strict numerical overlap with $\ge 70\%$ keyword overlap). LLM-generated Naive RAG answers use abstract high-level synthesis sentences rather than direct verbatim quotes from the chunks. Consequently, zero claims satisfied the conservative threshold.
- **Empirical Paper Reporting**: Rather than tuning thresholds or manufacturing synthetic matches, the zero-repair empirical result is validated and recorded directly from the exact context.
