# ResearchNexus AI — Module 2 Revision 01: Publication Language Audit

## 1. Audit Objective
This audit examines all textual statements, technical summaries, and publication-facing claims in Module 2 Revision 01. It enforces strict compliance with scientific integrity rules, eliminating hyperbolic or unsupported claims such as "100% factual accuracy", "100% grounding", or claims that "Verified RAG is proven to improve grounding on TEST".

---

## 2. Terminology & Claim Review

| Original / Potentially Ambiguous Phrasing | Audit Finding | Permitted Publication-Safe Replacement |
| :--- | :--- | :--- |
| *"Verified RAG achieves 100% factual precision"* | **DISALLOWED** as an unqualified global claim. Implies open-ended factual infallibility. | *"All automatically classified factual assertions within this small subset ($N \le 5$ per condition) were classified as supported by the retrieved literature."* |
| *"Verified RAG improves grounding"* | **DISALLOWED** for the frozen TEST split. Data shows $\Delta = 0.0000$ on factual precision and $\Delta = -0.0222$ on legacy CSR ($p=1.000$). | *"The frozen $N=15$ test split does not demonstrate a statistically detectable difference in factual grounding between Naive RAG and Verified RAG."* |
| *"McNemar's test proves CSR is equivalent ($p=1.000$)"* | **DISALLOWED**. McNemar evaluates a $2\times 2$ binary contingency table, not fractional CSR. | *"McNemar's test confirmed zero discordant queries regarding the binary presence of unsupported statements, but cannot be interpreted as a significance test for continuous CSR."* |
| *"Verification adds minimal latency overhead"* | **DISALLOWED** without decomposing internal verification cost from draft generation time. | *"The verification pipeline introduces a mean computational overhead of $+1,434.68$ ms. Observed total wall-clock time was comparable solely due to variance in draft generation length."* |
| *"Zero citation repair errors"* | **DISALLOWED** without independent human ground truth. | *"CitationRepair acted conservatively and introduced zero automated citation bindings onto refusal statements."* |
| *"Appropriate abstention observed on 5/5 adversarial queries"* | **PERMITTED**. Verifiable directly against benchmark ground truth definitions. | *"Appropriate epistemic abstention was observed on 5/5 adversarial unanswerable benchmark queries."* |

---

## 3. Mandatory Human Validation Boundary Clause
The following notice must be appended to all publication claims referencing Module 2:
> **Human Validation Boundary Notice**:  
> Independent human ground-truth annotation was not available in this evaluation environment (`HUMAN_VALIDATION_BLOCKED`). All verification metrics reflect automated deterministic rules and NLI model classifications. Automated evaluator outputs do not constitute independent human-verified factual ground truth.
