import sys
import os
import pytest
import asyncio

# Add backend root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.services.assistant.models import ResolvedContext
from app.services.assistant.eligibility import ContextEligibilityEngine
from app.services.assistant.self_feedback import SelfFeedbackEngine, ClaimObject
from app.services.assistant.refinement_query import RefinementQueryGenerator
from app.services.assistant.iterative_rag import IterativeRAGService

def test_self_feedback_supported_claim():
    claim = ClaimObject(
        claim_id="claim_01",
        text="Method X achieves 85% accuracy.",
        claim_type="numerical",
        citation_ids=["[1]"],
        evidence_ids=["c1"],
        claim_support_status="SUPPORTED"
    )
    fb = SelfFeedbackEngine.evaluate("What is Method X accuracy?", [claim], [], {"supported_claim_count": 1})
    assert fb.needs_refinement is False
    assert fb.feedback_category == "NO_REFINEMENT_NEEDED"

def test_self_feedback_unsupported_claim():
    claim = ClaimObject(
        claim_id="claim_01",
        text="Method X achieves 95% accuracy.",
        claim_type="numerical",
        citation_ids=["[1]"],
        evidence_ids=["c1"],
        claim_support_status="UNSUPPORTED",
        verification_reason="Numeric mismatch"
    )
    fb = SelfFeedbackEngine.evaluate("What is Method X accuracy?", [claim], [], {"unsupported_claim_count": 1})
    assert fb.needs_refinement is True
    assert fb.feedback_category == "UNSUPPORTED_CLAIM"
    assert "claim_01" in fb.unsupported_claim_ids

def test_current_evidence_zero_retinement_queries():
    ctx = ResolvedContext(
        allowed_paper_ids=["p1"],
        allowed_evidence_ids=["c1"],
        allowed_document_ids=[],
        allowed_source_types=["local"],
        mode="evidence",
        scope="current_evidence",
        context_snapshot_id="snap-101",
        context_hash="hash-101"
    )
    eligibility = ContextEligibilityEngine.evaluate(ctx)
    queries = RefinementQueryGenerator.generate_queries("What is Method X accuracy?", ["Method X achieves 95% accuracy"], eligibility)
    assert len(queries) == 0

def test_single_pass_no_refinement_cycles():
    async def _run():
        ctx = ResolvedContext(
            allowed_paper_ids=["non-existent"],
            allowed_evidence_ids=[],
            allowed_document_ids=[],
            allowed_source_types=["local"],
            mode="paper",
            scope="single_paper",
            context_snapshot_id="snap-202",
            context_hash="hash-202"
        )
        res = await IterativeRAGService.run_pipeline(
            query="What is the learning rate?",
            resolved_context=ctx,
            session_id="session-single-pass",
            refinement_mode="single_pass"
        )
        assert res["refinement_manifest"]["iteration_count"] == 0
        assert res["refinement_manifest"]["refinement_mode"] == "single_pass"
        assert res["context_snapshot_id"] == "snap-202"
        assert res["context_hash"] == "hash-202"

    asyncio.run(_run())

def test_iterative_pipeline_snapshot_immutability():
    async def _run():
        ctx = ResolvedContext(
            allowed_paper_ids=["non-existent"],
            allowed_evidence_ids=[],
            allowed_document_ids=[],
            allowed_source_types=["local"],
            mode="paper",
            scope="single_paper",
            context_snapshot_id="snap-303",
            context_hash="hash-303"
        )
        res = await IterativeRAGService.run_pipeline(
            query="What is the learning rate?",
            resolved_context=ctx,
            session_id="session-auto",
            refinement_mode="automatic"
        )
        # Snapshot and hash MUST remain immutable
        assert res["context_snapshot_id"] == "snap-303"
        assert res["context_hash"] == "hash-303"
        assert res["refinement_manifest"]["max_iterations_limit"] == 2

    asyncio.run(_run())

if __name__ == "__main__":
    pytest.main(["-v", __file__])
