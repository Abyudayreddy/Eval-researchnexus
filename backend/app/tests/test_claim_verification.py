import sys
import os
import pytest
import asyncio

# Add backend root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.services.assistant.claim_extractor import ClaimExtractor
from app.services.assistant.citation_repair import CitationRepair
from app.services.assistant.metrics import VerificationMetricsCalculator
from app.services.assistant.claim_verifier import ClaimVerifier

def test_claim_extraction():
    answer = "Hybrid retrieval improves recall by 15% [1]. However, accuracy was unchanged [2]."
    mapping = {"[1]": {"chunk_id": "c1"}, "[2]": {"chunk_id": "c2"}}
    claims = ClaimExtractor.extract_claims(answer, mapping)
    assert len(claims) == 2
    assert claims[0].claim_type == "numerical"
    assert claims[0].citation_ids == ["[1]"]
    assert claims[0].evidence_ids == ["c1"]

def test_stage_a_numerical_mismatch():
    claims = ClaimExtractor.extract_claims("Method X achieves 95% accuracy [1].", {"[1]": {"chunk_id": "c1"}})
    ev_map = {"c1": {"evidence_text": "Method X achieves 85% accuracy on benchmark."}}
    status, reason = ClaimVerifier._stage_a_deterministic_check(claims[0], ev_map)
    assert status == "UNSUPPORTED"
    assert "Numeric value(s)" in reason

def test_stage_a_negation_mismatch():
    claims = ClaimExtractor.extract_claims("The proposed model did not improve baseline recall [1].", {"[1]": {"chunk_id": "c1"}})
    ev_map = {"c1": {"evidence_text": "The proposed model improved baseline recall significantly."}}
    status, reason = ClaimVerifier._stage_a_deterministic_check(claims[0], ev_map)
    assert status == "UNSUPPORTED"
    assert "polarity/negation" in reason

def test_conservative_citation_repair():
    un_cited_claim = ClaimExtractor.extract_claims("Method X achieved 85% accuracy.", {})
    evidence = [{"chunk_id": "c1", "evidence_text": "Experimental setup shows Method X achieved 85% accuracy."}]
    mapping = {"[1]": {"chunk_id": "c1"}}
    
    repaired_claims = CitationRepair.repair_citations(un_cited_claim, evidence, mapping)
    assert repaired_claims[0].citation_repaired is True
    assert repaired_claims[0].citation_ids == ["[1]"]
    assert repaired_claims[0].claim_support_status == "SUPPORTED"

def test_metrics_calculation():
    claims = ClaimExtractor.extract_claims("Method X works [1]. Method Y fails [2].", {"[1]": {"chunk_id": "c1"}, "[2]": {"chunk_id": "c2"}})
    claims[0].claim_support_status = "SUPPORTED"
    claims[1].claim_support_status = "UNSUPPORTED"
    
    metrics = VerificationMetricsCalculator.calculate_metrics(claims)
    assert metrics["supported_claim_count"] == 1
    assert metrics["unsupported_claim_count"] == 1
    assert metrics["citation_precision"] == 0.5
    assert metrics["claim_support_rate"] == 0.5
    assert metrics["unsupported_claim_rate"] == 0.5

def test_verify_claims_pipeline():
    async def _run():
        raw_answer = "Method X achieves 85% accuracy on the benchmark [1]."
        mapping = {"[1]": {"chunk_id": "c1"}}
        evidence = [{"chunk_id": "c1", "title": "Paper 1", "evidence_text": "Method X achieves 85% accuracy on the benchmark."}]
        
        claims, audits, metrics = await ClaimVerifier.verify_claims(raw_answer, mapping, evidence)
        assert len(claims) == 1
        assert claims[0].claim_support_status in ["SUPPORTED", "VERIFICATION_UNAVAILABLE"]
        assert len(audits) == 1
        assert metrics["citation_precision"] >= 0.0

    asyncio.run(_run())

if __name__ == "__main__":
    pytest.main(["-v", __file__])
