# ResearchNexusAI — Complete System Flow

> **Trace:** End-to-End Query Execution Lifecycle  

---

```text
1. USER QUERY
   +-- User enters topic query in HybridSearchPage or AssistantPage.
       Example: "Contrast digital twin architectures in urban flood mitigation"

2. CLIENT TRANSMISSION
   +-- src/utils/api.ts sends POST request with JWT header to /api/ai/query.

3. API GATEWAY & VALIDATION
   +-- backend/app/api/ai.py validates payload via Pydantic model AskRequest.

4. DUAL-CHANNEL HYBRID RETRIEVAL
   +-- backend/app/services/retrieval.py launches parallel retrieval:
       |-- BM25 search across 687 papers in ResearchMind_LocalKB
       +-- ChromaDB dense vector search using BGE embedding
       Scores are unified via Reciprocal Rank Fusion: RRF = sum(1 / (60 + rank))

5. CROSS-ENCODER RERANKING
   +-- Top-20 candidates are rescored by BAAI/bge-reranker-large to produce final context.

6. STRUCTURED PROMPT ASSEMBLY
   +-- Top passages + user query are structured with citation anchors [1], [2] in EnhancedRAGService.

7. FOUNDATION MODEL GENERATION
   +-- llm_provider.py calls Groq/Gemini to generate multi-document synthesis text.

8. ATOMIC CLAIM EXTRACTION
   +-- claim_extractor.py parses synthesis output into discrete factual assertions.

9. CLAIM VERIFICATION (NLI)
   +-- claim_verifier.py evaluates entailment of each claim against the retrieved passages:
       |-- Entailed: Marked as verified with green badge
       +-- Contradicted / Unverified: Flagged for warning or repair

10. CITATION REPAIR CHECK
    +-- citation_repair.py attempts rule-based passage alignment (Module 3 logic).

11. XAI TRACE PACKAGING
    +-- System packages attention weights, similarity metrics, passage ranks into an XAI trace object.

12. FRONTEND RENDERING
    +-- AssistantPage renders synthesis with verified badges; XaiPage visualizes the full provenance DAG.
```
