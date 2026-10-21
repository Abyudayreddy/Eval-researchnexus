import sys
import os
import pytest
import asyncio

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.services.assistant.models import ResolvedContext
from app.services.assistant.eligibility import ContextEligibilityEngine
from app.services.assistant.enhanced_rag import EnhancedRAGService

def test_current_evidence_zero_retrieval_eligibility():
    ctx = ResolvedContext(
        allowed_paper_ids=["paper-1"],
        allowed_evidence_ids=["chunk-1"],
        allowed_document_ids=[],
        allowed_source_types=["local"],
        mode="evidence",
        scope="current_evidence",
        context_snapshot_id="snap-123",
        context_hash="hash-123"
    )
    eligibility = ContextEligibilityEngine.evaluate(ctx)
    assert eligibility.should_retrieve is False
    assert eligibility.can_use_local is False
    assert eligibility.can_use_online is False
    assert eligibility.allowed_evidence_ids == ["chunk-1"]

def test_single_paper_eligibility():
    ctx = ResolvedContext(
        allowed_paper_ids=["paper-123"],
        allowed_evidence_ids=[],
        allowed_document_ids=[],
        allowed_source_types=["local"],
        mode="paper",
        scope="single_paper",
        context_snapshot_id="snap-456",
        context_hash="hash-456"
    )
    eligibility = ContextEligibilityEngine.evaluate(ctx)
    assert eligibility.should_retrieve is True
    assert eligibility.can_use_local is True
    assert eligibility.can_use_online is False
    assert eligibility.allowed_paper_ids == ["paper-123"]

def test_enhanced_rag_insufficient_evidence():
    async def _run():
        ctx = ResolvedContext(
            allowed_paper_ids=["non-existent-paper"],
            allowed_evidence_ids=[],
            allowed_document_ids=[],
            allowed_source_types=["local"],
            mode="paper",
            scope="single_paper",
            context_snapshot_id="snap-789",
            context_hash="hash-789"
        )
        res = await EnhancedRAGService.generate_response(
            query="What is the learning rate?",
            resolved_context=ctx,
            session_id="test-session"
        )
        assert res["generation_status"] == "insufficient_evidence"
        assert "Insufficient evidence" in res["answer"]
        assert res["evidence_manifest"]["selected_evidence_count"] == 0

    asyncio.run(_run())

if __name__ == "__main__":
    pytest.main(["-v", __file__])
