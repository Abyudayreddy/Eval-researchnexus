# ResearchNexusAI — Code Preparation Matrix

> **Authoritative Inventory Reference:** PROJECT_REVIEW_CODE_INVENTORY.md  
> **Status:** Active Review Tracking Matrix  

This matrix tracks technical preparation across the 23 A+ core files (Primary Architectural Spine) and the 40 A-level files (Secondary Supporting Modules).

---

## 1. Primary Preparation: 23 A+ Core Files

| No. | File Path | Category | Importance | Purpose | Must Understand | Reviewer Questions | Related Files | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | src/App.tsx | FRONTEND_ENTRY | **A+** | React routing, auth wrapper, layout shell | ProtectedRoute, nested routes, redirect fallback | 4 questions (routing, auth, replace prop, module links) | AppLayout.tsx, uthStore.ts | **NOT_STARTED** |
| 2 | ackend/app/main.py | BACKEND_ENTRY | **A+** | FastAPI app, CORS, router registrations | App bootstrap, middleware stack, API prefixes | 4 questions (lifecycle, CORS, router registry, error handling) | ackend/app/api/*.py, config.py | **NOT_STARTED** |
| 3 | ackend/app/api/ai.py | API | **A+** | RAG query, synthesis, and XAI endpoints | Request validation, synthesis endpoint dispatch | 4 questions (Pydantic models, latency logging, fallback) | enhanced_rag.py, llm_provider.py | **NOT_STARTED** |
| 4 | ackend/app/api/papers.py | API | **A+** | Paper search, metadata filtering gateway | Query normalization, hybrid search dispatch | 4 questions (filters, pagination, chunk retrieval) | 
etrieval.py, models/paper.py | **NOT_STARTED** |
| 5 | ackend/app/api/research.py | API | **A+** | Multi-paper comparison & gap analysis API | Matrix assembly, session persistence | 4 questions (comparison schema, concurrent queries) | comparison_engine.py, 
esearch_session_service.py | **NOT_STARTED** |
| 6 | ackend/app/models/paper.py | DATABASE | **A+** | SQLAlchemy paper, chunk, embedding ORM | Table relationships, chunk metadata, vector FKs | 4 questions (indexing strategy, ChromaDB mapping) | ackend/app/db/session.py | **NOT_STARTED** |
| 7 | ackend/app/services/assistant/enhanced_rag.py | RAG_ORCHESTRATION | **A+** | Multi-stage RAG orchestrator pipeline | Pipeline sequencing, verification integration | 4 questions (stage flow, zero-retrieval handling) | 
etrieval.py, claim_verifier.py | **NOT_STARTED** |
| 8 | ackend/app/services/assistant/iterative_rag.py | RAG_ORCHESTRATION | **A+** | Multi-turn feedback & refinement loop | Re-querying criteria, iteration bounds | 4 questions (termination, latency trade-offs) | enhanced_rag.py, self_feedback.py | **NOT_STARTED** |
| 9 | ackend/app/services/retrieval.py | RETRIEVAL | **A+** | BM25 + Chroma dense + RRF + BGE rerank | RRF formulation (k=60), cross-encoder scoring | 4 questions (RRF formula, reranker latency, fallback) | 
ank_bm25, chromadb, sentence_transformers | **NOT_STARTED** |
| 10 | ackend/app/services/local_evidence.py | RETRIEVAL | **A+** | Local KB cached index query engine | Precomputed pickle loading, token cleaning | 4 questions (in-memory caching, passage scoring) | ResearchMind_LocalKB/indexes/ | **NOT_STARTED** |
| 11 | chunk_corpus.py | DATA_INGESTION | **A+** | Offline PDF text chunking pipeline | Sliding window size, token overlap rules | 4 questions (chunk boundaries, heading retention) | ResearchMind_LocalKB/chunks/ | **NOT_STARTED** |
| 12 | embed_corpus.py | DATA_INGESTION | **A+** | Dense neural embedding generation script | BGE-base embedding, batch Chroma storage | 4 questions (batching, distance metric, manifest check) | chunk_corpus.py, chromadb | **NOT_STARTED** |
| 13 | uild_indexes.py | DATA_INGESTION | **A+** | BM25 inverted index builder script | Serialization, token frequency, ID syncing | 4 questions (mapping synchronization, verification) | m25_index.pkl, m25_mapping.json | **NOT_STARTED** |
| 14 | ackend/app/services/llm_provider.py | GENERATION_LLM | **A+** | Multi-provider LLM driver with fallback | Provider abstraction, temperature control | 4 questions (error retry, latency logging, caching) | Groq, Gemini, OpenAI APIs | **NOT_STARTED** |
| 15 | ackend/app/services/assistant/synthesis_engine.py | GENERATION_LLM | **A+** | Structured scientific synthesis generator | Multi-document prompt, inline citations | 4 questions (hallucination guardrails, structure) | llm_provider.py, synthesis_extractor.py | **NOT_STARTED** |
| 16 | ackend/app/services/assistant/claim_verifier.py | CLAIM_VERIFICATION | **A+** | Automated NLI claim entailment verifier | Atomic claim decomposition, entailment scoring | 4 questions (NLI model, grounding precision/recall) | claim_extractor.py, enhanced_rag.py | **NOT_STARTED** |
| 17 | ackend/app/services/assistant/citation_repair.py | CITATION_PROVENANCE_XAI | **A+** | Rule-based citation repair module | Audited Module 3 findings (20.0% coverage) | 4 questions (1/5 claim result, safety limitations) | claim_verifier.py, module_03/ | **NOT_STARTED** |
| 18 | src/utils/api.ts | FRONTEND_API_SERVICES | **A+** | Axios HTTP client & API service bridge | JWT interceptors, typed response interfaces | 4 questions (base URL, auth headers, error dispatch) | uthStore.ts, backend API routers | **NOT_STARTED** |
| 19 | src/pages/HybridSearchPage.tsx | FRONTEND_PAGES | **A+** | Hybrid search & parameter control UI | Weight controls, rank score inspection | 4 questions (lexical vs dense toggle, result cards) | src/utils/api.ts | **NOT_STARTED** |
| 20 | src/pages/AssistantPage.tsx | FRONTEND_PAGES | **A+** | Conversational RAG assistant interface | Inline citations, evidence preview drawer | 4 questions (verified claim badges, context memory) | src/utils/api.ts | **NOT_STARTED** |
| 21 | src/pages/LiteratureReviewPage.tsx | FRONTEND_PAGES | **A+** | Multi-paper comparative synthesis UI | Comparison matrices, research gap tables | 4 questions (matrix filters, review export) | src/utils/api.ts | **NOT_STARTED** |
| 22 | src/pages/XaiPage.tsx | FRONTEND_PAGES | **A+** | Explainable AI provenance viewer UI | Attention distribution, provenance graph | 4 questions (evidence path trace, claim inspector) | src/utils/api.ts, components/xai/ | **NOT_STARTED** |
| 23 | evaluation/publication_audit_v2/v4_reconciliation/reproduce_v4.py | EVALUATION | **A+** | Authoritative V4 reproduction script | Recalculates canonical retrieval & grounding | 4 questions (N=90 split, Hit@20=0.867, claim count) | evaluation/Re-evaluation of mistakes/ | **NOT_STARTED** |

---

## 2. Secondary Preparation: 40 A-Level Modules

Reviewers may ask architectural or integration questions regarding these supporting modules:

| No. | File Path | Category | Importance | Role in Architecture |
|---|---|---|---|---|
| 1 | src/main.tsx | FRONTEND_ENTRY | A | ReactDOM root bootstrap and provider mounting |
| 2 | src/utils/apiAdapter.ts | FRONTEND_API_SERVICES | A | Adapter transforming backend DTOs to UI model contracts |
| 3 | src/pages/DashboardPage.tsx | FRONTEND_PAGES | A | Workspace overview and recent synthesis metrics |
| 4 | src/pages/ResearchPage.tsx | FRONTEND_PAGES | A | Literature exploration and topic workspace |
| 5 | src/pages/PaperReaderPage.tsx | FRONTEND_PAGES | A | Deep paper inspection with linked citation annotations |
| 6 | src/pages/AnalyticsPage.tsx | FRONTEND_PAGES | A | Corpus search analytics and query frequency metrics |
| 7 | src/pages/ComparisonPage.tsx | FRONTEND_PAGES | A | Direct side-by-side comparison between 2+ papers |
| 8 | src/store/authStore.ts | FRONTEND_STATE | A | Zustand store for authentication and active session token |
| 9 | src/store/paperStore.ts | FRONTEND_STATE | A | Zustand store for cached paper search results and selected corpus |
| 10 | src/store/researchStore.ts | FRONTEND_STATE | A | Zustand store for synthesis outputs and matrix states |
| 11 | src/store/sessionStore.ts | FRONTEND_STATE | A | Zustand store for multi-turn assistant session history |
| 12 | src/store/workspaceStore.ts | FRONTEND_STATE | A | Zustand store for custom user research collections |
| 13 | src/store/xaiStore.ts | FRONTEND_STATE | A | Zustand store for active provenance graph and token weights |
| 14 | ackend/app/core/config.py | CONFIGURATION | A | Pydantic BaseSettings for database URIs, API keys, and model paths |
| 15 | ackend/app/db/session.py | DATABASE | A | SQLAlchemy database engine and sessionmaker dependency |
| 16 | ackend/app/models/document.py | DATABASE | A | ORM model for user-uploaded research documents |
| 17 | ackend/app/models/workspace.py | DATABASE | A | ORM model for user project workspaces |
| 18 | ackend/app/models/session.py | DATABASE | A | ORM model for research chat and assistant sessions |
| 19 | ackend/app/models/search_history.py | DATABASE | A | ORM model tracking user queries and click-through provenance |
| 20 | ackend/app/api/literature_review.py | API | A | Dedicated controller for literature review generation endpoints |
| 21 | ackend/app/api/knowledge_base.py | API | A | API routes for inspecting local KB status and document statistics |
| 22 | ackend/app/api/search_history.py | API | A | API routes for retrieving past query traces |
| 23 | ackend/app/api/evaluation.py | API | A | API routes serving benchmark results to the frontend console |
| 24 | ackend/app/services/assistant/claim_extractor.py | CLAIM_VERIFICATION | A | Regex and LLM-assisted atomic claim decomposition |
| 25 | ackend/app/services/assistant/contradiction_detector.py | CLAIM_VERIFICATION | A | Semantic cross-paper contradiction and disagreement detector |
| 26 | ackend/app/services/assistant/eligibility.py | CLAIM_VERIFICATION | A | Gatekeeper evaluating whether claims meet factual verification criteria |
| 27 | ackend/app/services/research_artifact_service.py | CITATION_PROVENANCE_XAI | A | Assembles citation provenance graphs and artifact bundles |
| 28 | ackend/app/services/research_memory_service.py | CITATION_PROVENANCE_XAI | A | Maintains session memory and cross-query research context |
| 29 | ackend/app/services/assistant/synthesis_extractor.py | CITATION_PROVENANCE_XAI | A | Extracts structured sections and citations from raw LLM output |
| 30 | ackend/app/services/assistant/gap_analyzer.py | CITATION_PROVENANCE_XAI | A | Identifies unaddressed research gaps across compared literature |
| 31 | hybrid_retriever.py | RETRIEVAL | A | Standalone CLI hybrid retrieval baseline implementation |
| 32 | evidence_layer.py | RETRIEVAL | A | Standalone passage extraction and evidence scoring script |
| 33 | 
un_e04_eval.py | EVALUATION | A | Benchmark runner script for Experiment E04 (generation grounding) |
| 34 | 
un_e05_eval.py | EVALUATION | A | Benchmark runner script for Experiment E05 (claim verification) |
| 35 | 
un_e07_authoritative.py | EVALUATION | A | Benchmark runner script for Experiment E07 (iterative refinement) |
| 36 | 
un_e08_xai_evaluation.py | EVALUATION | A | Benchmark runner script for Experiment E08 (XAI provenance completeness) |
| 37 | 
un_e10_ablation_study.py | EVALUATION | A | Benchmark runner script for Experiment E10 (component ablation study) |
| 38 | 
un_e11_reconciled.py | EVALUATION | A | Benchmark runner script for Experiment E11 (error taxonomy reconciliation) |
| 39 | 
ebuild_results_freeze_canonical.py | EVALUATION | A | Rebuilds canonical results freeze directory from authoritative runs |
| 40 | 
un_module1_evaluations.py | EVALUATION | A | Evaluates Module 1 retrieval metrics (BM25, Dense, Hybrid, Rerank) |

---

## 3. Supporting Material (B & C Levels)

- **282 B-Level Files:** UI widgets, external API connectors (arXiv, OpenAlex, Crossref), test suites (ackend/app/tests/*), and secondary models. Study on an as-needed basis.
- **320 C-Level Files:** Static dataset artifacts, historical one-time patches (ix_*.py), scratch scripts (scratch/*), and archived reports. **Do not spend review preparation time on these.**
