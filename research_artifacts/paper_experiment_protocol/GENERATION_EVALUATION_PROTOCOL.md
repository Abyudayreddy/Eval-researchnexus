# Generation Evaluation Protocol (Frozen)

## 1. Overview

This document specifies the frozen generation metrics and controlled comparison rules for Naive RAG vs. ResearchNexus Verified RAG.

---

## 2. Primary Grounding Metrics

1. **Claim Support Rate (CSR)**:
   $$\text{CSR} = \frac{\text{Count of Claims Classified SUPPORTED}}{\text{Total Extracted Claims in Generated Text}}$$

2. **Unsupported Claim Rate (UCR)**:
   $$\text{UCR} = \frac{\text{Count of Claims Classified UNSUPPORTED or CONTRADICTED}}{\text{Total Extracted Claims in Generated Text}}$$

3. **Citation Precision (CP)**:
   $$\text{CP} = \frac{\text{Count of Citations Pointing to Entailing Evidence}}{\text{Total Inline Citations in Generated Text}}$$

4. **Citation Completeness (CC)**:
   $$\text{CC} = \frac{\text{Count of Supported Claims With Valid In-Text Citations}}{\text{Total Supported Claims in Generated Text}}$$

---

## 3. Secondary Lexical / Semantic Metrics

- **ROUGE-L**: Measures longest common subsequence overlap against gold reference synthesis.
- **BERTScore**: Measures contextual embedding token similarity against gold reference synthesis.
- *Rule*: Lexical/semantic metrics are secondary and MUST NOT replace NLI claim grounding metrics.

---

## 4. Controlled Comparison Rules

- **CONTROL**: Naive RAG (LLM generation directly over top-5 B4 retrieved context).
- **TREATMENT**: ResearchNexus Verified RAG (LLM generation + NLI claim verification + citation repair).
- **HELD CONSTANT**: Identical questions, retrieved contexts, paper pools, LLM model checkpoint, temperature ($0.0$), max tokens.
- **CHANGED VARIABLE**: Verification and repair pipeline intervention.
