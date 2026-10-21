# Research Gaps & System Weaknesses Analysis

**Auditor Status**: VERIFIED  
**Date**: September 22, 2026  

---

## 1. Retrieval Gaps

### Weakness 1.1: Static RRF Parameter ($k=60$) & Unweighted Sparse-Dense Merging
* **CURRENT STATE**: `reciprocal_rank_fusion` uses a fixed constant $k=60$ regardless of query complexity or token length.
* **WHY IT MATTERS**: Short 2-word queries favor exact keyword matching (BM25), while long natural language research questions favor semantic vector search. Static $k=60$ treats both equally.
* **WHAT IS MISSING**: Dynamic, query-adaptive RRF parameterization or weighted RRF $S_{\text{RRF}} = \frac{w_b}{k_b + r_b} + \frac{w_d}{k_d + r_d}$.
* **PROPOSED CHANGE**: Implement adaptive parameter tuning based on query entropy and token count.
* **EXPECTED RESEARCH VALUE**: Improves Hit@1 and MRR across distinct query categories (`SINGLE_PAPER` vs `SYNTHESIS`).
* **HOW TO TEST IT**: Grid-search $k \in [10, 100]$ and weights $w \in [0.1, 1.0]$ over `ds_nexus_v10` DEV split ($N=70$).

### Weakness 1.2: Fallback Mock BGE Reranker in Default Execution
* **CURRENT STATE**: If `USE_REAL_BGE != "true"` environment variable is not explicitly exported, `retrieval.py` falls back to `MockCrossEncoder`, returning hardcoded linear mock scores `4.85 - i*0.5`.
* **WHY IT MATTERS**: Benchmark runs executed without `USE_REAL_BGE=true` silently evaluate dummy linear scores instead of real neural cross-attention.
* **WHAT IS MISSING**: Strict runtime assertion requiring real model weights or explicit logging when fallback is used.
* **PROPOSED CHANGE**: Force transformer model loading or raise explicit runtime error during evaluation runs.
* **HOW TO TEST IT**: Run unit tests asserting `reranker_model` is an instance of `CrossEncoder`.

---

## 2. Evidence / RAG Gaps

### Weakness 2.1: Disconnected Search-Id Caching in `/api/ai/ask`
* **CURRENT STATE**: If a user submits a query via `/api/ai/ask` without passing an existing 32-character `search_id` UUID in `search_mode`, `/ask` re-runs `search_papers` afresh instead of reusing active Explorer results.
* **WHY IT MATTERS**: Violates strict context preservation; the AI Assistant may generate answers from a slightly different set of retrieved papers than what the user inspected in the Explorer UI.
* **WHAT IS MISSING**: Mandatory `search_id` parameter in `AskRequest` schema.
* **PROPOSED CHANGE**: Require `search_id` for all RAG generation requests and throw `400 BAD_REQUEST` if `search_id` is missing or invalid.
* **HOW TO TEST IT**: Execute end-to-end integration test verifying zero retrieval calls during `/ask` when `search_id` is provided.

---

## 3. Verification Gaps

### Weakness 3.1: Regex-Based Claim Extraction Limits
* **CURRENT STATE**: `ClaimExtractor` splits text strictly on sentence delimiters (`[.!?]`) and classifies claims into `numerical` vs `factual_general` via simple regex.
* **WHY IT MATTERS**: Complex compound sentences containing multiple claims are treated as a single monolithic claim. If 1 clause is unsupported, the whole sentence is flagged.
* **WHAT IS MISSING**: Atomic proposition decomposition (e.g. using OpenIE or LLM-based proposition extraction).
* **PROPOSED CHANGE**: Integrate fine-grained atomic claim extraction before Stage A/B verification.
* **EXPECTED RESEARCH VALUE**: Increases claim verification granularity and precision.
* **HOW TO TEST IT**: Compare sentence-level vs proposition-level verification precision on TEST split.

---

## 4. Explainability (XAI) Gaps

### Weakness 4.1: Fragmented XAI Trace & Stubbed `/api/explain` API
* **CURRENT STATE**: Paper-level retrieval scores are displayed in `XAIModal.tsx`, while claim verification audits are in `ClaimProofDrawer.tsx`. The backend endpoint `/api/explain` in `backend/app/api/ai.py` returns `{"message": "AI Explain endpoint"}`.
* **WHY IT MATTERS**: The user cannot view a unified end-to-end trace from a final claim back to its paper's BGE score, RRF score, and BM25 rank in a single view or via a single API call.
* **WHAT IS MISSING**: Full end-to-end provenance object mapping `Claim -> Citation -> Chunk -> Paper -> BGE -> RRF -> BM25/Dense`.
* **PROPOSED CHANGE**: Implement a comprehensive `/api/explain/{claim_id}` backend service.
* **EXPECTED RESEARCH VALUE**: Provides publication-grade full-stack explainability.
* **HOW TO TEST IT**: Validate schema completeness of `/api/explain/{claim_id}` response payload.

---

## 5. Evaluation / Reproducibility Gaps (CRITICAL)

### Weakness 5.1: Simulated Mock Functions in `evaluation_service.py`
* **CURRENT STATE**: `evaluation_service.py` contains `_simulate_retriever`, `_execute_generation_pipeline`, and hardcoded metric returns (e.g. 0.733, 0.947, 0.940).
* **WHY IT MATTERS**: Running evaluation experiments via the API or Evaluation Console executes mock simulation code rather than actual model inference against `ds_nexus_v10` DB records. This creates a severe reproducibility vulnerability.
* **WHAT IS MISSING**: Real, un-simulated evaluation execution pipeline connecting `EvaluationService` directly to `LocalEvidenceRetriever`, `EnhancedRAGService`, and `ClaimVerifier`.
* **PROPOSED CHANGE**: Replace all simulation methods in `evaluation_service.py` with direct invocations of real system services.
* **EXPECTED RESEARCH VALUE**: Essential for paper publication; guarantees 100% empirical authenticity.
* **HOW TO TEST IT**: Run full benchmark suite via `evaluation_service.py` with network disconnect and verify real GPU/CPU model execution and DB queries.
