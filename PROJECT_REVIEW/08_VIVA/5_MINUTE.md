# ResearchNexusAI — 5-Minute Comprehensive Presentation

### 1. Introduction & Motivation (1 Minute)
- Scientific literature is expanding faster than researchers can synthesize it.
- Existing general-purpose RAG systems hallucinate citations and fail to provide provenance.
- Goal: Create an explainable, multi-stage RAG system that guarantees evidence grounding and citation transparency.

### 2. Multi-Stage Pipeline Architecture (1.5 Minutes)
- **Ingestion:** 687 papers extracted, chunked with sliding window token overlap, indexed into BM25 and ChromaDB.
- **Retrieval:** Parallel BM25 + ChromaDB fused via Reciprocal Rank Fusion ($k=60$).
- **Reranking:** Cross-encoder reranking via `BAAI/bge-reranker-large`.
- **Synthesis:** Multi-document comparative synthesis with inline numeric citations `[1]`, `[2]`.
- **Verification:** NLI entailment gate evaluating whether each claim is Entailed, Contradicted, or Unverified.

### 3. Key Experimental Results (1 Minute)
- Tested on canonical 90-item multi-domain benchmark.
- Hybrid Hit@20: 86.7% vs. BM25 (77.8%) and Dense (81.1%).
- Grounding Precision: 88.4% (vs. 61.2% for Naive RAG).
- Latency: Hybrid retrieval completes in ~82ms; cross-encoder reranking completes in ~313ms.

### 4. Scientific Honesty & Audited Findings (1 Minute)
- Forensic audit (V1–V4) ensured all claims match raw data.
- Citation Repair achieved 20.0% coverage (1/5 claims), locked as a documented limitation.
- Reranking was shown to match Hybrid Hit@20, correctly presented as a precision filter rather than raw recall superiority.

### 5. Conclusion & Future Roadmap (0.5 Minutes)
- Successfully deployed as a responsive web workspace.
- Future work: Human expert validation and agentic multi-turn citation repair loops.
