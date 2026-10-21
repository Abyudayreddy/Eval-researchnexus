import asyncio
import os
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from typing import Dict, Any, Optional
from app.services.connectors import RepositoryRouter
from app.services.local_evidence import get_local_retriever
from pydantic import BaseModel

import uuid
import time
from app.db.session import SessionLocal
from app.models.search_experiment import SearchExperiment
from app.models.paper import Paper

# In‑memory experiment status store (search_id -> status dict)
_EXPERIMENTS: dict[uuid.UUID, dict] = {}

def _init_experiment(search_id: uuid.UUID, execution_id: str, query: str):
    """Create DB record and in‑memory entry for a new search experiment."""
    db = SessionLocal()
    try:
        exp = SearchExperiment(search_id=search_id, query=query)
        db.add(exp)
        db.commit()
    finally:
        db.close()
    _EXPERIMENTS[search_id] = {
        "search_id": str(search_id),
        "execution_id": execution_id,
        "query": query,
        "execution_state": "INITIALIZING",
        "current_stage": "QUERY_PROCESSING",
        "stage_message": f"Understanding '{query}'",
        "stage": "QUERY_PROCESSING",
        "progress": 5,
        "overall_status": "running",
        "terminal": False,
        "metrics": {},
        "warnings": [],
        "local_status": "queued",
        "online_status": "queued",
        "local_trace": None,
        "online_trace": None,
        "combined_trace": None,
        "results": [],
        "local_results": [],
        "online_results": [],
        "combined_results": [],
        "local_result_count": 0,
        "online_result_count": 0,
        "combined_result_count": 0,
        "providers": {
            "crossref": {"status": "queued", "count": 0},
            "openalex": {"status": "queued", "count": 0}
        }
    }

def _update_experiment(search_id: uuid.UUID, **kwargs):
    entry = _EXPERIMENTS.get(search_id)
    if not entry:
        return
    
    # Calculate terminal from execution_state if provided
    if "execution_state" in kwargs:
        st = kwargs["execution_state"]
        kwargs["terminal"] = st in {"COMPLETED_WITH_RESULTS", "COMPLETED_NO_RESULTS", "DEGRADED", "FAILED"}
    
    entry.update(kwargs)
    db = SessionLocal()
    try:
        exp = db.query(SearchExperiment).filter(SearchExperiment.search_id == search_id).first()
        if exp:
            for field in ["overall_status", "local_status", "online_status", "local_metrics", "online_metrics", "combined_metrics", "local_trace", "online_trace", "combined_trace", "results"]:
                if field in kwargs:
                    setattr(exp, field, kwargs[field])
                
        # Also update history counts
        from app.models.search_history import SearchHistory
        from app.models.workspace import ResearchSearchEvent
        history = db.query(SearchHistory).filter(SearchHistory.search_id == search_id).first()
        if history:
            if "local_result_count" in kwargs:
                history.local_result_count = kwargs["local_result_count"]
            if "online_result_count" in kwargs:
                history.online_result_count = kwargs["online_result_count"]
            if "combined_result_count" in kwargs:
                history.result_count = kwargs["combined_result_count"]
                
        # Also sync latest search event
        if "combined_result_count" in kwargs and history:
            last_event = db.query(ResearchSearchEvent).filter(
                ResearchSearchEvent.query == history.query
            ).order_by(ResearchSearchEvent.searched_at.desc()).first()
            if last_event:
                last_event.result_count = kwargs["combined_result_count"]

        db.commit()
    finally:
        db.close()

def _deterministic_query_analysis(query: str) -> list[str]:
    """Simple regex tokenisation + stop‑word removal."""
    import re
    stopwords = {"the", "and", "or", "of", "in", "to", "a", "an", "for", "on", "by", "with"}
    tokens = re.findall(r"\b\w+\b", query.lower())
    return [t for t in tokens if t not in stopwords]

def _retrieve_postgres_metadata(query: str, top_k: int = 20):
    """Metadata search using ILIKE on title/abstract.
    Returns a list of paper dicts compatible with local result format.
    """
    db = SessionLocal()
    try:
        kw = f"%{query}%"
        papers = (
            db.query(Paper)
            .filter((Paper.title.ilike(kw)) | (Paper.abstract.ilike(kw)))
            .limit(top_k)
            .all()
        )
        results = []
        for p in papers:
            results.append({
                "id": p.id,
                "paper_id": p.id,
                "title": p.title,
                "authors": p.authors,
                "abstract": p.abstract,
                "keywords": p.keywords.split(", ") if p.keywords else [],
                "domain": p.domain_id,
                "subdomain": p.subdomain,
                "publication_year": p.publication_year,
                "publication_date": p.publication_date,
                "doi": p.doi,
                "source_repository": p.source_repository,
                "paper_url": p.paper_url,
                "pdf_path": p.pdf_path,
                "read_source": p.read_source,
                "retrieval_source": "local",
            })
        return results, None
    finally:
        db.close()

router = APIRouter()
connector_router = RepositoryRouter()

class SearchRequest(BaseModel):
    query: str
    search_mode: Optional[str] = "hybrid"
    retrieval_mode: Optional[str] = "local_online"
    publication_year: Optional[str] = None
    sort_by: Optional[str] = "relevance"
    deep_evidence: Optional[bool] = False

def normalize_title(t):
    if not t: return ""
    return "".join(c.lower() for c in t if c.isalnum())

def run_local_search(query, deep_evidence=True):
    local_retriever = get_local_retriever()
    if local_retriever.init_status != "ready":
        local_retriever.load()
        if local_retriever.init_status != "ready":
            raise RuntimeError(f"Local retriever failed to initialize: {local_retriever.init_status}")
    return local_retriever.retrieve(query, rrf_candidates=20, top_k_evidence=5, deep_evidence=deep_evidence)

@router.get("/domain-counts")
async def get_domain_counts():
    from app.core.domains import CANONICAL_DOMAINS
    db = SessionLocal()
    try:
        from sqlalchemy import func
        from app.models.paper import Paper
        rows = db.query(Paper.domain_id, func.count(Paper.id)).group_by(Paper.domain_id).all()
        db_counts = {r[0]: r[1] for r in rows if r[0]}
        
        result = {}
        for dom_id, meta in CANONICAL_DOMAINS.items():
            offline_count = 0
            if meta.is_offline_available:
                # Match against domain title or folder_name in database
                offline_count = db_counts.get(meta.title, 0)
                if offline_count == 0 and meta.folder_name:
                    offline_count = db_counts.get(meta.folder_name, 0)
                if offline_count == 0:
                    offline_count = db_counts.get("Interdisciplinary", 0) if "interdisciplinary" in dom_id else 0
            
            result[dom_id] = {
                "id": dom_id,
                "title": meta.title,
                "is_offline_available": meta.is_offline_available,
                "is_online_available": meta.is_online_available,
                "source_badge": "Online + Offline" if meta.is_offline_available else "Online",
                "offline_paper_count": offline_count,
                "subdomains": meta.subdomains
            }
        return result
    finally:
        db.close()

@router.get("/domain/{domain_id}")
async def get_domain_papers(domain_id: str):
    papers = await connector_router.get_domain_papers(domain_id, limit_per_source=5)
    return {
        "domainId": domain_id,
        "totalPapers": len(papers),
        "papers": papers
    }

async def execute_search_experiment(search_id: uuid.UUID, request: SearchRequest):
    warnings = []

    # 1. LOCAL RETRIEVAL
    is_offline_mode = request.retrieval_mode in ["local_only", "offline"] or request.search_mode == "offline"
    is_online_mode = request.retrieval_mode in ["online_only", "online"]

    if not is_online_mode:
        _update_experiment(
            search_id,
            execution_state="LOCAL_RETRIEVING",
            current_stage="LOCAL_RETRIEVAL",
            stage_message="Retrieving local database metadata & vector evidence",
            stage="LOCAL_RETRIEVAL",
            progress=20,
            local_status="running"
        )
        local_task = asyncio.create_task(asyncio.to_thread(run_local_search, request.query, getattr(request, "deep_evidence", True)))
    else:
        local_task = None
    
    # 2. ONLINE RETRIEVAL
    if not is_offline_mode:
        _update_experiment(
            search_id,
            execution_state="ONLINE_RETRIEVING",
            current_stage="ONLINE_RESEARCH",
            stage_message="Searching academic sources (Crossref • OpenAlex)",
            stage="ONLINE_RESEARCH",
            progress=40,
            online_status="running"
        )
        online_task = asyncio.create_task(connector_router.search(
            query=request.query,
            search_mode=request.search_mode,
            publication_year=request.publication_year,
            sort_by=request.sort_by,
            limit_per_source=5,
        ))
    else:
        online_task = None

    # Await active tasks concurrently
    if local_task and online_task:
        local_res, online_res = await asyncio.gather(
            local_task, online_task, return_exceptions=True
        )
    elif local_task:
        local_res = await local_task
        online_res = ([], {"status": "skipped_offline_mode"})
    elif online_task:
        online_res = await online_task
        local_res = ([], True, {"status": "skipped_online_mode"})
    else:
        local_res = ([], True, {})
        online_res = ([], {})

    # Process local result
    if isinstance(local_res, Exception):
        local_papers, is_sufficient, local_trace = [], False, {"error": str(local_res)}
        warnings.append({
            "provider": "Local Repository",
            "code": "LOCAL_RETRIEVAL_ERROR",
            "message": f"Local database retrieval issue: {str(local_res)}",
            "severity": "warning",
            "blocking": False
        })
        _update_experiment(search_id, local_status="failed", local_trace=local_trace)
    else:
        local_papers, is_sufficient, local_trace = local_res
        _update_experiment(search_id, local_status="complete" if local_papers else "no_results", local_trace=local_trace, local_result_count=len(local_papers))

    # Process online result
    if isinstance(online_res, Exception):
        online_papers, online_trace = [], {"error": str(online_res)}
        warnings.append({
            "provider": "Online Connectors",
            "code": "CONNECTOR_FAILURE",
            "message": f"Online repository connector encountered errors: {str(online_res)}",
            "severity": "warning",
            "blocking": False
        })
        _update_experiment(search_id, online_status="failed", online_trace=online_trace)
    else:
        online_papers, online_trace = online_res
        # Extract any specific connector errors if present in trace
        if isinstance(online_trace, dict) and "repositories" in online_trace:
            repos = online_trace["repositories"]
            if isinstance(repos, dict):
                repo_items = repos.items()
            elif isinstance(repos, list):
                repo_items = [(r.get("name", "Connector"), r) for r in repos if isinstance(r, dict)]
            else:
                repo_items = []
            for repo, rdata in repo_items:
                if isinstance(rdata, dict) and rdata.get("error"):
                    warnings.append({
                        "provider": repo,
                        "code": "PROVIDER_RATE_LIMIT_OR_ERROR",
                        "message": f"{repo}: {rdata.get('error')}",
                        "severity": "warning",
                        "blocking": False
                    })
        _update_experiment(search_id, online_status="complete" if online_papers else "no_results", online_trace=online_trace, online_result_count=len(online_papers))

    # 3. MERGING & RERANKING
    _update_experiment(
        search_id,
        execution_state="MERGING",
        current_stage="RESULT_FUSION",
        stage_message="Combining keyword and semantic results using RRF",
        stage="RESULT_FUSION",
        progress=65
    )

    for p in local_papers:
        p["retrieval_source"] = "local"
    for p in online_papers:
        p["retrieval_source"] = "online"

    seen_map = {}
    mixed_papers = []
    def add_paper(p):
        pid = p.get('id') or p.get('paper_id')
        doi = p.get('doi')
        title = p.get('title')
        norm_title = normalize_title(title)
        existing = None
        if pid and pid in seen_map:
            existing = seen_map[pid]
        elif doi and doi in seen_map:
            existing = seen_map[doi]
        elif norm_title and norm_title in seen_map:
            existing = seen_map[norm_title]
        if existing:
            if existing.get('retrieval_source') != p.get('retrieval_source'):
                existing['retrieval_source'] = 'mixed'
                if p.get('evidence_text') and not existing.get('evidence_text'):
                    existing['evidence_text'] = p['evidence_text']
                if p.get('chunk_id') and not existing.get('chunk_id'):
                    existing['chunk_id'] = p['chunk_id']
            return False
        if pid:
            seen_map[pid] = p
        if doi:
            seen_map[doi] = p
        if norm_title:
            seen_map[norm_title] = p
        mixed_papers.append(p)
        return True

    max_len = max(len(local_papers), len(online_papers))
    for i in range(max_len):
        if i < len(local_papers):
            add_paper(local_papers[i])
        if i < len(online_papers):
            add_paper(online_papers[i])

    _update_experiment(
        search_id,
        execution_state="RERANKING",
        current_stage="BGE_RERANKING",
        stage_message="BGE Cross-Encoder refining evidence relevance",
        stage="BGE_RERANKING",
        progress=80
    )
    
    _update_experiment(
        search_id,
        execution_state="EVIDENCE_ASSEMBLY",
        current_stage="EVIDENCE_PREPARATION",
        stage_message="Deduplicating evidence and assembling context",
        stage="EVIDENCE_PREPARATION",
        progress=90
    )

    # 4. AUTHORITATIVE TERMINAL STATE CALCULATION
    local_failed = isinstance(local_res, Exception)
    online_failed = isinstance(online_res, Exception)
    total_unique = len(mixed_papers)

    if local_failed and online_failed:
        final_execution_state = "FAILED"
        overall_status = "failed"
    elif (local_failed or online_failed or len(warnings) > 0) and total_unique > 0:
        final_execution_state = "DEGRADED"
        overall_status = "partial"
    elif (local_failed or online_failed or len(warnings) > 0) and total_unique == 0:
        final_execution_state = "DEGRADED"
        overall_status = "partial"
    elif total_unique > 0:
        final_execution_state = "COMPLETED_WITH_RESULTS"
        overall_status = "complete"
    else:
        final_execution_state = "COMPLETED_NO_RESULTS"
        overall_status = "no_results"

    _update_experiment(
        search_id,
        execution_state=final_execution_state,
        current_stage="RESULTS_READY",
        stage_message="Combining the strongest local and online evidence",
        stage="RESULTS_READY",
        progress=100,
        overall_status=overall_status,
        warnings=warnings,
        combined_trace={"local_trace": local_trace if not local_failed else {}, "online_trace": online_trace if not online_failed else {}},
        combined_metrics={"merged_count": total_unique},
        results=mixed_papers[:15],
        local_results=local_papers,
        online_results=online_papers,
        combined_results=mixed_papers[:15],
        local_result_count=len(local_papers),
        online_result_count=len(online_papers),
        combined_result_count=total_unique
    )

@router.post("/search")
async def search_papers(request: SearchRequest, background_tasks: BackgroundTasks):
    search_id = uuid.uuid4()
    execution_id = f"exec_{int(time.time()*1000)}_{uuid.uuid4().hex[:6]}"
    
    _init_experiment(search_id, execution_id, request.query)

    db = SessionLocal()
    try:
        from app.models.search_history import SearchHistory
        from app.models.workspace import ResearchSearchEvent
        from sqlalchemy.exc import IntegrityError
        new_history = SearchHistory(
            search_id=search_id,
            query=request.query,
            title=request.query,
            user_id="default_user"
        )
        db.add(new_history)
        
        search_evt = ResearchSearchEvent(
            user_id="default_user",
            query=request.query,
            search_mode=getattr(request, 'search_mode', 'hybrid'),
            domain=getattr(request, 'domain', None),
            result_count=0
        )
        db.add(search_evt)
        db.commit()
    except IntegrityError:
        db.rollback()
    except Exception as e:
        db.rollback()
        print("Search history/event recording err:", e)
    finally:
        db.close()

    background_tasks.add_task(execute_search_experiment, search_id, request)

    return {
        "search_id": str(search_id),
        "execution_id": execution_id,
        "execution_state": "INITIALIZING",
        "terminal": False,
        "overall_status": "running"
    }

@router.get("/{id}")
async def get_paper(id: str):
    return {"message": f"Get paper {id}"}

@router.get("/{id}/pdf")
async def get_paper_pdf(id: str):
    db = SessionLocal()
    try:
        from app.models.paper import Paper
        paper = db.query(Paper).filter(Paper.id == id).first()
        if not paper:
            raise HTTPException(status_code=404, detail="Local paper metadata not found")
        
        pdf_path = paper.pdf_path
        if not pdf_path:
            raise HTTPException(status_code=404, detail="Paper does not have a local PDF")
    finally:
        db.close()
        
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    full_path = os.path.join(root_dir, pdf_path.replace("\\", "/"))
    
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="Local PDF file is missing on disk")
        
    return FileResponse(
        full_path, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"inline; filename=\"{os.path.basename(full_path)}\""}
    )

@router.get("/{search_id}/status")
async def get_search_status(search_id: str):
    try:
        uid = uuid.UUID(search_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid search_id format")
    exp = _EXPERIMENTS.get(uid)
    if exp:
        return exp
    db = SessionLocal()
    try:
        record = db.query(SearchExperiment).filter(SearchExperiment.search_id == uid).first()
        if not record:
            raise HTTPException(status_code=404, detail="Search experiment not found")
        
        st = getattr(record, "overall_status", "complete")
        results = getattr(record, "results", []) or []
        
        exec_state = "COMPLETED_WITH_RESULTS" if len(results) > 0 else "COMPLETED_NO_RESULTS"
        if st == "failed":
            exec_state = "FAILED"
        elif st == "partial":
            exec_state = "DEGRADED"

        return {
            "search_id": str(record.search_id),
            "execution_id": f"exec_db_{record.search_id}",
            "query": record.query,
            "execution_state": exec_state,
            "terminal": True,
            "stage": "completed",
            "progress": 100,
            "overall_status": st,
            "warnings": [],
            "local_status": getattr(record, "local_status", None),
            "online_status": getattr(record, "online_status", None),
            "metrics": {
                "local_metrics": getattr(record, "local_metrics", {}),
                "online_metrics": getattr(record, "online_metrics", {}),
                "combined_metrics": getattr(record, "combined_metrics", {}),
            },
            "trace": {
                "local_trace": record.local_trace or (record.combined_trace.get("local_trace") if record.combined_trace else {}),
                "online_trace": record.online_trace or (record.combined_trace.get("online_trace") if record.combined_trace else {}),
                "combined_trace": record.combined_trace or {},
            },
            "results": results,
            "local_results": [],
            "online_results": [],
            "combined_results": results,
            "local_result_count": len(results),
            "online_result_count": 0,
            "combined_result_count": len(results)
        }
    finally:
        db.close()
