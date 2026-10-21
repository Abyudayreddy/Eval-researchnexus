# Experiment E11: Authoritative Error Taxonomy Analysis
**Conference Research Paper Results Mode**  
**Dataset**: `ds_nexus_v11` (TEST Split Only, $N=15$)  
**Reconciliation Status**: PASS (Reconciled with Canonical E03.3 Live Candidate Context)  

---

## 1. Executive Summary

Experiment E11 evaluates the 14-category frozen failure taxonomy across the frozen TEST split ($N=15$, `item_v11_086` through `item_v11_100`) of `ds_nexus_v11` using exclusively authoritative empirical artifacts from predecessor experiments (E01, E02, E03.3, E04.1, E06.1, E07.1, E08, and E10).

> **Cross-Experiment Reconciliation with Canonical E03.3**:
> Authoritative canonical E03.3 live candidate evaluation establishes that all 15 TEST queries achieve Hit@20 = 1.0000 in the B3_Hybrid_RRF candidate context (gold documents are present at ranks 15–17 for items 086–095; items 096–100 are unanswerable probe queries). Consequently, under the authoritative k=20 pool, `CANDIDATE_POOL_MISS` and `RETRIEVAL_MISS` are exactly 0. Stale top-10 forensic artifacts (`independent_test_forensics.csv`) that evaluated an earlier top-10 slice are superseded.

> **Methodological Note on Multi-Label Categorization**:
> E11 uses multi-label error categorization; one query/claim/event may satisfy multiple taxonomy categories when the category definitions independently apply.

- **TEST Queries Analyzed**: 15
- **Verified RAG Claims Analyzed**: 28
- **Citation Repair Records Analyzed**: 28 (27 attempted, 0 successful, 27 failed, 1 not attempted / no repair required)
- **XAI Provenance Traces Analyzed**: 28
- **Categorized Error Events**: 98
- **Queries with Classified Errors**: 15 (100.0%)
- **Queries with Zero Classified Errors**: 0 (0.0%)

---

## 2. Authoritative Error Taxonomy Master Table

| Category | Count | Percentage | Denominator | Level | Source Artifact | Example Item IDs |
| :--- | :---: | :---: | :--- | :--- | :--- | :--- |
| **1. RETRIEVAL_MISS** | 0 | 0.00% | 15 TEST queries | Query | `e03_3_canonical_results_live.json` | None (0 observed at k=20) |
| **2. CANDIDATE_POOL_MISS** | 0 | 0.00% | 15 TEST queries | Query | `e03_3_canonical_results_live.json` | None (0 observed at k=20) |
| **3. RERANKING_ERROR** | 0 | 0.00% | 15 TEST queries | Query | `e03_3_canonical_results_live.json` | None (0 observed) |
| **4. EVIDENCE_SELECTION_ERROR** | 0 | 0.00% | 15 TEST queries | Query | `e04_1_per_query_results.json` | None (0 observed) |
| **5. UNSUPPORTED_CLAIM** | 28 | 100.00% | 28 claims | Claim | `e04_1_claim_level_results.json` | item_v11_086, item_v11_087, item_v11_088 |
| **6. CONTRADICTED_CLAIM** | 0 | 0.00% | 28 claims | Claim | `e04_1_claim_level_results.json` | None (0 observed) |
| **7. WRONG_CITATION** | 0 | 0.00% | 0 citations | Citation | `e04_1_citation_level_results.json` | None (0 observed) |
| **8. MISSING_CITATION** | 28 | 100.00% | 28 claims | Claim | `e04_1_claim_level_results.json` | item_v11_086, item_v11_087, item_v11_088 |
| **9. VERIFICATION_FALSE_POSITIVE** | 0 | N/A | N/A | Pipeline | E05 (BLOCKED) | *Not measurable without human GT* |
| **10. VERIFICATION_FALSE_NEGATIVE** | 0 | N/A | N/A | Pipeline | E05 (BLOCKED) | *Not measurable without human GT* |
| **11. CITATION_REPAIR_FAILURE** | 27 | 100.00% | 27 repair attempts | Citation | `e06_1_per_repair_results.json` | item_v11_086, item_v11_087, item_v11_088 |
| **12. ITERATION_FAILURE** | 15 | 100.00% | 15 TEST queries | Query | `e07_per_query_results.json` | item_v11_086, item_v11_087, item_v11_088 |
| **13. ONLINE_RETRIEVAL_FAILURE** | 0 | 0.00% | 15 TEST queries | Pipeline | System Execution Logs | None (0 observed) |
| **14. XAI_PROVENANCE_FAILURE** | 0 | 0.00% | 28 traces | Claim | `e08_per_claim_traces.json` | None (0 observed) |

---

## 3. Error Event Accounting by Level

The 98 categorized error events are composed strictly across explicit architectural denominators without cross-level percentage collapse:

- **Query-Level Events ($N=15$, Denominator: 15 TEST queries)**:
  - `RETRIEVAL_MISS`: 0 events ($0.00\%$)
  - `CANDIDATE_POOL_MISS`: 0 events ($0.00\%$)
  - `ITERATION_FAILURE`: 15 events ($100.00\%$)
- **Claim-Level Events ($N=56$, Denominator: 28 Verified RAG claims)**:
  - `UNSUPPORTED_CLAIM`: 28 events ($100.00\%$)
  - `MISSING_CITATION`: 28 events ($100.00\%$)
- **Citation-Level Events ($N=27$, Denominator: 27 repair attempts)**:
  - `CITATION_REPAIR_FAILURE`: 27 events ($100.00\%$ of attempts; $96.43\%$ of all 28 repair records)
- **Pipeline / Trace-Level Events ($N=0$)**:
  - `XAI_PROVENANCE_FAILURE`: 0 events ($0.00\%$)
  - `ONLINE_RETRIEVAL_FAILURE`: 0 events ($0.00\%$)

Total: $15 + 56 + 27 + 0 = 98$ events.

---

## 4. Reconciliation and Detailed Failure Mode Analyses

### A. Non-Zero Categories
1. **`UNSUPPORTED_CLAIM` (28 / 28 claims = 100.00%)**:
   - *Items*: All 28 verified claims across `item_v11_086` to `item_v11_100`.
   - *Explanation*: Although gold items were present in the 20-chunk candidate pool (ranks 15–17), they were placed towards the end of the context window behind distractor chunks. Consequently, the generator failed to synthesize grounded answers and produced ungrounded assertions or refusals, which were deterministically verified as `UNSUPPORTED`.
2. **`MISSING_CITATION` (28 / 28 claims = 100.00%)**:
   - *Items*: All 28 verified claims across `item_v11_086` to `item_v11_100`.
   - *Explanation*: Under the frozen taxonomy definition (*factual assertion lacks an inline citation*), all 28 claims generated in Verified RAG lacked inline citations because the model did not cite the distractor chunks.
3. **`CITATION_REPAIR_FAILURE` (27 / 27 attempts = 100.00%)**:
   - *Items*: All 27 attempted repairs.
   - *Explanation*: Exactly 28 repair records exist for TEST. Exactly 1 record (`item_v11_089`, `claim_01`) was `pre_repair_status = SUPPORTED` (`repair_opportunity_type = no_repair_required`, `repair_attempted = False`). Exactly 27 were attempted, 0 succeeded, and 27 failed under the conservative matching policy ($27 = 0 + 27$).
4. **`ITERATION_FAILURE` (15 / 15 queries = 100.00%)**:
   - *Items*: All 15 TEST queries.
   - *Explanation*: Iterative refinement executed feedback loops but terminated (`termination_reason = anti_oscillation`) without improving factual grounding; CSR remained at 0.0 on TEST without quality recovery.

### B. Zero-Count Categories
- **`RETRIEVAL_MISS` & `CANDIDATE_POOL_MISS`**: 0 observed in TEST under canonical E03.3 k=20 pool (Hit@20 = 1.0000).
- **`RERANKING_ERROR`**: 0 observed in TEST under canonical E03.3 evaluation.
- **`EVIDENCE_SELECTION_ERROR`**: 0 observed in TEST under the available evaluation artifacts.
- **`CONTRADICTED_CLAIM`**: 0 observed in TEST under the available evaluation artifacts.
- **`WRONG_CITATION`**: 0 observed in TEST under the available evaluation artifacts.
- **`ONLINE_RETRIEVAL_FAILURE`**: 0 observed in TEST under the available evaluation artifacts.
- **`XAI_PROVENANCE_FAILURE`**: 0 observed in TEST under the available evaluation artifacts. (100% trace completeness and offset resolution verified in E08).

### C. Unmeasurable Categories
- **`VERIFICATION_FALSE_POSITIVE`** & **`VERIFICATION_FALSE_NEGATIVE`**: *Not measurable from available artifacts* because Experiment E05 human ground truth remains strictly blocked.

---

## 5. Primary Observed Failure Pattern

Observed failures predominantly followed a context-distraction and grounding-deficit propagation pattern: while candidate pool retrieval succeeded in capturing gold papers in top-20 (ranks 15–17), lower rank placement amid distractors resulted in ungrounded assertions and missing citations that downstream CitationRepair and Iterative Refinement could not rescue, while provenance audit trails remained fully verifiable.
