import uuid
import re
from typing import List, Dict, Any, Optional
from app.services.assistant.models import ResearchGapCandidate

GAP_CATEGORIES = [
    "METHOD_GAP",
    "DATASET_GAP",
    "EVALUATION_GAP",
    "DOMAIN_GAP",
    "TASK_GAP",
    "GENERALIZATION_GAP",
    "INTEGRATION_GAP",
    "SCALABILITY_GAP",
    "REPRODUCIBILITY_GAP",
    "THEORETICAL_GAP"
]

class ResearchGapAnalyzer:
    """
    Analyzes literature coverage to identify evidence-backed research gap candidates.
    Evaluates evidence strength deterministically and prevents un-scoped global absence claims.
    """
    @staticmethod
    def analyze_gaps(
        allowed_paper_ids: List[str],
        evidence_id_map: Dict[str, Dict[str, Any]],
        llm_gap_data: List[Dict[str, Any]]
    ) -> List[ResearchGapCandidate]:
        gap_candidates: List[ResearchGapCandidate] = []

        for item in llm_gap_data:
            cat = item.get("category", "METHOD_GAP")
            if cat not in GAP_CATEGORIES:
                cat = "METHOD_GAP"

            title = item.get("title", "Underexplored Research Direction")
            obs_coverage = item.get("observed_coverage", f"Observed across selected literature ({len(allowed_paper_ids)} papers).")
            missing_dim = item.get("missing_dimension", "Specific evaluation dimension")
            reason = item.get("reason", "Limited evidence was found in the selected literature context.")

            # Sanitize wording to prevent un-scoped global absence claims
            title = ResearchGapAnalyzer._sanitize_gap_phrasing(title)
            reason = ResearchGapAnalyzer._sanitize_gap_phrasing(reason)

            paper_ids = item.get("paper_ids", allowed_paper_ids)
            evidence_ids = item.get("evidence_ids", [])

            # Deterministic evidence strength calculation
            strength = ResearchGapAnalyzer._calculate_evidence_strength(paper_ids, evidence_ids)

            gap_candidates.append(ResearchGapCandidate(
                gap_id=f"gap_{uuid.uuid4().hex[:8]}",
                category=cat,
                title=title,
                observed_coverage=obs_coverage,
                missing_dimension=missing_dim,
                reason=reason,
                evidence_strength=strength,
                paper_ids=paper_ids,
                evidence_ids=evidence_ids,
                support_status="SUPPORTED"
            ))

        return gap_candidates

    @staticmethod
    def _calculate_evidence_strength(paper_ids: List[str], evidence_ids: List[str]) -> str:
        unique_papers = len(set(paper_ids))
        unique_evidence = len(set(evidence_ids))

        if unique_papers >= 2 and unique_evidence >= 3:
            return "STRONG_EVIDENCE"
        elif unique_evidence >= 2:
            return "MODERATE_EVIDENCE"
        else:
            return "LIMITED_EVIDENCE"

    @staticmethod
    def _sanitize_gap_phrasing(text: str) -> str:
        """
        Replaces global absence claims like 'No research exists' with honest scoped statements.
        """
        forbidden_patterns = [
            (r"\bno research exists on\b", "limited evidence is present in the selected literature for"),
            (r"\bnobody has studied\b", "the selected literature provides limited evaluation of"),
            (r"\bunprecedented\b", "underexplored in selected evidence"),
            (r"\bthe first study to\b", "investigates a specific aspect in selected evidence"),
            (r"\bnever been done\b", "is not represented in the selected literature")
        ]

        sanitized = text
        for pat, repl in forbidden_patterns:
            sanitized = re.sub(pat, repl, sanitized, flags=re.IGNORECASE)

        return sanitized
