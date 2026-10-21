import uuid
from typing import List, Dict, Any, Optional
from app.services.assistant.models import ContradictionCandidate

class ContradictionDetector:
    """
    Identifies candidate conflicts across literature evidence without truth arbitration.
    Classifies conflicts into 5 candidate types and evaluates metric/dataset context compatibility.
    """
    @staticmethod
    def detect_candidate_conflicts(
        evidence_id_map: Dict[str, Dict[str, Any]],
        llm_conflict_data: List[Dict[str, Any]]
    ) -> List[ContradictionCandidate]:
        candidates: List[ContradictionCandidate] = []

        for item in llm_conflict_data:
            c_type = item.get("conflict_type", "APPARENT_CONFLICT")
            valid_types = [
                "DIRECT_CONTRADICTION",
                "NUMERICAL_CONTRADICTION",
                "METHODOLOGICAL_TENSION",
                "CONDITIONAL_DISAGREEMENT",
                "APPARENT_CONFLICT"
            ]
            if c_type not in valid_types:
                c_type = "APPARENT_CONFLICT"

            paper_a = item.get("paper_a_id", "Paper_A")
            paper_b = item.get("paper_b_id", "Paper_B")
            claim_a = item.get("claim_a", "Claim A")
            claim_b = item.get("claim_b", "Claim B")
            basis = item.get("conflict_basis", "Evidence comparison indicates divergent observations.")

            ev_a = item.get("evidence_a_ids", [])
            ev_b = item.get("evidence_b_ids", [])

            # Check context compatibility for numerical conflicts
            if c_type == "NUMERICAL_CONTRADICTION":
                metric_a = item.get("metric_a")
                metric_b = item.get("metric_b")
                dataset_a = item.get("dataset_a")
                dataset_b = item.get("dataset_b")

                if (metric_a and metric_b and metric_a.lower() != metric_b.lower()) or \
                   (dataset_a and dataset_b and dataset_a.lower() != dataset_b.lower()):
                    c_type = "CONDITIONAL_DISAGREEMENT"
                    basis += " (Reclassified to CONDITIONAL_DISAGREEMENT due to differing metric/dataset settings)."

            candidates.append(ContradictionCandidate(
                conflict_id=f"conflict_{uuid.uuid4().hex[:8]}",
                conflict_type=c_type,
                paper_a_id=paper_a,
                paper_b_id=paper_b,
                claim_a=claim_a,
                claim_b=claim_b,
                evidence_a_ids=ev_a,
                evidence_b_ids=ev_b,
                conflict_basis=basis,
                support_status="PARTIALLY_SUPPORTED"
            ))

        return candidates
