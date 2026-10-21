import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from app.services.assistant.models import ResolvedContext
from app.services.assistant.eligibility import ContextEligibilityEngine
from app.services.assistant.enhanced_rag import EnhancedRAGService
from app.services.assistant.self_feedback import SelfFeedbackEngine, SelfFeedbackResult
from app.services.assistant.refinement_query import RefinementQueryGenerator
from app.services.assistant.claim_verifier import ClaimVerifier
from app.services.local_evidence import get_local_retriever
from app.services.llm_provider import LLMProviderManager

class AnswerVersion(BaseModel):
    version: int  # 0 = initial, 1 = refinement 1, 2 = refinement 2
    answer: str
    claims: List[Dict[str, Any]]
    citations: List[Dict[str, Any]]
    evidence_ids: List[str]
    verification_metrics: Dict[str, Any]

class IterativeRAGService:
    MAX_REFINEMENT_CYCLES = 2  # Hard stop after 2 refinement cycles after initial generation

    @staticmethod
    async def run_pipeline(
        query: str,
        resolved_context: ResolvedContext,
        session_id: str,
        search_mode: str = "hybrid",
        refinement_mode: str = "automatic"  # automatic | single_pass
    ) -> Dict[str, Any]:
        pipeline_start = time.time()
        model_calls = 0

        # Stage 1: Initial Generation (Gen 0 / v1)
        model_calls += 1
        initial_response = await EnhancedRAGService.generate_response(
            query=query,
            resolved_context=resolved_context,
            session_id=session_id,
            search_mode=search_mode
        )

        v1 = AnswerVersion(
            version=0,
            answer=initial_response["answer"],
            claims=initial_response.get("claims", []),
            citations=initial_response.get("citations", []),
            evidence_ids=[ev.get("chunk_id", ev.get("id")) for ev in initial_response.get("evidence", [])],
            verification_metrics=initial_response.get("verification_metrics", {})
        )

        answer_versions = [v1]
        current_response = initial_response
        current_evidence = list(initial_response.get("evidence", []))
        seen_feedback_signatures = set()

        refinement_history = []
        iteration_count = 0

        # Eligibility check
        eligibility = ContextEligibilityEngine.evaluate(resolved_context)

        # Iteration Loop (At most 2 refinement cycles)
        while iteration_count < IterativeRAGService.MAX_REFINEMENT_CYCLES:
            if refinement_mode == "single_pass" or not eligibility.should_retrieve:
                break

            claims_objs = current_response.get("claims", [])

            # Run Self-Feedback
            t_fb = time.time()
            feedback: SelfFeedbackResult = SelfFeedbackEngine.evaluate(
                question=query,
                claims=[type('Claim', (), c)() for c in claims_objs] if False else [],  # evaluate uses dictionary matching
                available_evidence=current_evidence,
                verification_metrics=current_response.get("verification_metrics", {})
            )
            feedback_ms = (time.time() - t_fb) * 1000.0
            model_calls += 1

            if not feedback.needs_refinement:
                break

            # Anti-oscillation check: stop if identical feedback occurs again
            if feedback.feedback_signature in seen_feedback_signatures:
                break
            seen_feedback_signatures.add(feedback.feedback_signature)

            # Generate targeted queries
            refinement_queries = RefinementQueryGenerator.generate_queries(
                original_query=query,
                suggested_focus=feedback.suggested_focus,
                eligibility=eligibility
            )

            # Targeted Evidence Retrieval within ResolvedContext boundaries
            new_evidence = []
            if eligibility.can_use_local and refinement_queries:
                local_retriever = get_local_retriever()
                if local_retriever.init_status == "ready":
                    allowed_pids = eligibility.allowed_paper_ids if eligibility.allowed_paper_ids else None
                    for rq in refinement_queries:
                        ev_list, is_suff, trace = local_retriever.retrieve(
                            query=rq,
                            top_k_evidence=3,
                            deep_evidence=True,
                            allowed_paper_ids=allowed_pids
                        )
                        new_evidence.extend(ev_list)

            # Merge evidence with deduplication (source_type, paper_id, chunk_id)
            seen_identities = set([ (ev.get("source_type", "local"), ev.get("paper_id", ev.get("id")), ev.get("chunk_id", ev.get("id"))) for ev in current_evidence ])
            added_evidence = []
            for ev in new_evidence:
                stype = ev.get("source_type", ev.get("retrieval_source", "local"))
                pid = ev.get("paper_id", ev.get("id"))
                cid = ev.get("chunk_id", pid)
                ident = (stype, pid, cid)
                if ident not in seen_identities:
                    seen_identities.add(ident)
                    added_evidence.append(ev)
                    current_evidence.append(ev)

            # Stop iteration if no useful new evidence was found
            if not added_evidence:
                break

            iteration_count += 1

            # Build refined context text
            context_text = ""
            citation_map = {}
            citations_output = []
            for idx, ev in enumerate(current_evidence, 1):
                cid_str = f"[{idx}]"
                ev_text = ev.get("evidence_text", ev.get("resolved_evidence_text", ev.get("abstract", "")))
                title = ev.get("title", "Unknown Title")
                authors = ev.get("authors", "Unknown Authors")
                stype = ev.get("source_type", ev.get("retrieval_source", "local"))
                context_text += f"CITATION {cid_str}:\nSource: {stype}\nPaper: {title}\nAuthors: {authors}\nEvidence: {ev_text}\n\n"
                citation_map[idx] = ev
                citations_output.append({
                    "citation_id": cid_str,
                    "numeric_id": idx,
                    "paper_id": ev.get("paper_id", ev.get("id")),
                    "chunk_id": ev.get("chunk_id"),
                    "title": title,
                    "source_type": stype
                })

            # Refined generation via Gemini 2.5 Flash
            model_calls += 1
            is_upload = resolved_context.scope in ["uploaded_documents", "UPLOADED_DOCUMENTS"]
            if is_upload:
                refine_prompt = (
                    "You are an expert AI Research Assistant operating in STRICT UPLOADED_DOCUMENT_CONTEXT mode.\n"
                    "All answers must be grounded exclusively in the selected uploaded document(s).\n"
                    "MANDATORY OPERATIONAL CONSTRAINTS:\n"
                    "1. Base your answer ONLY on the facts present in the provided CITATION evidence from the uploaded document.\n"
                    "2. PROHIBITED: Do NOT introduce outside facts, global scientific corpus knowledge, or general knowledge as evidence.\n"
                    "3. Cite document evidence using bracketed citation markers like [1], [2].\n"
                    "4. If no relevant content or insufficient evidence, return the exact required fallback phrase.\n"
                )
            else:
                refine_prompt = (
                    "You are an expert AI Research Assistant. Produce a revised research answer using the supplied evidence context.\n"
                    "MANDATORY RULES:\n"
                    "1. Correct unsupported claims from initial answer.\n"
                    "2. Base every claim on the cited evidence.\n"
                    "3. Use explicit numeric citation markers like [1], [2].\n"
                    "4. Preserve valid conclusions from the initial answer.\n"
                )
            gen_res = await LLMProviderManager.generate(query, context_text, system_instruction=refine_prompt)
            refined_answer = gen_res.get("text", "")

            # Re-verification Pass via Phase 3.4 ClaimVerifier
            model_calls += 1
            citation_str_map = {f"[{k}]": v for k, v in citation_map.items()}
            claims_objs, verifier_audits, verification_metrics = await ClaimVerifier.verify_claims(
                raw_answer=refined_answer,
                citation_mapping=citation_str_map,
                available_evidence=current_evidence,
                scope=resolved_context.scope
            )

            # Record Version
            vn = AnswerVersion(
                version=iteration_count,
                answer=refined_answer,
                claims=[c.dict() for c in claims_objs],
                citations=citations_output,
                evidence_ids=[ev.get("chunk_id", ev.get("id")) for ev in current_evidence],
                verification_metrics=verification_metrics
            )
            answer_versions.append(vn)

            refinement_history.append({
                "iteration": iteration_count,
                "feedback_category": feedback.feedback_category,
                "refinement_queries": refinement_queries,
                "added_evidence_count": len(added_evidence),
                "verification_metrics": verification_metrics
            })

            # Update current_response object
            current_response = {
                "answer": refined_answer,
                "generation_status": gen_res.get("generation_status", "success"),
                "claims": [c.dict() for c in claims_objs],
                "citations": citations_output,
                "evidence": current_evidence,
                "verification_metrics": verification_metrics,
                "verifier_audits": [a.dict() for a in verifier_audits]
            }

        total_pipeline_ms = (time.time() - pipeline_start) * 1000.0

        # Calculate Quality & Latency Deltas
        v1_metrics = v1.verification_metrics
        vn_metrics = current_response.get("verification_metrics", v1_metrics)

        quality_delta = {
            "supported_claim_delta": vn_metrics.get("supported_claim_count", 0) - v1_metrics.get("supported_claim_count", 0),
            "unsupported_claim_delta": vn_metrics.get("unsupported_claim_count", 0) - v1_metrics.get("unsupported_claim_count", 0),
            "citation_precision_delta": round(vn_metrics.get("citation_precision", 0.0) - v1_metrics.get("citation_precision", 0.0), 4),
            "claim_support_rate_delta": round(vn_metrics.get("claim_support_rate", 0.0) - v1_metrics.get("claim_support_rate", 0.0), 4)
        }

        # Build Refinement Manifest
        refinement_manifest = {
            "refinement_enabled": refinement_mode == "automatic",
            "refinement_mode": refinement_mode,
            "iteration_count": iteration_count,
            "max_iterations_limit": IterativeRAGService.MAX_REFINEMENT_CYCLES,
            "total_model_calls": model_calls,
            "answer_versions_count": len(answer_versions),
            "refinement_history": refinement_history,
            "quality_delta": quality_delta,
            "context_snapshot_id": resolved_context.context_snapshot_id,
            "context_hash": resolved_context.context_hash
        }

        return {
            "answer": current_response["answer"],
            "generation_status": current_response.get("generation_status", "success"),
            "claims": current_response.get("claims", []),
            "citations": current_response.get("citations", []),
            "evidence": current_evidence,
            "sources": [
                {
                    "id": ev.get("id"),
                    "title": ev.get("title"),
                    "authors": ev.get("authors"),
                    "source": ev.get("source_type", "local"),
                    "evidence_status": ev.get("evidence_status", "evidence_ready")
                } for ev in current_evidence
            ],
            "context_snapshot_id": resolved_context.context_snapshot_id,
            "context_hash": resolved_context.context_hash,
            "search_id": resolved_context.search_id,
            "session_id": session_id,
            "answer_versions": [v.dict() for v in answer_versions],
            "refinement_manifest": refinement_manifest,
            "verification_metrics": current_response.get("verification_metrics", {}),
            "metadata": {
                "iteration_count": iteration_count,
                "total_model_calls": model_calls,
                "total_ms": round(total_pipeline_ms, 2)
            }
        }
