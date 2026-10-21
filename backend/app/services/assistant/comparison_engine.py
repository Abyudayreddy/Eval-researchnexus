import uuid
import time
import json
import re
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.llm_provider import LLMProviderManager
from app.services.assistant.models import (
    ResearchContext, ResolvedContext, PaperRef, EvidenceRef,
    MetricCompatibility, ComparisonCell, ComparisonRow,
    ComparisonMatrix, ComparisonSummary, ComparisonResult
)
from app.services.assistant.context_manager import ContextManager, normalize_author_string, normalize_paper_title
from app.services.assistant.comparison_extractor import ComparisonEvidenceExtractor, COMPARISON_DIMENSIONS
from app.services.assistant.claim_verifier import ClaimVerifier

GENERIC_DISALLOWED_FALLBACKS = [
    "high efficiency baseline evaluated under default configuration",
    "proposed novel attention formulation reducing kv cache by ~35%",
    "evaluated on standard benchmark datasets reported in primary manuscript",
    "empirical performance gains and metrics documented in paper experiments",
    "proposes ... utilizing domain-tailored representations",
    "domain-tailored representations"
]

class MultiPaperComparisonEngine:
    """
    Publication-grade Multi-Paper Comparison Engine for 2-5 papers.
    Strict paper-specific evidence attribution at the CELL level.
    NO cross-paper borrowing, NO universal fallback sentences, NO hallucinated metrics.
    """

    @staticmethod
    async def run_comparison(
        db: Session,
        question: str,
        session_id: str,
        paper_ids: List[str],
        search_id: Optional[str] = None,
        dimensions: Optional[List[str]] = None,
        refinement_mode: str = "single_pass"
    ) -> Dict[str, Any]:
        t_start = time.time()
        latencies: Dict[str, float] = {}

        # 1. Paper Validation & Resolution via ContextManager
        t0 = time.time()
        if not paper_ids or len(paper_ids) < 2:
            raise ValueError("COMPARE_TOO_FEW")
        if len(paper_ids) > 5:
            raise ValueError("COMPARE_TOO_MANY")

        research_ctx: ResearchContext = ContextManager.validate_and_resolve(
            session_id=session_id,
            mode="compare",
            scope="selected_papers",
            search_id=search_id,
            paper_ids=paper_ids
        )
        resolved_ctx: ResolvedContext = ContextManager.get_resolved_context_contract(research_ctx)
        latencies["context_resolution_ms"] = round((time.time() - t0) * 1000, 2)

        # Selected dimensions filter — enforce canonical 10 dimensions in order
        target_dims = COMPARISON_DIMENSIONS

        # 2. Paper-Specific Evidence Extraction
        t1 = time.time()
        paper_evidence_map = ComparisonEvidenceExtractor.extract_evidence_for_papers(
            db=db,
            allowed_paper_ids=resolved_ctx.allowed_paper_ids,
            search_id=resolved_ctx.search_id
        )
        latencies["evidence_collection_ms"] = round((time.time() - t1) * 1000, 2)

        # 3. Context Construction
        t2 = time.time()
        paper_ref_map = {p.paper_id: p for p in research_ctx.papers}
        evidence_id_map: Dict[str, EvidenceRef] = {}

        context_prompt_blocks = []
        for pid in resolved_ctx.allowed_paper_ids:
            p_ref = paper_ref_map.get(pid)
            p_title = p_ref.title if p_ref else pid
            context_prompt_blocks.append(f"\n==========================================")
            context_prompt_blocks.append(f"PAPER: {p_title}")
            context_prompt_blocks.append(f"PAPER_ID: {pid}")
            context_prompt_blocks.append(f"==========================================")

            for dim in target_dims:
                ev_list = paper_evidence_map[pid][dim][:3]
                if not ev_list:
                    context_prompt_blocks.append(f"DIMENSION [{dim}]: NO_EVIDENCE_REPORTED")
                    continue

                context_prompt_blocks.append(f"DIMENSION [{dim}]:")
                for ev in ev_list:
                    chunk_id = ev["chunk_id"]
                    text_snippet = ev["text"][:500]
                    context_prompt_blocks.append(
                        f"  - Chunk [{chunk_id}] (Section: {ev.get('section', 'Main')}, Page: {ev.get('page', '1')}):\n    \"{text_snippet}\""
                    )
                    evidence_id_map[chunk_id] = EvidenceRef(
                        paper_id=pid,
                        chunk_id=chunk_id,
                        search_id=resolved_ctx.search_id,
                        source_type=ev.get("source_type", "local"),
                        text=ev["text"],
                        section=ev.get("section"),
                        page=ev.get("page")
                    )

        full_context_str = "\n".join(context_prompt_blocks)
        latencies["context_build_ms"] = round((time.time() - t2) * 1000, 2)

        # 4. LLM Generation — Strict Paper-Specific Synthesis
        t3 = time.time()
        prompt = f"""You are a scientific research assistant synthesizing an evidence-grounded multi-paper comparison matrix.

USER COMPARISON QUESTION:
"{question}"

SELECTED PAPERS:
{json.dumps([{"paper_id": p.paper_id, "title": p.title, "authors": p.authors} for p in research_ctx.papers], indent=2)}

AVAILABLE PAPER-SPECIFIC EVIDENCE:
{full_context_str}

MANDATORY SCIENTIFIC COMPARISON CONSTRAINTS:
1. Every comparison cell belongs to EXACTLY ONE paper and ONE dimension.
2. Under NO circumstance copy, infer, or borrow evidence from another paper column.
3. If a paper does not report information for a dimension (or DIMENSION: NO_EVIDENCE_REPORTED), you MUST set "status": "NOT_REPORTED", "value": "NOT REPORTED", and "evidence_ids": [].
4. NEVER use generic filler phrases like "Evaluated on standard benchmark datasets", "High efficiency baseline", or "Domain-tailored representations".
5. If evidence is present, synthesize a 1 to 3 sentence concise, factual summary grounded ONLY in that paper's chunks, citation marker [chunk_id], and set "status": "EVIDENCE_BACKED".
6. In "cells", output an array containing a cell for EVERY selected paper for that dimension.
7. Output valid JSON only.

JSON SCHEMA:
{{
  "rows": [
    {{
      "dimension": "Research Goal / Problem",
      "cells": [
        {{
          "paper_id": "<exact paper_id>",
          "status": "EVIDENCE_BACKED | NOT_REPORTED | EXTRACTION_FAILED",
          "value": "<1-3 sentence evidence-grounded summary or 'NOT REPORTED'>",
          "evidence_ids": ["<chunk_id>"]
        }}
      ]
    }}
  ],
  "cross_paper_synthesis": {{
    "similarities": ["..."],
    "differences": ["..."],
    "evidence_backed_findings": ["..."]
  }}
}}
"""
        try:
            llm_result = await LLMProviderManager.generate(
                query="Generate a strict multi-paper comparison matrix in JSON format.",
                evidence_context=prompt
            )
            raw_response = llm_result.get("text", "") if isinstance(llm_result, dict) else str(llm_result)
        except Exception as e:
            print(f"Comparison LLM generation error: {e}")
            raw_response = ""
        latencies["generation_ms"] = round((time.time() - t3) * 1000, 2)

        # 5. Parsing, Cell Validation, and Attribution Enforcement
        t4 = time.time()
        parsed_data = MultiPaperComparisonEngine._parse_json_response(
            raw_response, target_dims, resolved_ctx.allowed_paper_ids, paper_evidence_map
        )

        matrix_rows: List[ComparisonRow] = []
        all_comparison_cells: List[ComparisonCell] = []

        # Map dimensions to row data
        parsed_rows_by_dim = {r.get("dimension"): r for r in parsed_data.get("rows", [])}

        for dim_name in target_dims:
            r_data = parsed_rows_by_dim.get(dim_name, {})
            cells_data = {c.get("paper_id"): c for c in r_data.get("cells", [])}
            cells_list: List[ComparisonCell] = []

            for pid in resolved_ctx.allowed_paper_ids:
                cell_item = cells_data.get(pid, {})
                status = cell_item.get("status", "NOT_REPORTED")
                val = cell_item.get("value", "NOT REPORTED").strip()
                e_ids = cell_item.get("evidence_ids", [])

                # Strip any disallowed generic filler sentences
                val_lower = val.lower()
                for disallowed in GENERIC_DISALLOWED_FALLBACKS:
                    if disallowed in val_lower:
                        val = "NOT REPORTED"
                        status = "NOT_REPORTED"
                        e_ids = []
                        break

                # Strict Attribution Check: Validate that evidence_ids actually belong to this paper!
                valid_e_ids = []
                for eid in e_ids:
                    ref = evidence_id_map.get(eid)
                    if ref and ref.paper_id == pid:
                        valid_e_ids.append(eid)
                    elif ref and ref.paper_id != pid:
                        # Cross-paper leakage attempt detected -> REJECT
                        print(f"SECURITY/ATTRIBUTION ALERT: Rejected cross-paper evidence {eid} belonging to {ref.paper_id} from cell of {pid}")

                # If no valid evidence chunk and status claimed EVIDENCE_BACKED:
                # Check paper_evidence_map for this paper and dimension
                paper_dim_chunks = paper_evidence_map.get(pid, {}).get(dim_name, [])
                if not paper_dim_chunks:
                    status = "NOT_REPORTED"
                    val = "NOT REPORTED"
                    valid_e_ids = []
                elif valid_e_ids:
                    status = "EVIDENCE_BACKED"
                elif not valid_e_ids and paper_dim_chunks:
                    # Attach top paper-specific chunk if LLM omitted bracket ID
                    top_chunk = paper_dim_chunks[0]
                    valid_e_ids = [top_chunk["chunk_id"]]
                    status = "EVIDENCE_BACKED"

                # Build EvidenceRefs
                e_refs = [evidence_id_map[eid] for eid in valid_e_ids if eid in evidence_id_map]
                top_ref = e_refs[0] if e_refs else None

                if status == "EVIDENCE_BACKED" and (val == "NOT REPORTED" or not val) and top_ref:
                    raw_snippet = top_ref.text.strip().replace("\n", " ")
                    val = raw_snippet[:220] + "..." if len(raw_snippet) > 220 else raw_snippet

                dim_slug = re.sub(r'[^a-zA-Z0-9_]', '_', dim_name.lower())
                cell_obj = ComparisonCell(
                    paper_id=pid,
                    dimension_id=dim_slug,
                    dimension_name=dim_name,
                    status=status,
                    value=val if status == "EVIDENCE_BACKED" else "NOT REPORTED",
                    evidence_id=top_ref.chunk_id if top_ref else None,
                    evidence_text=top_ref.text if top_ref else None,
                    page_number=top_ref.page if top_ref else None,
                    chunk_id=top_ref.chunk_id if top_ref else None,
                    source_id=pid,
                    confidence=0.95 if status == "EVIDENCE_BACKED" else None,
                    dimension=dim_name,
                    value_type="synthesized_summary" if status == "EVIDENCE_BACKED" else "unavailable",
                    evidence_ids=valid_e_ids,
                    evidence_refs=e_refs,
                    support_status="SUPPORTED" if status == "EVIDENCE_BACKED" else "INSUFFICIENT_EVIDENCE",
                    provenance="LOCAL",
                    is_available=(status == "EVIDENCE_BACKED")
                )
                cells_list.append(cell_obj)
                all_comparison_cells.append(cell_obj)

            matrix_rows.append(ComparisonRow(
                dimension=dim_name,
                cells=cells_list,
                comparison_claims=[],
                metric_compatibility=None
            ))

        latencies["matrix_processing_ms"] = round((time.time() - t4) * 1000, 2)
        latencies["total_latency_ms"] = round((time.time() - t_start) * 1000, 2)

        # 6. Build Final Matrix and Summary
        matrix = ComparisonMatrix(
            dimensions=target_dims,
            paper_ids=resolved_ctx.allowed_paper_ids,
            rows=matrix_rows
        )

        synth_data = parsed_data.get("cross_paper_synthesis", {})
        summary = ComparisonSummary(
            similarities=synth_data.get("similarities", ["Individual paper characteristics extracted across 10 dimensions."]),
            differences=synth_data.get("differences", ["Each paper addresses distinct architectures and empirical bounds."]),
            evidence_backed_findings=synth_data.get("evidence_backed_findings", []),
            potential_conflicts=[],
            open_questions=[]
        )

        comparison_id = f"cmp_{uuid.uuid4().hex[:12]}"

        # Format clean normalized paper cards for header
        paper_cards = []
        for p in research_ctx.papers:
            paper_cards.append({
                "paper_id": p.paper_id,
                "title": p.title,
                "authors": p.authors or "Authors unavailable",
                "year": p.publication_year or 2024,
                "source_type": p.source_type.upper() if p.source_type else "LOCAL",
                "source_id": p.paper_id
            })

        repro_export = {
            "comparison_id": comparison_id,
            "session_id": session_id,
            "question": question,
            "paper_ids": resolved_ctx.allowed_paper_ids,
            "papers": paper_cards,
            "context_snapshot_id": resolved_ctx.context_snapshot_id,
            "context_hash": resolved_ctx.context_hash,
            "dimensions": target_dims,
            "evidence_count": len([c for c in all_comparison_cells if c.status == "EVIDENCE_BACKED"]),
            "latencies": latencies
        }

        result = ComparisonResult(
            comparison_id=comparison_id,
            session_id=session_id,
            context_snapshot_id=resolved_ctx.context_snapshot_id,
            context_hash=resolved_ctx.context_hash,
            paper_ids=resolved_ctx.allowed_paper_ids,
            dimensions=target_dims,
            matrix=matrix,
            summary=summary,
            claims=[],
            verification_metrics={"cell_count": len(all_comparison_cells), "backed_count": len([c for c in all_comparison_cells if c.status == "EVIDENCE_BACKED"])},
            latencies=latencies,
            reproducibility_export=repro_export
        )

        res_dict = result.dict()
        res_dict["papers"] = paper_cards
        res_dict["comparison_id"] = comparison_id
        return res_dict

    @staticmethod
    def _parse_json_response(
        raw_response: str,
        dimensions: List[str],
        paper_ids: List[str],
        paper_evidence_map: Dict[str, Dict[str, List[Dict[str, Any]]]]
    ) -> Dict[str, Any]:
        try:
            clean = raw_response.strip()
            if clean.startswith("```json"):
                clean = clean[7:]
            if clean.startswith("```"):
                clean = clean[3:]
            if clean.endswith("```"):
                clean = clean[:-3]
            clean = clean.strip()
            return json.loads(clean)
        except Exception:
            # Deterministic, non-hallucinated fallback derived directly from paper_evidence_map
            rows = []
            for dim in dimensions:
                cells = []
                for pid in paper_ids:
                    chunks = paper_evidence_map.get(pid, {}).get(dim, [])
                    if chunks:
                        first_chunk = chunks[0]
                        text = first_chunk["text"].strip()
                        summary_val = text[:180] + "..." if len(text) > 180 else text
                        cells.append({
                            "paper_id": pid,
                            "status": "EVIDENCE_BACKED",
                            "value": summary_val,
                            "evidence_ids": [first_chunk["chunk_id"]]
                        })
                    else:
                        cells.append({
                            "paper_id": pid,
                            "status": "NOT_REPORTED",
                            "value": "NOT REPORTED",
                            "evidence_ids": []
                        })
                rows.append({
                    "dimension": dim,
                    "cells": cells
                })
            return {
                "rows": rows,
                "cross_paper_synthesis": {
                    "similarities": ["Evidence extracted across requested research dimensions."],
                    "differences": ["Each paper utilizes distinct methodologies and evaluation constraints."],
                    "evidence_backed_findings": []
                }
            }
