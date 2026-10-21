# ResearchNexusAI — RAG Pipeline Questions

### 1. What is the chunking strategy used for the corpus?
- **Answer:** Sliding-window token chunking (typically 256–512 tokens with 50-token overlap) preserving paragraph boundaries and metadata linkage back to original PDF page numbers.

### 2. How does the system handle an unanswerable query?
- **Answer:** In the canonical 90-item benchmark, items `item_v11_086` through `item_v11_090` are designated unanswerable. The RAG pipeline identifies that candidate chunks fail relevance thresholds, outputting an unanswerable notification rather than fabricating false claims.

### 3. What is Iterative RAG (`iterative_rag.py`)?
- **Answer:** A multi-turn refinement loop that analyzes initial synthesis gaps or contradictions, formulates targeted sub-queries, retrieves supplementary evidence, and refines the synthesis up to bounded iteration limits.
