# ResearchNexus AI — Module 3 Human Annotation Guidelines & Protocol

## 1. Status Determination: HUMAN_VALIDATION_BLOCKED
In strict adherence to the empirical standards of ResearchNexus AI, **no synthetic or simulated human labels are produced**. Because independent human annotators are not available in this CLI environment, human ground-truth validation remains formally **BLOCKED**.

This document and associated blank templates are provided for future independent study reproduction.

---

## 2. Protocol for Independent Citation Raters

Annotators are provided with 30 blinded claim-citation units sampled across factual, methodological, numerical, and unanswerable queries.

For each unit, annotators evaluate:
1. **Source Attribution**: Does the citation point to the claimed paper and author list?
2. **Support Entailment**: Does the referenced passage directly entail the claim, partially support it, or fail to support it?
3. **Attachment Accuracy**: Is the citation attached to the specific factual clause rather than a negative finding or refusal?
4. **Provenance Continuity**: Can the claim be traced from chunk to paper to database without gaps?

### Operational Labels:
- **`SUPPORTED`**: The cited chunk directly and unambiguously proves the claim.
- **`PARTIALLY_SUPPORTED`**: The cited chunk supports core aspects but omits secondary details.
- **`NOT_SUPPORTED`**: The cited chunk does not support the claim or mentions different figures.
- **`UNVERIFIABLE`**: The evidence text is truncated or corrupted.
- **`NOT_APPLICABLE`**: The claim is an explicit refusal or negative finding that should not carry citations.
