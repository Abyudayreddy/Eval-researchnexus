# Error Taxonomy Specification (Frozen)

## 1. Overview

This document specifies the 14 frozen error categories for qualitative error analysis.

---

## 2. Frozen Error Categories

1. **`RETRIEVAL_MISS`**: Query tokens fail to retrieve relevant documents in top-$k$.
2. **`CANDIDATE_POOL_MISS`**: Target gold item is missing from initial candidate pool before reranking.
3. **`RERANKING_ERROR`**: Reranker demotes relevant candidate out of top-$k$.
4. **`EVIDENCE_SELECTION_ERROR`**: System selects irrelevant chunk from retrieved candidate set.
5. **`UNSUPPORTED_CLAIM`**: LLM generates statement not backed by context.
6. **`CONTRADICTED_CLAIM`**: LLM generates statement contradicting context.
7. **`WRONG_CITATION`**: Inline citation points to incorrect chunk.
8. **`MISSING_CITATION`**: Factual assertion lacks inline citation.
9. **`VERIFICATION_FALSE_POSITIVE`**: NLI verifier marks unsupported claim as supported.
10. **`VERIFICATION_FALSE_NEGATIVE`**: NLI verifier marks supported claim as unsupported.
11. **`CITATION_REPAIR_FAILURE`**: Citation repair fails to find supporting chunk.
12. **`ITERATION_FAILURE`**: Iterative refinement fails to improve factual quality.
13. **`ONLINE_RETRIEVAL_FAILURE`**: Upstream API or index lookup timeout.
14. **`XAI_PROVENANCE_FAILURE`**: Provenance link chain broken between claim and database chunk.
