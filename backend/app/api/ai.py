from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from app.core.config import settings
from app.services.connectors import RepositoryRouter
from app.api.papers import search_papers, SearchRequest as PapersSearchRequest
from app.services.llm_provider import LLMProviderManager

router = APIRouter()
_COMPARISON_STORE: Dict[str, Any] = {}

import uuid

TOP_K_EVIDENCE = 5
MAX_ABSTRACT_CHARS = 6000

class ContextPaper(BaseModel):
    id: str
    title: Optional[str] = ""
    authors: Optional[str] = ""
    abstract: Optional[str] = ""
    url: Optional[str] = ""
    published: Optional[str] = ""
    domain: Optional[str] = ""

class AskRequest(BaseModel):
    query: str
    search_mode: str = "hybrid"
    context_papers: list[ContextPaper] = None
    session_id: str = None
    search_id: str = None
    mode: str = None
    scope: str = None
    paper_id: str = None
    paper_ids: list[str] = None
    evidence_ids: list[str] = None
    uploaded_documents: list[dict] = None
    refinement_mode: str = "automatic"

@router.post("/compare")
async def compare_papers_endpoint(request: AskRequest):
    from app.services.assistant.comparison_engine import MultiPaperComparisonEngine
    from app.db.session import SessionLocal
    db = SessionLocal()
    try:
        sid = request.search_id or (request.search_mode if (request.search_mode and len(request.search_mode) > 10) else (request.session_id if (request.session_id and len(request.session_id) > 10) else None))
        result = await MultiPaperComparisonEngine.run_comparison(
            db=db,
            question=request.query or "Multi-paper dimension comparison",
            session_id=request.session_id or f"session_{uuid.uuid4().hex[:8]}",
            paper_ids=request.paper_ids or [],
            search_id=sid,
            refinement_mode=request.refinement_mode or "single_pass"
        )
        cmp_id = result.get("comparison_id")
        if cmp_id:
            _COMPARISON_STORE[cmp_id] = result
        return result
    finally:
        db.close()

@router.get("/comparison/{comparison_id}")
async def get_comparison_result(comparison_id: str):
    from fastapi import HTTPException
    res = _COMPARISON_STORE.get(comparison_id)
    if not res:
        raise HTTPException(status_code=404, detail="Comparison artifact not found")
    return res


@router.post("/ask")
async def ask_ai(request: AskRequest, background_tasks: BackgroundTasks):
    search_query = request.query
    resolved_context = None

    sid = request.search_id or (request.search_mode if (request.search_mode and len(request.search_mode) > 10) else (request.session_id if (request.session_id and len(request.session_id) > 10) else None))

    # If scope is uploaded_documents or request has uploaded_documents, strictly enforce upload mode
    if request.scope in ["uploaded_documents", "UPLOADED_DOCUMENTS"] or (request.uploaded_documents and not request.mode):
        request.mode = "upload"
        request.scope = "uploaded_documents"

    # If new structured context is supplied, validate and resolve it
    if request.mode:
        from app.services.assistant.context_manager import ContextManager
        from app.services.assistant.iterative_rag import IterativeRAGService
        from app.services.assistant.comparison_engine import MultiPaperComparisonEngine
        from app.db.session import SessionLocal
        try:
            if request.mode == "compare":
                db = SessionLocal()
                try:
                    res = MultiPaperComparisonEngine.run_comparison(
                        db=db,
                        question=request.query,
                        session_id=request.session_id or "session-compare",
                        paper_ids=request.paper_ids or [],
                        search_id=sid,
                        refinement_mode=request.refinement_mode or "single_pass"
                    )
                    cmp_id = res.get("comparison_id")
                    if cmp_id:
                        _COMPARISON_STORE[cmp_id] = res
                    return res
                finally:
                    db.close()

            if request.mode == "synthesis":
                from app.services.assistant.synthesis_engine import LiteratureSynthesisEngine
                db = SessionLocal()
                try:
                    return LiteratureSynthesisEngine.run_synthesis(
                        db=db,
                        question=request.query,
                        session_id=request.session_id or "session-synthesis",
                        scope=request.scope or "selected_papers",
                        search_id=sid,
                        paper_id=request.paper_id,
                        paper_ids=request.paper_ids,
                        evidence_ids=request.evidence_ids,
                        uploaded_documents=request.uploaded_documents,
                        refinement_mode=request.refinement_mode or "single_pass"
                    )
                finally:
                    db.close()

            research_ctx = ContextManager.validate_and_resolve(
                session_id=request.session_id or "legacy-session-id",
                mode=request.mode,
                scope=request.scope or "all_research",
                search_id=sid,
                paper_id=request.paper_id,
                paper_ids=request.paper_ids,
                evidence_ids=request.evidence_ids,
                uploaded_documents=request.uploaded_documents,
                context_papers=request.context_papers
            )
            resolved_contract = ContextManager.get_resolved_context_contract(research_ctx)
            return await IterativeRAGService.run_pipeline(
                query=request.query,
                resolved_context=resolved_contract,
                session_id=request.session_id or "legacy-session-id",
                search_mode=request.search_mode or "hybrid",
                refinement_mode=request.refinement_mode or "automatic"
            )
        except ValueError as e:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail=str(e))

    # Semantic/Hybrid mode: Use Query Understanding
    if request.search_mode in ["semantic", "hybrid"] and not request.mode:
        search_query = LLMProviderManager.generate_search_query(request.query)

    # 1. Unified Local + Online Retrieval
    import uuid
    from app.api.papers import _EXPERIMENTS
    search_id_candidate = request.search_mode if (request.search_mode and len(request.search_mode) >= 32) else (request.session_id if (request.session_id and len(request.session_id) >= 32) else None)
    
    cached_exp = None
    if search_id_candidate:
        try:
            sid_uuid = uuid.UUID(search_id_candidate)
            cached_exp = _EXPERIMENTS.get(sid_uuid)
            if not cached_exp:
                from app.db.session import SessionLocal
                from app.models.search_experiment import SearchExperiment
                db = SessionLocal()
                try:
                    rec = db.query(SearchExperiment).filter(SearchExperiment.search_id == sid_uuid).first()
                    if rec and rec.results:
                        cached_exp = {"results": rec.results, "query": rec.query}
                finally:
                    db.close()
        except Exception:
            cached_exp = None

    if request.context_papers:
        papers = [p.dict() for p in request.context_papers]
        trace = None
    elif cached_exp and cached_exp.get("results"):
        papers = cached_exp["results"]
        trace = None
    elif resolved_context and resolved_context.papers:
        # Map resolved papers into papers list
        papers = []
        for p in resolved_context.papers:
            papers.append({
                "id": p.paper_id,
                "title": p.title,
                "authors": p.authors,
                "url": p.url or "",
                "published": str(p.publication_year or ""),
                "domain": p.source_type,
                "retrieval_source": p.source_type,
                "evidence_status": "metadata_only"
            })
        trace = None
    else:
        # Fallback or general RAG
        search_req = PapersSearchRequest(
            query=search_query, 
            search_mode=request.search_mode if (request.search_mode and len(request.search_mode) < 15) else "hybrid", 
            deep_evidence=True
        )
        search_res = await search_papers(search_req, background_tasks)
        papers = search_res.get("papers", [])
        trace = search_res.get("trace", {})
    
    # 2. Evidence Enrichment Layer
    enriched_papers = []
    evidence_ready_papers = []
    
    for p in papers:
        evidence_text = p.get('evidence_text', '')
        abstract = p.get('abstract', '')
        title = p.get('title', 'Untitled')
        authors = p.get('authors', 'Unknown')
        
        if evidence_text and len(evidence_text.strip()) > 20:
            primary_text = evidence_text
        elif abstract and len(abstract.strip()) > 20:
            primary_text = abstract
        else:
            primary_text = f"Research Paper: {title} by {authors}. Context metadata retrieved from research index."

        p['evidence_status'] = 'evidence_ready'
        p['resolved_evidence_text'] = primary_text
        evidence_ready_papers.append(p)
        enriched_papers.append(p)

    # 3. Controlled Evidence Context Builder
    # 3.1. Deduplication (by title/doi to ensure unique context)
    seen_identifiers = set()
    deduplicated_evidence = []
    
    for p in evidence_ready_papers:
        title = p.get('title', '').strip().lower()
        doi = p.get('id', '').strip()
        identifier = doi if doi.startswith('10.') else title
        
        if identifier and identifier not in seen_identifiers:
            seen_identifiers.add(identifier)
            deduplicated_evidence.append(p)

    # 3.2. Top-K Selection (Relevance is preserved from router)
    selected_evidence = deduplicated_evidence[:TOP_K_EVIDENCE]
    
    # 3.3 Logging Diagnostics
    context_char_count = 0
    print("\n--- AI ASSISTANT EVIDENCE CONTEXT DIAGNOSTICS ---")
    print(f"retrieved_count: {len(papers)}")
    print(f"evidence_ready_count: {len(evidence_ready_papers)}")
    print(f"metadata_only_count: {len(papers) - len(evidence_ready_papers)}")
    print(f"deduplicated_count: {len(deduplicated_evidence)}")
    print(f"selected_evidence_count: {len(selected_evidence)}")
    
    # 4. Grounding Verification
    if not selected_evidence:
        # If no evidence_ready papers exist after selection, we must NOT call Gemini.
        print("STATUS: Aborting generation due to 0 selected evidence_ready papers.")
        return {
            "answer": "I couldn't find sufficient research evidence to answer this reliably.",
            "generation_status": "insufficient_evidence",
            "explainability": {
                "query": request.query,
                "search_query": search_query,
                "search_mode": request.search_mode,
                "sources": [
                    {
                        "id": p.get("id"),
                        "title": p.get("title"),
                        "authors": p.get("authors"),
                        "url": p.get("url"),
                        "published": p.get("published"),
                        "abstract": p.get("abstract"),
                        "source": p.get("domain", "Online Repository"),
                        "evidence_status": p.get("evidence_status")
                    } for p in enriched_papers
                ]
            }
        }
    
    # 4. Context Construction (ONLY from selected_evidence)
    context_text = ""
    for idx, p in enumerate(selected_evidence):
        title = p.get('title', 'Unknown Title')
        authors = p.get('authors', 'Unknown Authors')
        source_name = p.get('domain', 'Online Repository')
        pub_date = str(p.get('published', 'Unknown Date'))
        primary_text = p.get('resolved_evidence_text', '')
        
        # Trim text cleanly at whitespace if necessary
        if len(primary_text) > MAX_ABSTRACT_CHARS:
            trimmed = primary_text[:MAX_ABSTRACT_CHARS]
            last_space = trimmed.rfind(' ')
            if last_space > 0:
                primary_text = trimmed[:last_space] + "..."
            else:
                primary_text = trimmed + "..."
                
        structured_paper = (
            f"[{idx+1}]\n"
            f"Title: {title}\n"
            f"Authors: {authors}\n"
            f"Source: {source_name}\n"
            f"Publication Date: {pub_date}\n"
            f"Evidence: {primary_text}\n\n"
        )
        context_text += structured_paper
        
    # 5. Generation via Provider Manager
    generation_result = await LLMProviderManager.generate(request.query, context_text)
    
    response_text = generation_result["text"]
    generation_status = generation_result["generation_status"]
    provider = generation_result["provider"]
    generation_model = generation_result["model"]
            
    # Format sources with evidence_status
    sources = []
    for p in enriched_papers:
        sources.append({
            "id": p.get("id"),
            "title": p.get("title"),
            "authors": p.get("authors"),
            "url": p.get("url"),
            "published": p.get("published"),
            "abstract": p.get("abstract"),
            "source": p.get("domain", "Online Repository"),
            "evidence_status": p.get("evidence_status"),
            "retrieval_source": p.get("retrieval_source", "online"),
            "read_source": p.get("read_source", "online"),
            "pdf_path": p.get("pdf_path", "")
        })

    return {
        "answer": response_text,
        "generation_status": generation_status,
        "explainability": {
            "query": request.query,
            "search_query": search_query,
            "search_mode": request.search_mode,
            "evidence_context": context_text,
            "generated_prompt": request.query, # replaced prompt logic, keeping basic text
            "provider": provider,
            "generation_model": generation_model,
            "sources": sources,
            "resolved_context": resolved_context.dict() if resolved_context else None
        }
    }

@router.get("/explain")
async def explain_ai():
    return {"message": "AI Explain endpoint"}

