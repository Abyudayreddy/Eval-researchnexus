# ResearchNexus AI — Module 2 Error Analysis

## 1. Executive Summary
On the frozen TEST split of the benchmark ($N=15$), Claim Support Rate (CSR) was:
- **Naive RAG**: $0.0222$ (95% CI: $[0.0000, 0.0667]$)
- **Verified RAG**: $0.0000$ (95% CI: $[0.0000, 0.0000]$)
- **Delta CSR**: $-0.0222$ ($p = 1.000$, McNemar discordant test: not statistically significant)

This error analysis examines the underlying linguistic and algorithmic factors contributing to these numbers.

---

## 2. Failure Mode Categorization

### 2.1 Failure Mode A: The "Refusal / Negative Finding" Citation Gap
- **Nature**: The 15 TEST queries fall into two categories:
  1. *Answerable synthesis / quantitative checks* (queries 86–95) asking about specific metrics (e.g., 92.4% Precision@5 or 99.9% accuracy) which are not found or contradicted in the evidence.
  2. *Adversarial unanswerable queries* (queries 96–100) asking about non-existent concepts ("quantum gravity calibration constant").
- **Generator Behavior**: In both Naive and Verified modes, Gemini 2.5 Flash reliably acts with extreme epistemic caution, explicitly stating:
  > *"Based on the provided evidence, there is no mention of a '92.4% Precision@5' metric... Therefore, I cannot answer the query based on the retrieved documents."*
- **Algorithmic Verification Impact**: Because the model correctly refrained from making hallucinated positive assertions, it did not affix chunk citation tags (e.g., `[1]`) to its refusal sentences. Under canonical Stage A deterministic rules, any sentence lacking a citation marker is assigned `status = UNSUPPORTED` (`verification_method = "stage_a_deterministic"`). Consequently, true model abstentions were categorized as unsupported claims, artificially suppressing CSR.

### 2.2 Failure Mode B: Conservative Citation Repair Invariant
- `CitationRepair` is deliberately engineered to be conservative: it only binds candidate citations to claims when semantic overlap exceeds strict thresholds.
- When an extracted claim is an explicit refusal/abstention sentence, `CitationRepair` correctly refrains from binding arbitrary retrieved chunks to the negative statement. This demonstrates high system integrity—repair does not force spurious citations.

### 2.3 Failure Mode C: Single Supported Claim in Naive RAG
- In query `item_v11_089`, Naive RAG generated:
  > *"Based on the provided evidence, the documents mention that recent advances in Multimodal Representation Learning face scaling challenges [1]."*
  This statement received a supported classification ($1/3 = 0.3333$ CSR for query 89).
- Verified RAG generated a slightly different phrasing at temperature 0:
  > *"Based on the provided evidence, there is no mention of a '92.4% Precision@5' or any specific quantitative precision metrics related to adaptive gradient scheduling... While the evidence notes that multimodal representation learning research faces scaling challenges, no specific 92.4% Precision@5 metric is detailed."*
  Because the sentence was phrased contrastively without appending an explicit `[1]` tag directly to the clause, it was categorized as unsupported.

---

## 3. Implications for Claims & Paper Presentation
1. **Verification Mechanism Soundness**: The NLI and Stage A verification pipelines function deterministically as designed without crashes or false positives.
2. **Abstention vs. Grounding**: In future work, a distinct epistemological category (`ABSTENTION` / `NEGATIVE_FINDING`) should be introduced into claim extractors so that accurate refusals are not conflated with factual hallucinations.
3. **Publication Claim Boundary**: Research papers must not claim that Verified RAG yielded higher CSR than Naive RAG on the frozen TEST set; the difference is negligible and statistically indistinguishable ($p = 1.000$).
