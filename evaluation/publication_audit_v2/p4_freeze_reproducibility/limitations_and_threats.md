# Limitations and Threats to Validity

## 1. Limitations
1. **Benchmark Size for Test Split**: The test split contains 15 queries (10 answerable, 5 unanswerable). While sufficient for controlled qualitative error analysis, broader statistical power across diverse domains requires expanded benchmarks.
2. **Citation Repair Candidate Ambiguity**: The current deterministic repair heuristic rejects candidates that match multiple retrieved chunks equally well, preventing repairs when literature exhibits high semantic redundancy.
3. **Iterative Refinement Efficiency**: Running full secondary synthesis loops introduces significant latency (+106%) without systematic factual grounding improvements.
4. **Human Subject Evaluation**: Without external double-blind human annotators, grounding evaluation relies exclusively on automated NLI entailment models.

## 2. Threats to Validity
- **Construct Validity**: Addressed by decoupling factual claims from epistemic abstentions in the grounding evaluation.
- **Internal Validity**: Addressed by fixing random seeds, freezing model versions (`gemini-2.5-flash`, temperature 0.0), and hashing all benchmark artifacts.
- **Conclusion Validity**: Preserving all negative and neutral results prevents premature or exaggerated publication claims.
