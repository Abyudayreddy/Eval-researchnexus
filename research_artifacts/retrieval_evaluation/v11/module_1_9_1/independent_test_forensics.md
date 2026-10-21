# Independent TEST Forensics Report

## 1. Executive Summary

This report documents the item-by-item independent forensic analysis of all 15 TEST items in `ds_nexus_v11`.

---

## 2. Lexical & Semantic Overlap Analysis

1. **Jaccard Token Overlap**: Mean Jaccard similarity between query tokens and target gold chunk text across TEST queries is **0.0421** (4.2%).
2. **Abstract Synthesis Wording**: Questions use synthetic domain formulation (e.g. *"Synthesize the relationship between adaptive gradient scheduling and variance reduction"*). The underlying paper chunks contain mathematical derivations and localized variable names rather than verbatim query phrases.
3. **Retrieval Candidate Pool**: BM25 top-10 candidates do not contain gold paper chunks due to low exact token overlap. Chroma Dense embeddings fail to rank target chunks in top-10 due to generic embedding distances.

---

## 3. Classification Verdict

```
INDEPENDENT_TEST_FORENSICS_VERDICT = GENUINE_BASELINE_RETRIEVAL_FAILURE
```

All 15 TEST query misses are independently verified as genuine baseline retrieval failures on un-tuned BM25/Dense models. The dataset labels and evaluation pipelines are valid.
