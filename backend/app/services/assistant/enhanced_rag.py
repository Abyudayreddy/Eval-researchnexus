import time
import re
from typing import List, Dict, Any, Optional
from app.db.session import SessionLocal
from app.models.paper import Paper, PaperChunk
from app.services.assistant.models import ResolvedContext, ResearchContext
from app.services.assistant.eligibility import ContextEligibilityEngine, ContextEligibility
from app.services.local_evidence import get_local_retriever
from app.services.llm_provider import LLMProviderManager

class EnhancedRAGService:
    @staticmethod
    async def generate_response(
        query: str,
        resolved_context: ResolvedContext,
        session_id: str,
        search_mode: str = "hybrid"
    ) -> Dict[str, Any]:
        pipeline_start = time.time()
        
        # Stage 1: Context Eligibility Check
        eligibility = ContextEligibilityEngine.evaluate(resolved_context)
        
        t0 = time.time()
        retrieved_evidence: List[Dict[str, Any]] = []
        retrieval_ms = 0.0
        
        # Stage 2: Evidence Selection / Retrieval
        if resolved_context.evidence_items:
            # Use bounded evidence passed directly from resolved context contract
            retrieved_evidence = list(resolved_context.evidence_items)
            retrieval_ms = (time.time() - t0) * 1000.0
        elif not eligibility.should_retrieve:
            # Rule 3: current_evidence = zero retrieval (Fetch exact evidence objects from DB)
            db = SessionLocal()
            try:
                if eligibility.allowed_evidence_ids:
                    chunks = db.query(PaperChunk).filter(PaperChunk.chunk_id.in_(eligibility.allowed_evidence_ids)).all()
                    chunk_by_id = {c.chunk_id: c for c in chunks}
                    p_ids = list(set([c.paper_id for c in chunks]))
                    papers = db.query(Paper).filter(Paper.id.in_(p_ids)).all() if p_ids else []
                    paper_by_id = {p.id: p for p in papers}
                    
                    for eid in eligibility.allowed_evidence_ids:
                        chunk = chunk_by_id.get(eid)
                        if chunk:
                            paper = paper_by_id.get(chunk.paper_id)
                            retrieved_evidence.append({
                                "id": chunk.paper_id,
                                "paper_id": chunk.paper_id,
                                "chunk_id": chunk.chunk_id,
                                "title": paper.title if paper else "Unknown Title",
                                "authors": paper.authors if paper else "Unknown Authors",
                                "evidence_text": chunk.text,
                                "section": getattr(chunk, 'section', None),
                                "page": str(getattr(chunk, 'page_start', '')) if hasattr(chunk, 'page_start') else None,
                                "source_type": "local",
                                "retrieval_source": "local",
                                "evidence_status": "evidence_ready"
                            })
            finally:
                db.close()
            retrieval_ms = (time.time() - t0) * 1000.0
            # Execute bounded retrieval based on scope
            local_evidence = []
            if eligibility.can_use_uploads and eligibility.allowed_document_ids:
                from app.services.document_service import UploadedDocumentRetriever
                db = SessionLocal()
                try:
                    upload_evidence = UploadedDocumentRetriever.retrieve(
                        db=db,
                        query=query,
                        allowed_document_ids=eligibility.allowed_document_ids,
                        top_k=5
                    )
                    local_evidence.extend(upload_evidence)
                finally:
                    db.close()
            elif eligibility.can_use_local:
                local_retriever = get_local_retriever()
                if local_retriever.init_status != "ready":
                    local_retriever.load()
                
                if local_retriever.init_status == "ready":
                    allowed_pids = eligibility.allowed_paper_ids if eligibility.allowed_paper_ids else None
                    ev_list, is_sufficient, trace = local_retriever.retrieve(
                        query=query,
                        top_k_evidence=5,
                        deep_evidence=True,
                        allowed_paper_ids=allowed_pids
                    )
                    local_evidence.extend(ev_list)
                    
            retrieved_evidence = local_evidence
            retrieval_ms = (time.time() - t0) * 1000.0

        # Stage 3: Evidence Deduplication ((source_type, paper_id, chunk_id))
        t_dedup = time.time()
        seen_identity = set()
        deduplicated_evidence = []
        
        for ev in retrieved_evidence:
            source_type = ev.get("source_type", ev.get("retrieval_source", "local"))
            pid = ev.get("paper_id", ev.get("id", ""))
            cid = ev.get("chunk_id", pid)
            identity = (source_type, pid, cid)
            
            if identity not in seen_identity:
                seen_identity.add(identity)
                ev["canonical_identity"] = identity
                deduplicated_evidence.append(ev)
                
        evidence_selection_ms = (time.time() - t_dedup) * 1000.0
        
        # Grounding check - if zero evidence
        is_upload_mode = resolved_context.scope in ["uploaded_documents", "UPLOADED_DOCUMENTS"]
        if not deduplicated_evidence:
            total_ms = (time.time() - pipeline_start) * 1000.0
            zero_evidence_answer = (
                "No matching content was found in the uploaded paper."
                if is_upload_mode
                else "Insufficient evidence in the selected research context to answer this question."
            )
            return {
                "answer": zero_evidence_answer,
                "generation_status": "insufficient_evidence",
                "claims": [],
                "citations": [],
                "evidence": [],
                "sources": [],
                "context_snapshot_id": resolved_context.context_snapshot_id,
                "context_hash": resolved_context.context_hash,
                "search_id": resolved_context.search_id,
                "session_id": session_id,
                "evidence_manifest": {
                    "question": query,
                    "scope": resolved_context.scope,
                    "mode": resolved_context.mode,
                    "retrieved_candidates": 0,
                    "selected_evidence_count": 0,
                    "citation_mapping": {},
                    "source_distribution": {"local": 0, "online": 0, "uploaded": 0}
                },
                "metadata": {
                    "context_resolution_ms": 0.0,
                    "retrieval_ms": round(retrieval_ms, 2),
                    "evidence_selection_ms": round(evidence_selection_ms, 2),
                    "context_build_ms": 0.0,
                    "generation_ms": 0.0,
                    "total_ms": round(total_ms, 2)
                }
            }

        # Stage 4: Deterministic Context Construction & Citation ID Mapping
        t_build = time.time()
        context_text = ""
        citation_map = {}  # index int -> evidence dict
        citations_output = []
        
        for idx, ev in enumerate(deduplicated_evidence, 1):
            citation_id = f"[{idx}]"
            ev_text = ev.get("evidence_text", ev.get("resolved_evidence_text", ev.get("abstract", "")))
            title = ev.get("title", ev.get("filename", "Unknown Title"))
            authors = ev.get("authors", "Unknown Authors")
            source_type = ev.get("source_type", ev.get("retrieval_source", "local"))
            page_info = f", Page {ev.get('page')}" if ev.get("page") else ""
            section_info = f", Section: {ev.get('section')}" if ev.get("section") else ""
            
            context_text += (
                f"CITATION {citation_id}:\n"
                f"Source: {source_type}\n"
                f"Document/Paper: {title}{page_info}{section_info}\n"
                f"Authors: {authors}\n"
                f"Evidence: {ev_text}\n\n"
            )
            
            citation_map[idx] = ev
            citations_output.append({
                "citation_id": citation_id,
                "numeric_id": idx,
                "paper_id": ev.get("paper_id", ev.get("id")),
                "chunk_id": ev.get("chunk_id"),
                "title": title,
                "source_type": source_type,
                "page": ev.get("page"),
                "section": ev.get("section")
            })
            
        context_build_ms = (time.time() - t_build) * 1000.0
        
        # Stage 5: Generation via Gemini 2.5 Flash
        t_gen = time.time()
        if is_upload_mode:
            system_instruction = (
                "You are an expert AI Research Assistant operating in STRICT UPLOADED_DOCUMENT_CONTEXT mode.\n"
                "All answers must be grounded exclusively in the selected uploaded document(s).\n"
                "MANDATORY OPERATIONAL CONSTRAINTS:\n"
                "1. Base your answer ONLY on the facts present in the provided CITATION evidence from the uploaded document.\n"
                "2. PROHIBITED: Do NOT introduce outside facts, global scientific corpus knowledge, or general knowledge as evidence.\n"
                "3. Cite document evidence using bracketed citation markers like [1], [2] matching the provided evidence.\n"
                "4. When the user asks for a summary:\n"
                "   - Use the uploaded document as the sole source.\n"
                "   - Summarize only information actually present in the document.\n"
                "   - Do not introduce outside facts.\n"
                "   - Preserve uncertainty when the paper is uncertain.\n"
                "   - Cite page/section evidence where possible.\n"
                "5. EXACT FALLBACK RULES:\n"
                "   - If no relevant content was found in the uploaded evidence, return exactly:\n"
                "     \"No matching content was found in the uploaded paper.\"\n"
                "   - If related evidence exists in the document but is insufficient to answer confidently, return exactly:\n"
                "     \"The selected paper does not contain sufficient evidence to answer this question confidently.\"\n"
            )
        else:
            system_instruction = (
                "You are an expert AI Research Assistant. Answer the user question based STRICTLY on the provided evidence context.\n"
                "MANDATORY RULES:\n"
                "1. Base every claim on the cited evidence.\n"
                "2. Use explicit numeric citation markers like [1], [2] matching the provided evidence.\n"
                "3. If evidence is lacking or insufficient, clearly state that evidence is insufficient.\n"
                "4. Structure your response into clear sections: Answer, Key Findings, Research Implications.\n"
            )
        
        generation_result = await LLMProviderManager.generate(query, context_text, system_instruction=system_instruction)
        raw_answer = generation_result.get("text", "")
        generation_status = generation_result.get("generation_status", "success")
        generation_ms = (time.time() - t_gen) * 1000.0
        
        # Stage 6: Claim-Level Verification & Grounding (Phase 3.4)
        from app.services.assistant.claim_verifier import ClaimVerifier
        citation_str_map = {f"[{k}]": v for k, v in citation_map.items()}
        
        claims_objects, verifier_audits, verification_metrics = await ClaimVerifier.verify_claims(
            raw_answer=raw_answer,
            citation_mapping=citation_str_map,
            available_evidence=deduplicated_evidence,
            scope=resolved_context.scope
        )

        cited_numbers = [int(n) for n in re.findall(r'\[(\d+)\]', raw_answer)]
        valid_citations = []
        invalid_citations = []
        
        for cnum in set(cited_numbers):
            if cnum in citation_map:
                valid_citations.append(cnum)
            else:
                invalid_citations.append(cnum)

        # Build Enriched Canonical Citations Output
        canonical_citations_output = []
        for idx, ev in enumerate(deduplicated_evidence, 1):
            citation_id = f"[{idx}]"
            title = ev.get("title", "Unknown Title")
            authors = ev.get("authors", "Unknown Authors")
            source_type = ev.get("source_type", ev.get("retrieval_source", "local"))
            is_cited = idx in valid_citations
            matching_claim_ids = [c.claim_id for c in claims_objects if citation_id in c.citation_ids]

            canonical_citations_output.append({
                "citation_id": citation_id,
                "citation_number": idx,
                "claim_ids": matching_claim_ids,
                "claim_id": matching_claim_ids[0] if matching_claim_ids else None,
                "evidence_id": ev.get("chunk_id", ev.get("id")),
                "paper_id": ev.get("paper_id", ev.get("id")),
                "source_id": ev.get("id"),
                "source_type": source_type,
                "title": title,
                "authors": authors,
                "url": ev.get("url", ""),
                "provenance": source_type.upper(),
                "is_actually_cited": is_cited,
                "evidence_text": ev.get("evidence_text", ev.get("abstract", ""))
            })
                
        total_ms = (time.time() - pipeline_start) * 1000.0
        
        # Build Evidence Manifest & Audit Records
        source_counts = {"local": 0, "online": 0, "uploaded": 0}
        for ev in deduplicated_evidence:
            stype = ev.get("source_type", ev.get("retrieval_source", "local"))
            source_counts[stype] = source_counts.get(stype, 0) + 1

        # Separate Grounded Sources vs Actually Cited Sources
        grounded_sources = [
            {
                "id": ev.get("id"),
                "paper_id": ev.get("paper_id", ev.get("id")),
                "title": ev.get("title"),
                "authors": ev.get("authors"),
                "source": ev.get("source_type", "local"),
                "source_type": ev.get("source_type", "local"),
                "evidence_status": ev.get("evidence_status", "evidence_ready")
            } for ev in deduplicated_evidence
        ]

        cited_evidence_indices = set(valid_citations)
        cited_sources = [
            grounded_sources[i-1] for i in sorted(cited_evidence_indices) if 0 <= i-1 < len(grounded_sources)
        ]

        import uuid
        answer_id = f"ans_{uuid.uuid4().hex[:12]}"
        execution_id = f"exec_{resolved_context.search_id or session_id}"

        evidence_manifest = {
            "question": query,
            "answer_id": answer_id,
            "execution_id": execution_id,
            "context_snapshot_id": resolved_context.context_snapshot_id,
            "context_hash": resolved_context.context_hash,
            "scope": resolved_context.scope,
            "mode": resolved_context.mode,
            "retrieved_candidates": len(retrieved_evidence),
            "selected_evidence_count": len(deduplicated_evidence),
            "grounded_sources_count": len(grounded_sources),
            "cited_sources_count": len(cited_sources),
            "source_distribution": source_counts,
            "citation_mapping": {f"[{k}]": v.get("chunk_id", v.get("id")) for k, v in citation_map.items()},
            "structural_citation_validation": {
                "cited_ids": cited_numbers,
                "valid_citations": valid_citations,
                "invalid_citations": invalid_citations,
                "citation_integrity": len(invalid_citations) == 0
            },
            "verification_metrics": verification_metrics,
            "verifier_audit_records": [audit.dict() for audit in verifier_audits],
            "generation_model": generation_result.get("model", "gemini-2.5-flash"),
            "generation_latency_ms": round(generation_ms, 2)
        }
        
        return {
            "answer": raw_answer,
            "answer_id": answer_id,
            "execution_id": execution_id,
            "search_id": resolved_context.search_id,
            "session_id": session_id,
            "generation_status": generation_status,
            "claims": [c.dict() for c in claims_objects],
            "citations": canonical_citations_output,
            "evidence": deduplicated_evidence,
            "sources": grounded_sources,
            "grounded_sources": grounded_sources,
            "cited_sources": cited_sources,
            "grounded_sources_count": len(grounded_sources),
            "cited_sources_count": len(cited_sources),
            "context_snapshot_id": resolved_context.context_snapshot_id,
            "context_hash": resolved_context.context_hash,
            "evidence_manifest": evidence_manifest,
            "verification_metrics": verification_metrics,
            "metadata": {
                "answer_id": answer_id,
                "execution_id": execution_id,
                "search_id": resolved_context.search_id,
                "context_resolution_ms": 0.0,
                "retrieval_ms": round(retrieval_ms, 2),
                "evidence_selection_ms": round(evidence_selection_ms, 2),
                "context_build_ms": round(context_build_ms, 2),
                "generation_ms": round(generation_ms, 2),
                "claim_extraction_ms": verification_metrics.get("claim_extraction_ms", 0.0),
                "verification_ms": verification_metrics.get("verification_ms", 0.0),
                "total_ms": round(total_ms, 2)
            }
        }
