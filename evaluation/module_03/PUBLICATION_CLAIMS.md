# ResearchNexus AI — Module 3 Publication Claims & Scientific Boundaries

## 1. Supported Scientific Claims
The empirical results of Module 3 support the following rigorous statements:

1. **Conservative Repair Safety**:
   The conservative `CitationRepair` module introduces **zero incorrect citations** ($\text{Repair Error Rate} = 0.0\%$, $0/4$ candidate repairs applied). When candidate evidence matches multiple chunks, the system safely declines to apply ambiguous citations.

2. **Complete Evidence Provenance**:
   100% of validated citations maintain a complete, unbroken provenance chain from atomic claim $\rightarrow$ citation marker $\rightarrow$ retrieved chunk ID $\rightarrow$ paper title $\rightarrow$ local database origin.

3. **Computational Latency Overhead**:
   Citation validation and repair introduce a measurable, statistically significant mean computational overhead of **$+1,434.68$ ms** ($p < 0.001$, Wilcoxon signed-rank test). Total wall-clock time was comparable solely due to sample variance in draft generation length.

4. **Taxonomic Disambiguation of Non-Factual Findings**:
   Excluding evidence-based negative findings and abstentions from citation requirements prevents the artificial penalization of epistemic caution.

---

## 2. Unsupported / Prohibited Claims

1. **PROHIBITED: Claiming 100% Citation Correctness Across Open Literature**:
   On the frozen TEST split, only a single citation was generated and evaluated ($N=1$). Claiming universal 100% citation precision or coverage is statistically unjustified due to extremely low sample power.

2. **PROHIBITED: Claiming That Citation Repair Significantly Improves Coverage on TEST**:
   On the frozen TEST split, CitationRepair improved citation coverage by **0.0%** because all candidate matches were multi-chunk ambiguous and safely rejected.

3. **PROHIBITED: Claiming Human Ground Truth Validation**:
   Independent human subject validation was not conducted (`HUMAN_VALIDATION_BLOCKED`). Automated verification outcomes must not be represented as independent human truth.

4. **PROHIBITED: Claiming That Provenance Proves Factual Truth**:
   Provenance verifies that a citation points to an authentic text chunk in the database; it does not independently verify whether the underlying scientific claim published in the literature is objectively true.
