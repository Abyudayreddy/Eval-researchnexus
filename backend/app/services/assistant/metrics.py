from typing import List, Dict, Any
from app.services.assistant.claim_extractor import ClaimObject

class VerificationMetricsCalculator:
    @staticmethod
    def calculate_metrics(claims: List[ClaimObject]) -> Dict[str, Any]:
        """
        Calculates explicit mathematical verification metrics:
        - CitationPrecision = supported_cited_claims / evaluated_cited_claims
        - CitationCoverage = cited_verifiable_claims / all_verifiable_claims
        - ClaimSupportRate = supported_claims / all_verifiable_claims
        - UnsupportedClaimRate = unsupported_claims / all_verifiable_claims
        """
        total_claims = len(claims)
        if total_claims == 0:
            return {
                "supported_claim_count": 0,
                "partially_supported_claim_count": 0,
                "insufficient_claim_count": 0,
                "unsupported_claim_count": 0,
                "citation_precision": 0.0,
                "citation_coverage": 0.0,
                "claim_support_rate": 0.0,
                "unsupported_claim_rate": 0.0
            }

        supported_count = sum(1 for c in claims if c.claim_support_status == "SUPPORTED")
        partial_count = sum(1 for c in claims if c.claim_support_status == "PARTIALLY_SUPPORTED")
        insufficient_count = sum(1 for c in claims if c.claim_support_status == "INSUFFICIENT_EVIDENCE")
        unsupported_count = sum(1 for c in claims if c.claim_support_status == "UNSUPPORTED")

        evaluated_cited_claims = sum(1 for c in claims if c.citation_ids)
        supported_cited_claims = sum(1 for c in claims if c.citation_ids and c.claim_support_status == "SUPPORTED")

        verifiable_claims = total_claims
        cited_verifiable_claims = sum(1 for c in claims if c.citation_ids)

        citation_precision = (supported_cited_claims / evaluated_cited_claims) if evaluated_cited_claims > 0 else 0.0
        citation_coverage = (cited_verifiable_claims / verifiable_claims) if verifiable_claims > 0 else 0.0
        claim_support_rate = (supported_count / verifiable_claims) if verifiable_claims > 0 else 0.0
        unsupported_claim_rate = (unsupported_count / verifiable_claims) if verifiable_claims > 0 else 0.0

        return {
            "supported_claim_count": supported_count,
            "partially_supported_claim_count": partial_count,
            "insufficient_claim_count": insufficient_count,
            "unsupported_claim_count": unsupported_count,
            "citation_precision": round(citation_precision, 4),
            "citation_coverage": round(citation_coverage, 4),
            "claim_support_rate": round(claim_support_rate, 4),
            "unsupported_claim_rate": round(unsupported_claim_rate, 4)
        }
