# Statistical Amendments (V1.1 Amendment)

## 1. Executive Summary & Rationale

Naive RAG (Control) and ResearchNexus Verified RAG (Treatment) generate independent text outputs that may contain different sets, counts, and phrasings of extracted claims. 

Forcing paired McNemar tests onto unmatched, independently generated claims is statistically invalid. V1.1 defines explicit statistical testing rules based on whether the underlying evaluation unit is paired or unpaired.

---

## 2. Generation Comparison Statistical Plan

1. **For Independently Generated Claim Sets (Unmatched Sets)**:
   - **Metrics**: Claim Support Rate, Unsupported Claim Rate, Citation Precision, Citation Coverage.
   - **Procedure**: Report proportions (%), absolute deltas ($\text{Treatment} - \text{Control}$), and **bootstrap 95% percentile confidence intervals** (1,000 resamples).
   - **Categorical Testing**: Use **Chi-square test of independence** or Fisher's exact test for independent claim proportion comparisons across conditions.

2. **For Paired Query-Level Units (Matched Units)**:
   - **Procedure**: Use **McNemar's test** ONLY where the underlying unit of evaluation is paired and identical across conditions (e.g. query-level binary outcome: whether a query generated at least one unsupported claim).
