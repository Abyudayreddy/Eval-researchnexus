# Module 1: Deduplication Policy

## 1. Identity Definitions

- **Chunk Identity**: A unique string identifying an exact contiguous passage in ChromaDB or BM25 index. Format: `paper_id_chunk_idx` (e.g. `paper_res_032_chunk_001` or `local:Domain:Hash#chunk_0001`).
- **Paper Identity**: A unique string identifying the source publication/manuscript (e.g. `paper_res_032` or `local:Domain:Hash`).

---

## 2. Where Deduplication Occurs

### 2.1 Retrieval Execution (B1, B2, B3, B4)
- During raw retrieval, all models (BM25, Dense ChromaDB, RRF, and Cross-Encoder) retrieve and rank **individual chunks**.
- In B3 (RRF), fusion operates at the **chunk level**: scores from BM25 chunks and Dense chunks are fused via their chunk identifiers.
- In B4 (Cross-Encoder), reranking operates at the **chunk level**: query-chunk text pairs are evaluated and sorted by neural cross-attention scores.

### 2.2 Paper-Level Evaluation
- When evaluating **Paper-Level Metrics** (Document Discovery):
  1. The ranked chunk list $[c_1, c_2, \dots, c_N]$ is mapped to paper IDs $[p(c_1), p(c_2), \dots, p(c_N)]$.
  2. The paper list is deduplicated preserving the *first observed rank*: if paper $P$ appears at rank 1 and rank 3, only rank 1 is kept.
  3. The resulting deduplicated paper list $[P_1, P_2, \dots]$ is evaluated against `expected_paper_ids` at cutoffs $K \in \{5, 10, 20, 50\}$.

### 2.3 Evidence-Level Evaluation
- When evaluating **Evidence-Level Metrics** (Passage Grounding):
  1. The raw ranked chunk list $[c_1, c_2, \dots, c_N]$ is preserved without modification.
  2. The exact chunk IDs are matched against `expected_evidence_ids` at cutoffs $K \in \{5, 10, 20, 50\}$.
