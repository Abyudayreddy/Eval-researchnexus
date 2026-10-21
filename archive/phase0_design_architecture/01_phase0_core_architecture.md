# ResearchNexus AI — Phase 0: Core Architecture

## Product Identity
ResearchNexus AI is an Explainable Research Assistant using Hybrid Retrieval, Evidence-Centric XAI, and Enhanced RAG.
It is a serious Research Operating System focused on:
DISCOVER → UNDERSTAND → VERIFY → COMPARE → SYNTHESIZE → ORGANIZE.

It is NOT a generic SaaS, a Google Scholar clone, a generic chatbot, or a project-management app.

## Core Research Lifecycle
1. RESEARCH QUESTION
2. DISCOVERY (Research Explorer)
3. RETRIEVAL
4. EVIDENCE (Evidence & Proof)
5. UNDERSTANDING (AI Research Assistant)
6. EXPLAINABILITY (XAI)
7. COMPARISON
8. SYNTHESIS (Literature Builder)
9. VERIFICATION
10. ORGANIZATION (Projects / Notebook / Library)

## Module Responsibilities
- **Research Explorer**: Answers "What should I read?" (Submits query, runs Local + Online, shows live retrieval state, relevant papers, exposes evidence, links to XAI and AI Assistant).
- **AI Research Assistant**: Answers "What does this research tell me?" (Supports open research, single-paper, multi-paper, project context). Must be evidence-grounded.
- **XAI**: Answers "Why did this result appear?" (Exposes query understanding, retrieval, ranking, evidence, source provenance).
- **Literature Builder**: Answers "What does the body of literature collectively show?"
- **Projects**: Persistent research workspace. Contains papers, evidence, notes. (No independent retrieval engine).
- **Notebook**: Stores notes, paper/evidence references, citations. Preserves provenance.
- **Library**: Stores/curates saved papers, collections. (No independent retrieval).

## Core Object Model (Contracts)
### SearchExperiment
- `search_id`, `query`, `created_at`, `user_id`
- `overall_status`, `stage`, `progress`
- `local_status`, `online_status`
- `local_metrics`, `online_metrics`, `combined_metrics`
- `local_trace`, `online_trace`, `combined_trace`
- `local_results`, `online_results`, `combined_results`

### Paper
- `paper_id`, `title`, `authors`, `abstract`, `keywords`, `publication_year`, `publication_date`
- `journal`, `conference`, `publisher`, `doi`
- `domain`, `subdomain`
- `source_repository`, `source_id`, `paper_url`, `pdf_path`, `read_source`
- `retrieval_source`
*(Note: Do not fabricate missing metadata)*

### Evidence
- `evidence_id`, `paper_id`, `chunk_id`, `retrieval_source`
- `section`, `page_start`, `page_end`
- `evidence_text`
- `retrieval_score`, `rrf_score`, `reranker_score`
- `evidence_status`
*(Note: Represent unavailable values honestly)*

### ResearchContext
- `context_id`
- `context_mode`: OPEN_RESEARCH, SINGLE_PAPER, MULTI_PAPER, UPLOADED_DOCUMENT, PROJECT
- `search_id`, `selected_papers`, `uploaded_documents`, `project_id`
- `allowed_evidence_sources`

### AIResponse
- `response_id`, `context_id`, `answer`
- `claims`, `citations`, `evidence_refs`, `source_breakdown`
*(Note: Do not generate citation objects without actual source evidence)*

### XAITrace
- `search_id`, `source` (local / online / mixed)
- `stages[]`, `metrics`, `candidates`, `final_results`
*(Note: Every stage must represent something actually executed)*

## Source Architecture
Two independent evidence providers:
- **LOCAL**: PostgreSQL + BM25 + ChromaDB + RRF + BGE reranking.
- **ONLINE**: Existing RepositoryRouter + existing connectors/normalization/ranking. (Do not modify existing online implementation during Phase 0).

## AI / XAI Boundaries
- **XAI**: "HOW did ResearchNexus retrieve this?"
- **AI Assistant**: "WHAT does the evidence mean?"
- **Evidence**: "WHERE is the proof?"
- **Literature Builder**: "WHAT does the literature collectively indicate?"

## Enhanced RAG Definition
Conceptual Definition:
QUERY → Hybrid Retrieval → Candidate Fusion → Evidence Validation → Reranking → Evidence Selection → Structured Context → LLM Generation → Claim/Citation Mapping → Evidence Verification → Final Answer.

## Current Codebase Review
### Existing to Preserve
- `backend/app/api/`, `backend/app/services/` (Current retrieval services, API utilities, AI, XAI endpoints).
- Existing Database schemas, ChromaDB integrations.
- Current React frontend components structure (`src/components`, `src/pages`).

### Planned Reconstruction (To Implement Later)
- Deep integration of the strict `ResearchContext` model across AI Assistant.
- Full UI alignment with Phase 0 Design System (Explorer, XAI, Assistant).
- Enhanced Literature Builder and Notebook.
