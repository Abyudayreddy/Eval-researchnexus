# Publication Limitations Register

The following limitations are grounded in verified artifacts and must be transparently acknowledged in Section V:

1. **Test Set Statistical Power ($N=15$)**:
   The test split of `ds_nexus_v11` comprises 15 items. While ideal for exhaustive forensic analysis (e.g., E11), it limits high statistical power for small effect sizes. Analysis is primarily descriptive.

2. **Absence of Human-Grounded Ground Truth (E05 Blocked)**:
   Experiment E05 remains blocked due to the unavailability of human expert annotations. Claim verification accuracy is audited deterministically and semantically against LLM-based NLI, but human-annotator agreement metrics are not reported.

3. **Automated Scope of XAI Provenance (E08)**:
   The 100% provenance chain accuracy reflects automated graph link resolution and exact text offset matching within the canonical database. It does not measure cognitive interpretability or human user trust.

4. **Policy-Specific Citation Repair Outcomes (E06.1)**:
   The 0% success rate in CitationRepair reflects a conservative exact-string/semantic matching policy in a closed retrieval corpus. It should not be generalized as a fundamental limitation of the concept.

5. **No Grounding Improvement in Verified Pipeline (E04.1 / E07.1)**:
   Neither Verified RAG over Naive RAG (McNemar $p=0.6831$) nor Iterative Refinement over Single-Pass ($p=1.000$) demonstrated statistically significant grounding gains on this benchmark, despite a 2.2x latency overhead.

6. **Context Distraction Despite High Recall (E03.3 / E11)**:
   While canonical candidate recall achieves Hit@20 = 1.0000 on TEST, gold documents are placed at lower ranks (15–17) amid distractor chunks, challenging LLM synthesis and leading to refusal/ungrounded outputs.

7. **Derived Latency Decompositions (E10)**:
   Ablation conditions A2 (No Citation Repair) and A4 (No BGE) latency values are derived mathematically via component decomposition from A0, rather than independent wall-clock runs.
