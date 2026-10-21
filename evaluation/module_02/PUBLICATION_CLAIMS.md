# ResearchNexus AI — Module 2 Publication Claims & Scientific Boundaries

## 1. Supported Scientific Claims
The empirical evaluation of Module 2 supports the following scientific statements:

1. **Deterministic Verification Pipeline Feasibility**:
   The two-stage verification framework (Stage A deterministic rule checking followed by Stage B NLI semantic verification) executes reliably within a production RAG pipeline, completing full extraction, verification, and repair in a mean of $4,649.18$ ms (compared to $4,821.81$ ms for naive generation).

2. **Conservative Repair Safeguards**:
   The `CitationRepair` module adheres strictly to conservative semantics. It introduces zero spurious citation bindings onto refusal statements or unanswerable queries, preventing synthetic grounding artifacts.

3. **High Abstention Fidelity**:
   Both Naive RAG and Verified RAG achieve 100% abstention on unanswerable adversarial queries (`item_v11_096` to `item_v11_100`), correctly identifying the absence of non-existent scientific concepts without hallucinatory synthesis.

---

## 2. Unsupported / Prohibited Claims
In strict accordance with empirical findings, the following claims must **NOT** be made in publications or technical reports:

1. **NO Claim of Significant Grounding Improvement on TEST Split**:
   It is factually incorrect to claim that Verified RAG improved Claim Support Rate (CSR) over Naive RAG on the frozen TEST benchmark split ($\text{CSR}_{\text{Naive}} = 0.0222$ vs $\text{CSR}_{\text{Verified}} = 0.0000$, $\Delta = -0.0222$, $p = 1.000$). The difference is statistically indistinguishable.

2. **NO Human Ground Truth Validation Claim**:
   Because human subject annotations were not conducted in this evaluation, no claims of human validation or correlation with human preference may be made. Human annotation status must remain documented as `HUMAN_VALIDATION_BLOCKED`.

3. **NO Claim of Broad Benchmark Superiority Without Qualifying Evaluation Protocol**:
   The low Claim Support Rates observed stem primarily from the benchmark composition (difficult queries probing metrics absent from the evidence, prompting epistemic refusals that omit positive bracket citations). All presentations must disclose this context honestly.
