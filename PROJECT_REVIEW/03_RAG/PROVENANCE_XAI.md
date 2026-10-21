# ResearchNexusAI — Explainable AI (XAI) & Provenance

> **Source Implementation:** ackend/app/services/research_artifact_service.py & src/pages/XaiPage.tsx  
> **Status:** Authoritative RAG Review Note  

---

## 1. What is Explainable RAG?
In academic and clinical literature review, users cannot rely on black-box summaries. ResearchNexusAI provides complete end-to-end evidence transparency through an Explainable AI (XAI) provenance graph.

## 2. Trace Architecture
For every user query, the system logs and returns an XAI trace payload:
- **Query Decomposition:** Extracted keywords and intent classification.
- **Retrieval Scores:** Side-by-side BM25 scores, ChromaDB cosine similarities, and post-RRF ordinal ranks.
- **Passage Attribution:** Exact byte offsets, page numbers, and chunk IDs in the source PDF.
- **Claim-Level Entailment Scores:** Probability distributions showing why a specific claim was classified as Entailed or Unverified.

## 3. Frontend Visualization (src/pages/XaiPage.tsx)
- Renders interactive Directed Acyclic Graphs (DAG) linking Query $\rightarrow$ Retrieved Chunks $\rightarrow$ Extracted Claims $\rightarrow$ Final Synthesis.
- Allows researchers to click any claim in the synthesis to inspect the exact highlighted paragraph in the original PDF.
