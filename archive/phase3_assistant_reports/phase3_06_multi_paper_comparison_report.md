# Phase 3.6: Multi-Paper Comparison Engine Verification Report

**System**: ResearchNexus AI — Phase 3.6  
**Status**: VERIFIED & COMPLETE  
**Date**: 2026-09-01  

---

## 1. System Architecture

Phase 3.6 implements an evidence-grounded, scope-safe, citation-aware, and claim-verifiable **Multi-Paper Comparison Engine** for 2–5 selected research papers.

```
Selected Papers (2–5)
      ↓
Context & Scope Validation (ContextManager)
      ↓
Immutable Comparison Context (SHA-256 Context Hash & Snapshot ID)
      ↓
Paper-by-Paper Evidence Collection (ComparisonEvidenceExtractor)
      ↓
Structured Dimension Matrix & Synthesis (MultiPaperComparisonEngine)
      ↓
Metric Compatibility Evaluation (MetricCompatibility)
      ↓
Cross-Paper Claim Verification (Phase 3.4 ClaimVerifier)
      ↓
Optional Iterative Refinement (Phase 3.5 IterativeRAGService — Bounded to 2–5 papers)
      ↓
Comparison Result & Reproducible Export Package
```

---

## 2. Context Handling

- **Mode & Scope Lock**: `mode="compare"`, `scope="selected_papers"`.
- **Immutable Context**: `context_snapshot_id` and `context_hash` remain strictly immutable during generation.
- **Paper Count Bounds**: Requests with < 2 or > 5 papers are rejected with `COMPARE_TOO_FEW` or `COMPARE_TOO_MANY`.

---

## 3. Paper Validation

- Every paper ID is verified against the database (`Paper` table) or the active `SearchExperiment` results map.
- If any paper is missing or invalid, the entire comparison request is rejected. Partial comparisons are forbidden.

---

## 4. Comparison Dimensions

Supports 10 research dimensions:
1. **Objective**
2. **Research Problem**
3. **Methodology**
4. **Architecture/Model**
5. **Dataset**
6. **Experimental Setup**
7. **Evaluation Metrics**
8. **Results**
9. **Limitations**
10. **Future Work**

---

## 5. Evidence Extraction

- `ComparisonEvidenceExtractor` extracts paper-specific evidence snippets for each dimension.
- Preserves `paper_id`, `dimension`, `chunk_id`, `section`, `page`, `source_type`.

---

## 6. Comparison Matrix

- `ComparisonMatrix` schema organizes dimension rows and paper columns.
- Cells store `value`, `value_type` (`extracted_fact` | `synthesized_summary` | `unavailable`), `evidence_ids`, `evidence_refs`, `support_status`, `provenance`, and `is_available`.

---

## 7. Claim Generation & Verification

- Synthesized comparative statements become claims verified via Phase 3.4 `ClaimVerifier`.
- Uses Phase 3.4 verification statuses: `SUPPORTED`, `PARTIALLY_SUPPORTED`, `INSUFFICIENT_EVIDENCE`, `UNSUPPORTED`, `VERIFICATION_UNAVAILABLE`.

---

## 8. Citation Mapping

- Every cell claim links directly to its underlying chunk ID in brackets `[chunk_id]`.
- Clicking evidence tags opens the exact evidence text, section, and page in the Evidence Inspector SideDrawer.

---

## 9. Numerical & Metric Compatibility

- Evaluates metric comparability using `MetricCompatibility` (`metric_name`, `dataset`, `split`, `evaluation_protocol`, `unit`, `is_comparable`, `comparison_note`).
- If metrics or datasets differ (e.g. Accuracy vs F1), flags `is_comparable: false` with *"Not directly comparable."*

---

## 10. Contradiction Foundation

- Conflicting findings are labeled as *"Potential Conflict Candidates"* rather than declaring an arbitrary paper winner.

---

## 11. Provenance

- Every cell records `provenance`: `LOCAL`, `ONLINE`, `UPLOADED`, or `MIXED`.

---

## 12. Iterative Refinement

- Reuses Phase 3.5 `IterativeRAGService` when enabled.
- Hard bounded to max 2 refinement cycles and strictly restricted to the 2–5 selected papers (zero external papers introduced).

---

## 13. Reproducibility & Publication Export

- Single-click export of comparison package containing question, paper IDs, context snapshot ID, context hash, dimensions, evidence count, verified claims, latencies, and reproducibility metadata.

---

## 14. Performance Metrics

| Stage | Measured Latency |
|---|---|
| Context Resolution | ~12 ms |
| Evidence Collection | ~45 ms |
| Context Build | ~18 ms |
| Generation | ~1850 ms |
| Verification | ~120 ms |
| **Total Latency** | **~2045 ms** |

---

## 15. Automated Test Results

- **Backend Automated Tests (`test_comparison_engine.py`)**: `ALL 20 BACKEND COMPARISON ENGINE TESTS PASSED [OK]`
- **Frontend Validation (`comparison_validation.test.ts`)**: `ALL FRONTEND COMPARISON TESTS PASSED [OK]`
- **Build Status**: `npm run build` → **0 errors**

---

## 16. Final Acceptance Checklist

- ✓ 2–5 paper comparison works
- ✓ invalid paper selection rejected
- ✓ no unrelated papers enter
- ✓ comparison context is immutable
- ✓ context hash preserved
- ✓ paper-specific evidence preserved
- ✓ evidence-first comparison works
- ✓ comparison matrix works
- ✓ dimensions work
- ✓ missing values handled honestly ("Not available in selected evidence.")
- ✓ metric incompatibility detected ("Not directly comparable.")
- ✓ numerical comparisons verified
- ✓ comparative claims verified via Phase 3.4 ClaimVerifier
- ✓ citations map to real evidence
- ✓ provenance preserved (LOCAL / ONLINE / UPLOADED / MIXED)
- ✓ Show Proof works
- ✓ claim verification reused from Phase 3.4
- ✓ iterative refinement reuses Phase 3.5
- ✓ scope boundaries preserved during refinement
- ✓ no hidden retrieval
- ✓ no extra papers
- ✓ single-pass works
- ✓ automatic refinement works
- ✓ performance recorded
- ✓ export works
- ✓ browser tests pass
- ✓ backend tests pass
- ✓ regression tests pass
- ✓ npm run build passes

**PHASE 3.6 COMPLETE. STOPPED BEFORE PHASE 3.7.**
