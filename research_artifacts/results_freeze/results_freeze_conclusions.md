# Authoritative Results Freeze Conclusions

1. **High Candidate Context Recall**: Under canonical live evaluation (E03.3), hybrid RRF achieves high candidate context recall (Recall@20 = 0.9500, Hit@20 = 1.0000 on ALL; Hit@20 = 1.0000 on TEST), successfully capturing gold documents within the top-20 pool.
2. **Context Distraction & Generator Bounds**: Although gold items are retrieved in top-20, their placement at lower ranks (ranks 15–17) amid distractors prevents the generator from synthesizing grounded answers, leading to refusal statements and ungrounded assertions.
3. **Verified RAG Performance**: On the evaluated benchmark, the multi-stage verified pipeline did not demonstrate a statistically significant grounding or citation improvement over Naive RAG (McNemar $p = 0.6831$).
4. **Iterative Refinement Trade-off**: Enabling iterative refinement increased wall-clock generation latency by 2.2x (mean 12,656 ms vs 5,691 ms) with no measurable grounding recovery (98 unchanged, 1 improved, 1 degraded, $p = 1.000$).
5. **Citation Repair Constraints**: Under conservative replacement policies in closed candidate pools, citation repair resolved 0 of 191 repair opportunities because replacement evidence did not satisfy strict matching thresholds.
6. **Disaggregated Neural Latency**: Genuine cross-encoder neural reranking contributes a median of 531.41 ms (p95 of 4,246.05 ms), representing the largest pre-generation latency component.
7. **Complete Architectural Provenance**: Under automated graph verification, the ResearchNexus explanation layer achieves 100% end-to-end provenance integrity (202/202 claims) connecting claims, citations, chunks, and retrieval scores.
8. **Empirical Grounding Integrity**: Scientific literature synthesis benchmarking requires strict separation between automated provenance tracing and human evaluation, with transparent reporting of non-significant improvements.
