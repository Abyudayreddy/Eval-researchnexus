# RESEARCHNEXUS — FINAL BLACK-BOX END-USER AUDIT V2 & NUMERICAL INTEGRITY VERIFICATION

**Audit Date**: September 13, 2026  
**Auditor Role**: Independent End User, Scientific Researcher & Peer Reviewer  
**Audit Protocol**: `imp.md` V2 Re-Evaluation Protocol (Strict Evidence & Numerical Integrity Audit)  

---

## 1. Executive Summary & Critical Correction

This V2 Audit replaces and corrects the previous audit. Per the explicit directives in `imp.md` V2:

> **Rule 2 & Rule 25 (Strict Evidence Rule)**: A feature that was not actually exercised through visual browser interaction cannot receive `PASS`. Unit tests, code inspections, and headless API calls cannot be converted into UI `PASS`. If interactive browser testing is unavailable in the execution environment, the end-user UI status must be strictly set to **`NOT TESTED`**.

### Summary of Verdicts

1. **APPLICATION FUNCTIONALITY (UI Interaction)**: **`NOT TESTED`**  
   - *Rationale*: Direct visual browser automation was unavailable in the current CLI execution environment. Headless HTTP requests confirmed that the React application shell loads at `http://localhost:5173/`, but DOM interactions (button clicks, form inputs, modal opens) could not be visually executed. Per Rule 25, unit test passes are **not** inferred as UI passes.

2. **CODEBASE & SUITE INTEGRITY**: **`PASS`**  
   - *Rationale*: All 112 backend pytest cases across 8 evaluation test files (`test_e02`, `test_e03`, `test_e04`, `test_e05`, `test_claim_verification`, `test_enhanced_rag`, `test_iterative_refinement`, `test_evaluation_console`) pass cleanly. All 8 frontend TypeScript validation assertions pass cleanly.

3. **E01–E05 NUMERICAL INTEGRITY**: **`FAIL`** (due to E03 Report Metric Discrepancy)  
   - *Rationale*: An audit comparing the canonical markdown evaluation reports against `evaluation_service.py` uncovered a numerical discrepancy in Evaluation Stage 3 (E03).

4. **SCIENTIFIC VALIDITY**: **`PASS`**  
   - *Rationale*: The fundamental experimental design, component isolation chain ($B3 \rightarrow B4 \rightarrow B5E \rightarrow B6V \rightarrow B7R$), and non-parametric statistical testing (Wilcoxon signed-rank tests & Bootstrap 95% CIs) are scientifically sound.

5. **REPRODUCIBILITY**: **`PASS`**  
   - *Rationale*: Full hyperparameter configurations, dataset split definitions (`ds_nexus_v10`), frozen item IDs, and raw reproducible metric packages are fully exported via `export_publication_package()`.

6. **PUBLICATION READINESS**: **`BORDERLINE`**  
   - *Rationale*: The system architecture and empirical evaluation are strong, but submission readiness requires reconciling the E03 metric report discrepancy and expanding the frozen TEST split ($N=15$) prior to peer submission.

7. **OVERALL DECISION**: **`FAIL`**  
   - *Rationale*: Per Rule 41 ("Do not average away critical failures or data discrepancies"), the detected E03 report discrepancy prevents an overall PASS until reconciled.

---

## 2. E01–E05 Numerical & Report Consistency Audit

Per Rule 19 and Rule 22, every value presented in the canonical reports was audited against the backend database and evaluation service code.

### Canonical Benchmark Results Summary ($N=15$ Frozen TEST Split)

| Stage | Baseline ID | Primary Metric | Reported Value | Code Service Value | Discrepancy Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **E01** | `B3_HYBRID_RAG` | MRR / Recall@5 | 0.812 / 0.933 | 0.812 / 0.933 | **MATCH (PASS)** |
| **E02** | `B4_HYBRID_BGE` | Top-1 MRR | 0.887 (+0.075) | 0.887 (+0.075) | **MATCH (PASS)** |
| **E03** | `B5E_ENHANCED_RAG` | Citation Precision | **0.947** (vs 0.733 B5R) | **0.964** (vs 0.750 B5R) | **DISCREPANCY DETECTED (FAIL)** |
| **E04** | `B6V_ENHANCED_RAG` | Citation Precision | 0.980 (+0.230) | 0.980 (+0.230) | **MATCH (PASS)** |
| **E05** | `B7R_ITERATIVE_RAG`| Citation Precision | 0.992 (+0.027) | 0.992 (+0.027) | **MATCH (PASS)** |

### Detail on E03 Discrepancy
- **Canonical Report (`evaluation_stage3_E03_enhanced_rag_report.md`)**: Table 1 reports B5R Citation Precision = **0.733** and B5E Citation Precision = **0.947** ($\Delta = +0.214$).
- **Service Logic (`evaluation_service.py:compare_e03_enhanced_rag`)**: Line 1250 returns B5R Citation Precision = **0.750** and B5E Citation Precision = **0.964** ($\Delta = +0.214$).
- **Impact**: While the metric delta ($\Delta = +0.214$) and statistical significance ($p = 0.008$) remain identical, the absolute baseline numbers differ by 0.017. Per V2 Rule 19 and Rule 22, this discrepancy is flagged as **FAIL** and must be reconciled before paper submission.

---

## 3. End-User UI Audit Coverage (Sections 3–21)

Because interactive browser automation tools were not available in the execution environment, all 21 end-user UI interaction categories are recorded as **`NOT TESTED`** per Rule 2 and Rule 25:

| Category | Tested Feature | Observed Status | Reason for Status |
| :--- | :--- | :---: | :--- |
| **Dashboard** | Page load & nav actions | **NOT TESTED** | Visual browser interaction unavailable |
| **Research Explorer** | 5 domain search queries | **NOT TESTED** | Visual browser interaction unavailable |
| **Execution Transparency** | Progress step verification | **NOT TESTED** | Visual browser interaction unavailable |
| **Counter Consistency** | Paper vs Evidence counters | **NOT TESTED** | Visual browser interaction unavailable |
| **Explainable AI (XAI)** | Score & rank shift audit | **NOT TESTED** | Visual browser interaction unavailable |
| **AI Assistant** | RAG Q&A & unsupported queries | **NOT TESTED** | Visual browser interaction unavailable |
| **Manual Citation Audit** | 20-answer manual inspection | **NOT TESTED** | Visual browser interaction unavailable |
| **Claim Verification** | Phase 3.4 verification UI | **NOT TESTED** | Visual browser interaction unavailable |
| **Iterative Refinement** | Phase 3.5 cycle UI | **NOT TESTED** | Visual browser interaction unavailable |
| **Compare Papers** | 2, 3, 5 paper comparison matrix | **NOT TESTED** | Visual browser interaction unavailable |
| **Literature Synthesis** | Consensus & gap analysis | **NOT TESTED** | Visual browser interaction unavailable |
| **Personal Corpus** | PDF upload & user isolation | **NOT TESTED** | Visual browser interaction unavailable |
| **Session / Workspace** | Session lifecycle & notes | **NOT TESTED** | Visual browser interaction unavailable |
| **Adversarial Testing** | False premise query handling | **NOT TESTED** | Visual browser interaction unavailable |
| **Failure Testing** | Refresh & back button handling | **NOT TESTED** | Visual browser interaction unavailable |
| **Performance** | End-user visual timings | **NOT TESTED** | Visual browser interaction unavailable |

---

## 4. Simulated Peer Review (Mock Reviewer Assessment)

Per Rule 21, all reviewer assessments are explicitly identified as **simulated mock peer reviews**:

### Mock Reviewer 1 (Scientific Novelty & Methodology)
- **Rating**: **BORDERLINE PASS**
- **Comments**: "The integration of RRF fusion, cross-encoder reranking, claim verification, and iterative refinement forms a complete system. However, the methodological novelty lies in engineering integration rather than fundamentally new algorithmic primitives. The paper must clearly frame its contribution as an empirical system design."

### Mock Reviewer 2 (Technical Correctness & Experimental Control)
- **Rating**: **FAIL / MAJOR REVISION**
- **Comments**: "The experimental controls (such as freezing initial generations across control and experimental arms in E04 and E05) are methodologically sound. However, I detected a numerical discrepancy between the reported E03 metrics in the text (0.733 vs 0.947) and the exported evaluation service payload (0.750 vs 0.964). This discrepancy must be reconciled prior to publication."

### Mock Reviewer 3 (Dataset & Statistical Rigor)
- **Rating**: **BORDERLINE PASS**
- **Comments**: "The component isolation across E01–E05 is exemplary. However, evaluating primary claims on a TEST split of $N=15$ items represents a major statistical limitation. Although non-parametric Wilcoxon tests and bootstrap CIs are reported, expanding the benchmark TEST split to $N \ge 50$ is strongly recommended."

### Mock Editor Summary
- **Simulated Recommendation**: **REVISE AND RESUBMIT (BORDERLINE)**
- **Required Action Items Before Resubmission**:
  1. Reconcile the absolute baseline values between `evaluation_stage3_E03_enhanced_rag_report.md` and `evaluation_service.py`.
  2. Perform interactive browser QA and attach visual screenshot evidence.
  3. Explicitly document the $N=15$ sample size limitation in the manuscript's Threat to Validity section.

---

## 5. Final Verdicts & Recommendations

```text
==================================================
APPLICATION FUNCTIONALITY: NOT TESTED (No Browser UI)
END-USER EXPERIENCE:       NOT TESTED (No Browser UI)
SCIENTIFIC VALIDITY:       PASS
REPRODUCIBILITY:           PASS
PUBLICATION READINESS:     BORDERLINE
--------------------------------------------------
OVERALL PROJECT DECISION:  FAIL (E03 Metric Discrepancy)
==================================================
```

### Next Steps (Post-Audit):
1. **Reconcile E03 Report**: Update `evaluation_stage3_E03_enhanced_rag_report.md` or `evaluation_service.py` so that reported absolute baselines match exactly (0.750 / 0.964 vs 0.733 / 0.947).
2. **Execute Interactive Browser QA**: Perform manual visual testing via Chrome/Firefox browser once a graphical test environment is configured.
3. **DO NOT MODIFY E01-E05 LOGIC**: Preserve all underlying retrieval and refinement algorithms.
