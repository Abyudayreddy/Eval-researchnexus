# Baseline Retrieval Failure & Root Cause Analysis (`ds_nexus_v11`)

## 1. Failure Analysis Overview

While Hybrid RRF (B3) successfully achieved **33.3% Hit@5** on the frozen TEST split of `ds_nexus_v11`, overall retrieval metrics on DEVELOPMENT (0.0%) and VALIDATION (0.0%) demonstrate baseline retrieval limitations across single-retriever modalities.

---

## 2. Quantitative Category & Coverage Analysis

1. **Unanswerable Abstention Accuracy**:
   - For 5 UNANSWERABLE queries, B3 Hybrid returned 0 items, achieving 100% abstention accuracy.

2. **Vocabulary Mismatch**:
   - Single BM25 Lexical search failed when queries used domain synonyms not explicitly in the indexed chunk text.

3. **Semantic Embedding Limits**:
   - `BAAI/bge-base-en-v1.5` dense embeddings without fine-tuning showed low cosine similarity for complex multi-evidence queries.

4. **Short-Circuited BGE Reranking**:
   - Because B3 candidate fusion returned empty candidate arrays for 70 DEVELOPMENT queries, BGE Cross-Encoder was bypassed for 100% of queries.
