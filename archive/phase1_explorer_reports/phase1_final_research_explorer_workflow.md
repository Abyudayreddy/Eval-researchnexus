# Phase 1 Final Research Explorer Workflow

This document details the exact implementation and verification of the Research Explorer retrieval workflow, confirming that the pipeline strictly adheres to the requested architecture.

## 1. Query Processing
The exact original query is preserved as `original_query` for XAI and history. A `normalized_query` is created using deterministic preprocessing (whitespace normalization, lowercase) without utilizing an LLM, ensuring scientific terminology is not aggressively destructed.

## 2. Keyword Extraction
Deterministic query understanding extracts keywords and key phrases without reducing meaningful phrases to single tokens. This produces a keyword list for lexical search.

## 3. Semantic Representation
A semantic query text is derived from the user input. The embedding uses `BAAI/bge-base-en-v1.5` at 768 dimensions. Embeddings are NOT regenerated at runtime; only the query is embedded and matched against pre-computed corpus vectors in ChromaDB.

## 4. PostgreSQL
Structured candidate metadata (like title, authors, domain, doi) is queried via parameterized SQL to form a deterministic candidate pool, avoiding full unstructured data scans.

## 5. BM25
The chunk corpus is searched via a local BM25 index utilizing the tokenized normalized query. It retrieves a configurable `top_k` count of candidates (chunk_id, paper_id, BM25 score, rank).

## 6. ChromaDB
Semantic search runs against the persistent ChromaDB collection. It returns `chunk_id`, `paper_id`, `distance`, and `rank` for the configured nearest neighbors.

## 7. Candidate Union
A unified candidate pool aggregates results from PostgreSQL, BM25, and ChromaDB. Identity is rigorously managed with `chunk_id` for content matches and `paper_id` for document matches.

## 8. RRF
Reciprocal Rank Fusion (RRF) combines lexical and semantic ranks: `RRF(d) = 1 / (k + rank)`. Candidates present in both streams receive additive contributions, correctly sorting the united pool by `rrf_score` while retaining component ranks for XAI.

## 9. Relevance Filtering
Configurable relevance filters evaluate candidates based on overlap and RRF scores, eliminating low-quality matches before computationally expensive reranking. This decision is strictly logged.

## 10. Paper Diversification
The retrieval layer operates on chunks, but the UI operates on papers. Candidates are grouped by `paper_id`, and the highest-scoring chunk represents the paper, ensuring multiple Explorer cards are not spawned for the same paper.

## 11. BGE Reranking
When "deep evidence" mode is active, `BAAI/bge-reranker-base` is engaged. It re-scores the selected candidate evidence text against the query, generating a `reranker_score` that determines final sorting.

## 12. Evidence Selection
For every finalized local paper, `chunk_id`, `evidence_text`, and structural metadata are prepared. The actual retrieved text is utilized as evidence rather than defaulting to the abstract.

## 13. Online Retrieval
The existing `RepositoryRouter` remains internally unmodified. It executes concurrently with the local pipeline, pulling external repository data, scoring, and formatting.

## 14. Merge/Deduplication
Local and Online results are joined using a configured hybrid merge policy. Identity resolution deduplicates results matching on DOI, external ID, or strict title+author combination.

## 15. Provenance
Each final result card explicitly marks its retrieval source (`LOCAL`, `ONLINE`, or `MIXED`). A paper only appears as MIXED if independently discovered in both branches, preserving transparent provenance.

## 16. History
Every explicit query stores a history entry (`search_id`, `query`, timestamps, counts). Accessing history faithfully restores the state without re-triggering the retrieval pipeline.

## 17. XAI Handoff
"Why This Paper" correctly passes the `search_id` to render actual contribution metrics (BM25 position, Dense rank, RRF, reranker score, and evidence text), completely avoiding fake percentages.

## 18. Assistant Handoff
"Ask AI" invokes the Assistant in `SINGLE_PAPER` mode, passing the specific `paper_id` and `search_id` context to ground answers firmly in the selected literature.

## 19. Literature Handoff
"Build Literature Review" consumes the same research context (papers and chunk evidence IDs) and executes directly over the established evidence pool without re-running retrieval.

## 20. Offline Behavior
The local pipeline cleanly supports offline execution. If online connectors are disabled, a local query reliably processes the local corpus and returns `LOCAL` results successfully.

## 21. Performance Metrics
A comprehensive latency breakdown is tracked (BM25 latency, dense latency, RRF merge latency, total parallel search time). These exact metrics are persisted to support subsequent evaluations.

## 22. Browser Verification
Browser-level interactions are confirmed:
- Searching emits a single POST request to initiate the pipeline.
- Status is correctly tracked from 'queued' to 'complete'.
- Local, Online, and Mixed results are properly merged and visually distinguished.
- XAI, Ask AI, and Search History functionality works as specified without duplicated effort.
