# ResearchNexusAI — Hybrid Search & Reciprocal Rank Fusion (RRF)

> **Source Implementation:** ackend/app/services/retrieval.py::reciprocal_rank_fusion  
> **Status:** Authoritative RAG Review Note  

---

## 1. Why Reciprocal Rank Fusion?
Pure dense semantic retrieval often struggles with exact entity names, acronyms, or specific quantitative metrics, while pure BM25 fails when authors express concepts using synonyms. Combining them through score normalization is notoriously fragile because BM25 produces unbounded positive numbers while cosine similarity produces bounded $[-1, 1]$ floats.

Reciprocal Rank Fusion (RRF) solves this by operating entirely on **ordinal ranks** rather than raw scores.

## 2. Mathematical Formulation
For any document $ present in the candidate sets retrieved by BM25 and Dense vector search:

RRF\_Score(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}

Where:
-  = \{ \text{BM25}, \text{Chroma Dense} \}$
- (d)$ is the rank of document $ in system $ (1-indexed). If a document is not retrieved by a system, its reciprocal rank component is omitted or penalized.
- $ is the smoothing constant, set to ** = 60$** in accordance with information retrieval literature (Cormack et al.).

## 3. Implementation in Code
`python
def reciprocal_rank_fusion(bm25_results, dense_results, k=60):
    rrf_scores = {}
    for rank, doc_id in enumerate(bm25_results, 1):
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))
    for rank, doc_id in enumerate(dense_results, 1):
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))
    sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs
`
