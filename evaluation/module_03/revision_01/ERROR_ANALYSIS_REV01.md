# ResearchNexus AI — Module 3 Revision 01: Error Analysis

## 1. Overview & Methodological Clarification
This revised error analysis documents the 13 canonical failure modes for Module 3 on the frozen TEST split ($N=15$).

**Critical Methodological Clarification**:
In this analysis, an observed count of zero ($0$) is rigorously distinguished between:
- **Observed Zero (Tested & Verified Zero)**: The condition occurred or was evaluated, and zero failures were found.
- **Not Estimable / Not Tested**: The condition could not occur because the necessary prerequisite was absent (e.g. incorrect repairs cannot be measured if zero repairs were applied).

---

## 2. Comprehensive Failure Mode Table

| Failure Mode | Observed Count | Evaluated Sample ($N$) | Rate | Inference Status | Representative Example & Root Cause |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **A. Missing Citation** | 4 | 5 eligible factual claims | 80.0% | **OBSERVED** | `item_v11_091` claim 01 (Dense Retrieval scaling challenges). LLM generated multi-bracket citation format `[1, 3, 5...]` not parsed as single citation tag. |
| **B. Incorrect Citation** | 0 | 1 evaluated citation | 0.0% | **DESCRIPTIVE ZERO** ($N=1$) | The single citation in `item_v11_089` correctly cited `paper_res_003_chunk_001`. |
| **C. Partial Citation** | 0 | 1 evaluated citation | 0.0% | **DESCRIPTIVE ZERO** ($N=1$) | Entailment covered the asserted background proposition. |
| **D. Wrong-Paper Citation** | 0 | 1 evaluated citation | 0.0% | **DESCRIPTIVE ZERO** ($N=1$) | Citation resolved to correct paper ID. |
| **E. Wrong-Evidence Citation** | 0 | 1 evaluated citation | 0.0% | **DESCRIPTIVE ZERO** ($N=1$) | Evidence chunk ID matched context rank 1. |
| **F. Numerical Mismatch** | 10 | 10 answerable queries | 100.0% | **OBSERVED ABSENCE** | Queries probed metrics absent in evidence (e.g. 92.4% Precision@5); model correctly refused to confirm. |
| **G. False-Positive Repair** | 0 | 0 applied repairs | N/A | **NOT ESTIMABLE** | Zero repairs applied; incorrect-repair rate is not estimable because no repairs were applied. |
| **H. Ambiguous Repair Candidates** | 4 | 4 uncited factual claims | 100.0% | **OBSERVED CONSERVATIVE REJECTION** | All 4 candidate claims matched 10 chunks in context; conservative repair safely rejected all 4. |
| **I. Provenance Break** | 0 | 1 evaluated citation | 0.0% | **DESCRIPTIVE ZERO** ($N=1$) | Complete claim $\rightarrow$ citation $\rightarrow$ chunk $\rightarrow$ paper $\rightarrow$ source path verified. |
| **J. Metadata Mismatch** | 0 | 1 evaluated citation | 0.0% | **DESCRIPTIVE ZERO** ($N=1$) | Valid schema attributes across chunk JSON records. |
| **K. Unsupported Factual Proposition** | 0 | 28 extracted claims | 0.0% | **OBSERVED ZERO** | No hallucinations; model refrained from asserting ungrounded positive claims. |
| **L. Appropriate Abstention** | 15 | 28 extracted claims | 53.6% | **OBSERVED VALID REFUSAL** | Explicit refusals on queries where evidence lacked target figures. |
| **M. Insufficient-Evidence Finding** | 9 | 28 extracted claims | 32.1% | **OBSERVED NEGATIVE FINDING** | Meta-statements accurately noting lack of target metrics in documents. |

---

## 3. Scientific Summary of Repair Failure Dynamics
The absence of applied repairs on this frozen TEST split was not an algorithm crash or failure. Rather, it represents the exact intended operation of the conservative ambiguity safeguard:
- When a factual statement matches multiple retrieved literature chunks, guessing an arbitrary chunk ID would introduce spurious, ungrounded provenance.
- The algorithm's rejection of all 4 multi-chunk ambiguous candidates demonstrates **observed conservative rejection behavior under evidence ambiguity**.
- **Incorrect-repair rate is NOT ESTIMABLE** because no repairs were applied ($0/0$).
