# ResearchNexus AI — Module 2 Revision 01: Publication Claims & Boundaries

## 1. Validated, Publication-Safe Findings
The following empirical conclusions are scientifically supported by the corrected evaluation:

1. **High Abstention Fidelity**:
   Both Naive RAG and Verified RAG achieve 100% appropriate abstention (5/5) on adversarial unanswerable scientific queries (`item_v11_096` to `item_v11_100`), correctly identifying the absence of non-existent concepts without generating hallucinations.

2. **Conservative Repair Safety**:
   The `CitationRepair` module strictly preserves conservative behavior: it introduced zero synthetic citations onto negative findings or abstention statements.

3. **Verification Latency Footprint**:
   The internal computational overhead of Stage A deterministic matching, Stage B NLI semantic verification, and citation repair introduces a mean pipeline cost of $+1,434.68$ ms (Draft Generation: $3,214.50$ ms mean vs. Verification: $1,434.68$ ms mean).

4. **Taxonomic Separation Necessity**:
   In RAG benchmark evaluations containing negative findings and unanswerable queries, evaluating sentences without separating epistemic abstentions from factual assertions conflates refusal caution with hallucination.

---

## 2. Unsupported / Prohibited Claims

1. **PROHIBITED: Claiming Significant Grounding Improvement on Frozen TEST Split**:
   It is scientifically invalid to claim that Verified RAG improved grounding or factual precision over Naive RAG on the frozen TEST split ($p = 1.000$, $\Delta = 0.0000$).

2. **PROHIBITED: Claiming Human Ground Truth Validation**:
   No human annotations have been performed. All references must declare `HUMAN_VALIDATION_BLOCKED`.

3. **PROHIBITED: Interpreting McNemar's Test as a CSR Test**:
   McNemar's test evaluates paired binary contingency tables, not continuous or claim-aggregated support rates. Reporting $p=1.000$ from McNemar as proof of CSR equivalence is mathematically prohibited.

4. **PROHIBITED: Generalizing Beyond the Frozen Benchmark ($N=15$)**:
   No claims of universal grounding superiority across open-domain literature may be made from this frozen 15-query split.

---

## 3. Mandatory Human Validation Boundary Notice
Independent human ground-truth annotation was not available in this evaluation environment (`HUMAN_VALIDATION_BLOCKED`). All verification metrics reflect automated deterministic rules and NLI model classifications. Automated evaluator output does not constitute independent human-verified factual ground truth.
