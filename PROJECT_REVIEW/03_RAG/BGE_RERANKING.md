# ResearchNexusAI — BGE Reranking Stage

> **Source Implementation:** ackend/app/services/retrieval.py::rerank_with_bge  
> **Status:** Authoritative RAG Review Note & Reconciled Audit Findings  

---

## 1. Role in the Multi-Stage Pipeline
After Reciprocal Rank Fusion aggregates the top candidate passages (typically Top-20 or Top-50), a cross-encoder model rescores passage relevance conditioned directly on the user query.

ResearchNexusAI integrates **BAAI/bge-reranker-large**.

## 2. Bi-Encoder vs. Cross-Encoder
- **Bi-Encoder (ChromaDB Dense Retrieval):** Embeds the query and passage independently into vectors: $\text{sim}(q, p) = \cos(e_q, e_p)$. Fast for (N)$ vector indexing but misses fine-grained token-level cross-attention.
- **Cross-Encoder (BGE Reranker):** Concatenates query and passage into a single sequence: $[CLS] + q + [SEP] + p + [SEP]$. Full self-attention across every query token and passage token produces higher relevance discrimination at the cost of higher latency.

## 3. Canonical Evaluation Status (V4 Reconciliation)
> **IMPORTANT PUBLICATION FINDING:**  
> The V4 canonical reconciliation established that while BGE Reranking operates correctly in the pipeline, on the frozen 90-item test benchmark, Hybrid retrieval alone achieved **@20 = 0.867$**. The audit formally **withdrew claims of statistical reranking superiority over hybrid baseline** on the frozen evaluation split. In the IEEE paper and review defense, acknowledge BGE as a precision filter for generation context rather than overclaiming statistical retrieval gains.
