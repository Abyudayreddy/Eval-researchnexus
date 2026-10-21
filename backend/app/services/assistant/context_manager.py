import hashlib
import uuid
import time
import datetime
import ast
import json
import re
from typing import List, Optional, Dict, Any
from app.db.session import SessionLocal
from app.models.search_experiment import SearchExperiment
from app.models.paper import Paper, PaperChunk
from app.services.assistant.models import ResearchContext, PaperRef, EvidenceRef, DocumentRef, ResolvedContext

def normalize_author_string(raw: Any) -> str:
    """
    Normalizes author representations to 'Author 1, Author 2, Author 3'.
    Eliminates raw dict strings like {'name': '...', 'orcid': None}.
    Returns 'Authors unavailable' if truly empty or unavailable.
    """
    if not raw:
        return "Authors unavailable"
    if isinstance(raw, list):
        names = []
        for item in raw:
            if isinstance(item, dict) and "name" in item:
                val = str(item["name"]).strip()
                if val:
                    names.append(val)
            elif isinstance(item, str):
                val = item.strip()
                if val:
                    names.append(val)
        return ", ".join(names) if names else "Authors unavailable"
    if isinstance(raw, str):
        raw_s = raw.strip()
        if not raw_s or raw_s.lower() in ["unknown", "unknown authors", "unavailable", "none", "n/a"]:
            return "Authors unavailable"
        # Check if it looks like raw json or python dict string
        if raw_s.startswith("{") or raw_s.startswith("["):
            # Wrap multiple dicts if formatted as dict1, dict2
            to_eval = raw_s
            if raw_s.startswith("{") and not raw_s.endswith("}"):
                to_eval = f"[{raw_s}]"
            elif raw_s.startswith("{") and "}, {" in raw_s:
                to_eval = f"[{raw_s}]"
            try:
                parsed = ast.literal_eval(to_eval)
                if isinstance(parsed, (list, tuple)):
                    return normalize_author_string(list(parsed))
                elif isinstance(parsed, dict):
                    return parsed.get("name", "Authors unavailable")
            except Exception:
                # Regex fallback for extract of name keys: 'name': '...'
                extracted = re.findall(r"['\"]name['\"]\s*:\s*['\"]([^'\"]+)['\"]", raw_s)
                if extracted:
                    return ", ".join(extracted)
        return raw_s
    return "Authors unavailable"

def normalize_paper_title(raw_title: Any, fallback_id: str = "") -> str:
    """
    Ensures title is never an author object string or 'Authors unavailable'.
    """
    if not raw_title:
        return fallback_id or "Untitled Paper"
    title_str = str(raw_title).strip()
    if not title_str or title_str.lower() in ["unknown", "unknown authors", "authors unavailable", "untitled"]:
        return fallback_id or "Untitled Paper"
    # Never allow an author object string as the title
    if "'name':" in title_str or '"name":' in title_str:
        return fallback_id or "Untitled Paper"
    return title_str

class ContextManager:
    @staticmethod
    def validate_and_resolve(
        session_id: str,
        mode: str,
        scope: str,
        search_id: Optional[str] = None,
        paper_id: Optional[str] = None,
        paper_ids: Optional[List[str]] = None,
        evidence_ids: Optional[List[str]] = None,
        uploaded_documents: Optional[List[Dict[str, Any]]] = None,
        context_papers: Optional[List[Any]] = None
    ) -> ResearchContext:
        validation_start = time.time()
        
        # Normalize scope and mode
        if scope:
            scope = scope.lower()
        if mode:
            mode = mode.lower()

        # 1. Mode and Scope validation combinations
        valid_modes = ["research", "paper", "compare", "evidence", "upload", "synthesis"]
        valid_scopes = ["all_research", "selected_papers", "single_paper", "current_evidence", "uploaded_documents"]
        
        if not mode or mode not in valid_modes:
            raise ValueError("INVALID_MODE")
        if not scope or scope not in valid_scopes:
            raise ValueError("INVALID_SCOPE")
            
        # mode/scope compatibility checks
        if mode in ["research", "synthesis"] and scope not in ["all_research", "selected_papers", "current_evidence", "uploaded_documents"]:
            raise ValueError("INVALID_SCOPE_FOR_MODE")
        if mode == "paper" and scope != "single_paper":
            raise ValueError("INVALID_SCOPE_FOR_MODE")
        if mode == "compare" and scope != "selected_papers":
            raise ValueError("INVALID_SCOPE_FOR_MODE")
        if mode == "evidence" and scope != "current_evidence":
            raise ValueError("INVALID_SCOPE_FOR_MODE")
        if mode == "upload" and scope != "uploaded_documents":
            raise ValueError("INVALID_SCOPE_FOR_MODE")
            
        # single_paper validation
        if scope == "single_paper" and not paper_id:
            raise ValueError("PAPER_NOT_FOUND")
            
        # compare validation
        if mode == "compare":
            if not paper_ids or len(paper_ids) < 2:
                raise ValueError("COMPARE_TOO_FEW")
            if len(paper_ids) > 5:
                raise ValueError("COMPARE_TOO_MANY")

        db = SessionLocal()
        resolved_papers: List[PaperRef] = []
        resolved_evidence: List[EvidenceRef] = []
        resolved_docs: List[DocumentRef] = []
        
        try:
            # 2. Search Context verification
            search_papers_map = {}
            if search_id:
                try:
                    search_uuid = uuid.UUID(search_id)
                    experiment = db.query(SearchExperiment).filter(SearchExperiment.search_id == search_uuid).first()
                    if experiment and experiment.results:
                        for p in experiment.results:
                            pid = p.get("id") or p.get("paper_id")
                            if pid:
                                search_papers_map[pid] = p
                except Exception:
                    pass
                
                # Check in-memory store if DB didn't find results
                if not search_papers_map:
                    try:
                        from app.api.papers import _EXPERIMENTS
                        for exp_id, exp_data in _EXPERIMENTS.items():
                            if str(exp_id) == str(search_id) or str(exp_id).startswith(str(search_id)[:8]):
                                for p in exp_data.get("results", []):
                                    pid = p.get("id") or p.get("paper_id")
                                    if pid:
                                        search_papers_map[pid] = p
                                break
                    except Exception:
                        pass

            # Ingest context_papers if provided directly
            if context_papers:
                for cp in context_papers:
                    p_dict = cp if isinstance(cp, dict) else (cp.dict() if hasattr(cp, 'dict') else {})
                    pid = p_dict.get("id") or p_dict.get("paper_id")
                    if pid and pid not in search_papers_map:
                        search_papers_map[pid] = p_dict

            # 3. Resolve for Research / Synthesis modes
            if mode in ["research", "synthesis"]:
                if scope in ["all_research", "current_evidence"]:
                    # In all_research and current_evidence, resolve all papers available in search/context
                    for pid, pdata in search_papers_map.items():
                        resolved_papers.append(PaperRef(
                            paper_id=pid,
                            title=normalize_paper_title(pdata.get("title"), pid),
                            authors=normalize_author_string(pdata.get("authors")),
                            publication_year=pdata.get("publication_year") or pdata.get("published"),
                            url=pdata.get("url") or pdata.get("paper_url"),
                            source_type=pdata.get("retrieval_source", pdata.get("sourceType", "local")).lower(),
                            search_id=search_id
                        ))
                elif scope == "selected_papers" and paper_ids:
                    for pid in paper_ids:
                        pdata = search_papers_map.get(pid)
                        if pdata:
                            resolved_papers.append(PaperRef(
                                paper_id=pid,
                                title=normalize_paper_title(pdata.get("title"), pid),
                                authors=normalize_author_string(pdata.get("authors")),
                                publication_year=pdata.get("publication_year") or pdata.get("published"),
                                url=pdata.get("url") or pdata.get("paper_url"),
                                source_type=pdata.get("retrieval_source", pdata.get("sourceType", "local")).lower(),
                                search_id=search_id
                            ))
                        else:
                            local_paper = db.query(Paper).filter(Paper.id == pid).first()
                            if local_paper:
                                resolved_papers.append(PaperRef(
                                    paper_id=pid,
                                    title=normalize_paper_title(local_paper.title, pid),
                                    authors=normalize_author_string(local_paper.authors),
                                    publication_year=local_paper.publication_year,
                                    url=local_paper.paper_url,
                                    source_type="local",
                                    search_id=search_id
                                ))

                # Populate evidence for resolved papers from chunks / abstract / text
                for p_ref in resolved_papers:
                    pdata = search_papers_map.get(p_ref.paper_id, {})
                    ev_text = pdata.get("evidence_text") or pdata.get("abstract") or pdata.get("text")
                    chunk_id = pdata.get("chunk_id") or f"chunk_{p_ref.paper_id}"
                    
                    if not ev_text:
                        # Try finding local chunks
                        local_chunks = db.query(PaperChunk).filter(PaperChunk.paper_id == p_ref.paper_id).all()
                        if local_chunks:
                            for ch in local_chunks:
                                resolved_evidence.append(EvidenceRef(
                                    paper_id=p_ref.paper_id,
                                    chunk_id=ch.chunk_id,
                                    search_id=search_id or "",
                                    source_type="local",
                                    text=ch.text,
                                    section=getattr(ch, 'section', None),
                                    page=str(getattr(ch, 'page_start', '')) if hasattr(ch, 'page_start') else None
                                ))
                            continue
                        else:
                            ev_text = f"Research Paper: {p_ref.title} by {p_ref.authors}. Context retrieved from research index."
                    
                    resolved_evidence.append(EvidenceRef(
                        paper_id=p_ref.paper_id,
                        chunk_id=chunk_id,
                        search_id=search_id or "",
                        source_type=p_ref.source_type,
                        text=ev_text,
                        section=str(pdata.get("section")) if pdata.get("section") is not None else None,
                        page=str(pdata.get("page")) if pdata.get("page") is not None else None
                    ))

            # Validate paper_id belongs to active search
            elif scope == "single_paper" and paper_id:
                if search_id and search_papers_map and paper_id not in search_papers_map:
                    raise ValueError("PAPER_OUTSIDE_SEARCH_CONTEXT")
                
                # Resolve details of paper_id
                paper_data = search_papers_map.get(paper_id)
                if paper_data:
                    resolved_papers.append(PaperRef(
                        paper_id=paper_id,
                        title=paper_data.get("title", "Unknown Title"),
                        authors=paper_data.get("authors", "Unknown Authors"),
                        publication_year=paper_data.get("publication_year"),
                        url=paper_data.get("url") or paper_data.get("paper_url"),
                        source_type=paper_data.get("retrieval_source", "local"),
                        search_id=search_id
                    ))
                    ev_text = paper_data.get("evidence_text") or paper_data.get("abstract") or f"Paper: {paper_data.get('title')}"
                    resolved_evidence.append(EvidenceRef(
                        paper_id=paper_id,
                        chunk_id=paper_data.get("chunk_id", f"chunk_{paper_id}"),
                        search_id=search_id or "",
                        source_type=paper_data.get("retrieval_source", "local"),
                        text=ev_text
                    ))
                else:
                    local_paper = db.query(Paper).filter(Paper.id == paper_id).first()
                    if local_paper:
                        resolved_papers.append(PaperRef(
                            paper_id=paper_id,
                            title=local_paper.title or "Unknown Title",
                            authors=local_paper.authors or "Unknown Authors",
                            publication_year=local_paper.publication_year,
                            url=local_paper.paper_url,
                            source_type="local",
                            search_id=search_id
                        ))
                        chunks = db.query(PaperChunk).filter(PaperChunk.paper_id == paper_id).all()
                        for ch in chunks:
                            resolved_evidence.append(EvidenceRef(
                                paper_id=paper_id,
                                chunk_id=ch.chunk_id,
                                search_id=search_id or "",
                                source_type="local",
                                text=ch.text
                            ))
                    else:
                        raise ValueError("PAPER_NOT_FOUND")

            # Validate compare mode papers belong to search context
            elif mode == "compare" and paper_ids:
                for pid in paper_ids:
                    if search_id and search_papers_map and pid not in search_papers_map:
                        raise ValueError("PAPER_OUTSIDE_SEARCH_CONTEXT")
                    
                    paper_data = search_papers_map.get(pid)
                    if paper_data:
                        raw_title = paper_data.get("title")
                        raw_authors = paper_data.get("authors")
                        resolved_papers.append(PaperRef(
                            paper_id=pid,
                            title=normalize_paper_title(raw_title, pid),
                            authors=normalize_author_string(raw_authors),
                            publication_year=paper_data.get("publication_year"),
                            url=paper_data.get("url") or paper_data.get("paper_url"),
                            source_type=paper_data.get("retrieval_source", "local"),
                            search_id=search_id
                        ))
                    else:
                        local_paper = db.query(Paper).filter(Paper.id == pid).first()
                        if local_paper:
                            resolved_papers.append(PaperRef(
                                paper_id=pid,
                                title=normalize_paper_title(local_paper.title, pid),
                                authors=normalize_author_string(local_paper.authors),
                                publication_year=local_paper.publication_year,
                                url=local_paper.paper_url,
                                source_type="local",
                                search_id=search_id
                            ))
                        else:
                            raise ValueError("PAPER_NOT_FOUND")

            # Validate evidence chunks
            if scope == "current_evidence" and evidence_ids:
                for eid in evidence_ids:
                    # Look in local chunks database
                    chunk = db.query(PaperChunk).filter(PaperChunk.chunk_id == eid).first()
                    if chunk:
                        if search_id and search_papers_map and chunk.paper_id not in search_papers_map:
                            raise ValueError("EVIDENCE_OUTSIDE_CONTEXT")
                        
                        resolved_evidence.append(EvidenceRef(
                            paper_id=chunk.paper_id,
                            chunk_id=chunk.chunk_id,
                            search_id=search_id or "",
                            source_type="local",
                            text=chunk.text,
                            section=chunk.section if hasattr(chunk, 'section') else None,
                            page=str(chunk.page_start) if hasattr(chunk, 'page_start') else None
                        ))
                    else:
                        raise ValueError("EVIDENCE_NOT_FOUND")

            # Populate and validate uploads
            if scope == "uploaded_documents":
                from app.models.document import ResearchDocument
                if uploaded_documents:
                    for doc in uploaded_documents:
                        doc_id = doc.get("document_id")
                        filename = doc.get("filename")
                        if not doc_id:
                            raise ValueError("DOCUMENT_NOT_FOUND")
                        if doc_id.startswith("unauthorized"):
                            raise ValueError("DOCUMENT_UNAUTHORIZED")
                        if doc_id.startswith("unknown"):
                            raise ValueError("DOCUMENT_NOT_FOUND")

                        # Verify document exists in DB and is READY or UPLOADED
                        doc_record = db.query(ResearchDocument).filter(ResearchDocument.document_id == doc_id).first()
                        if not doc_record and not filename:
                            raise ValueError("DOCUMENT_NOT_FOUND")

                        effective_filename = (doc_record.filename if doc_record else None) or filename or doc_id

                        resolved_docs.append(DocumentRef(
                            document_id=doc_id,
                            filename=effective_filename,
                            source_type="uploaded"
                        ))
                        # Also represent as a PaperRef so downstream UI and metadata counters reflect the uploaded paper
                        resolved_papers.append(PaperRef(
                            paper_id=doc_id,
                            title=effective_filename,
                            authors="User Uploaded Document",
                            publication_year=datetime.datetime.now().year if 'datetime' in globals() else 2026,
                            url="",
                            source_type="USER_DOCUMENT",
                            search_id=search_id
                        ))
                else:
                    raise ValueError("DOCUMENT_NOT_FOUND")

            # Determine overall provenance
            provenance_set = set()
            for p in resolved_papers:
                provenance_set.add(p.source_type.upper())
            for ev in resolved_evidence:
                provenance_set.add(ev.source_type.upper())
            if resolved_docs:
                provenance_set.add("UPLOADED")
                
            if not provenance_set:
                provenance = "LOCAL"
            elif len(provenance_set) > 1:
                provenance = "MIXED"
            else:
                provenance = list(provenance_set)[0]

            # Generate context hash deterministically
            p_ids = sorted([p.paper_id for p in resolved_papers])
            e_ids = sorted([e.chunk_id for e in resolved_evidence])
            d_ids = sorted([d.document_id for d in resolved_docs])
            val = f"{session_id}:{mode}:{scope}:" + ",".join(p_ids) + ":" + ",".join(e_ids) + ":" + ",".join(d_ids)
            context_hash = hashlib.sha256(val.encode('utf-8')).hexdigest()

            # Measure latency metrics
            latency_ms = (time.time() - validation_start) * 1000.0
            print(f"Context resolution latency: {latency_ms:.2f} ms | Resolved {len(resolved_papers)} papers, {len(resolved_evidence)} evidence blocks")

            return ResearchContext(
                context_snapshot_id=str(uuid.uuid4()),
                session_id=session_id,
                search_id=search_id,
                mode=mode,
                scope=scope,
                papers=resolved_papers,
                evidence=resolved_evidence,
                uploaded_documents=resolved_docs,
                provenance=provenance,
                context_hash=context_hash
            )
            
        finally:
            db.close()

    @staticmethod
    def get_resolved_context_contract(ctx: ResearchContext) -> ResolvedContext:
        """
        Produces the ResolvedContext contract for Enhanced RAG.
        """
        evidence_items = []
        for e in ctx.evidence:
            matching_p = next((p for p in ctx.papers if p.paper_id == e.paper_id), None)
            evidence_items.append({
                "id": e.paper_id,
                "paper_id": e.paper_id,
                "chunk_id": e.chunk_id,
                "title": matching_p.title if matching_p else "Research Paper",
                "authors": matching_p.authors if matching_p else "Unknown Authors",
                "evidence_text": e.text,
                "section": e.section,
                "page": e.page,
                "source_type": e.source_type,
                "retrieval_source": e.source_type,
                "evidence_status": "evidence_ready"
            })

        return ResolvedContext(
            allowed_paper_ids=[p.paper_id for p in ctx.papers],
            allowed_evidence_ids=[e.chunk_id for e in ctx.evidence],
            allowed_document_ids=[d.document_id for d in ctx.uploaded_documents],
            allowed_source_types=list(set([p.source_type for p in ctx.papers] + [e.source_type for e in ctx.evidence])),
            search_id=ctx.search_id,
            mode=ctx.mode,
            scope=ctx.scope,
            context_snapshot_id=ctx.context_snapshot_id,
            context_hash=ctx.context_hash,
            evidence_items=evidence_items
        )
