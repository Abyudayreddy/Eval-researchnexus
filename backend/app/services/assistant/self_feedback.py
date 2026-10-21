import hashlib
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from app.services.assistant.claim_extractor import ClaimObject

class SelfFeedbackResult(BaseModel):
    needs_refinement: bool
    feedback_category: str  # NO_REFINEMENT_NEEDED | MISSING_EVIDENCE | WEAK_EVIDENCE | UNSUPPORTED_CLAIM | PARTIAL_SUPPORT | NUMERICAL_SUPPORT_GAP
    issues: List[str] = Field(default_factory=list)
    unsupported_claim_ids: List[str] = Field(default_factory=list)
    insufficient_claim_ids: List[str] = Field(default_factory=list)
    suggested_focus: List[str] = Field(default_factory=list)
    feedback_signature: str
    feedback_summary: str

class SelfFeedbackEngine:
    @staticmethod
    def evaluate(
        question: str,
        claims: List[ClaimObject],
        available_evidence: List[Dict[str, Any]],
        verification_metrics: Dict[str, Any]
    ) -> SelfFeedbackResult:
        """
        Evidence & Verification-aware self-feedback.
        Uses Phase 3.4 claim support statuses to decide if refinement is necessary.
        Operates strictly on context evidence only. Zero hidden external retrieval.
        """
        unsupported_claims = [c for c in claims if c.claim_support_status == "UNSUPPORTED"]
        insufficient_claims = [c for c in claims if c.claim_support_status == "INSUFFICIENT_EVIDENCE"]
        partial_claims = [c for c in claims if c.claim_support_status == "PARTIALLY_SUPPORTED"]

        unsupported_ids = [c.claim_id for c in unsupported_claims]
        insufficient_ids = [c.claim_id for c in insufficient_claims]

        issues = []
        suggested_focus = []
        feedback_category = "NO_REFINEMENT_NEEDED font-bold"

        if unsupported_claims:
            feedback_category = "UNSUPPORTED_CLAIM"
            for c in unsupported_claims:
                issues.append(f"Claim {c.claim_id} ({c.claim_type}) unsupported: {c.verification_reason}")
                suggested_focus.append(c.text)
        elif insufficient_claims:
            feedback_category = "MISSING_EVIDENCE"
            for c in insufficient_claims:
                issues.append(f"Claim {c.claim_id} lacks sufficient evidence context.")
                suggested_focus.append(c.text)
        elif partial_claims:
            feedback_category = "PARTIAL_SUPPORT"
            for c in partial_claims:
                issues.append(f"Claim {c.claim_id} only partially supported.")
                suggested_focus.append(c.text)

        needs_refinement = len(unsupported_claims) > 0 or len(insufficient_claims) > 0 or len(partial_claims) > 0

        if not needs_refinement:
            feedback_category = "NO_REFINEMENT_NEEDED"
            feedback_summary = "Initial answer is fully supported by evidence context. No refinement needed."
        else:
            feedback_summary = f"Refinement required for {len(issues)} claim issue(s)."

        # Compute deterministic feedback signature for anti-oscillation check
        sig_input = f"{feedback_category}:" + ",".join(sorted(unsupported_ids + insufficient_ids))
        feedback_signature = hashlib.sha256(sig_input.encode('utf-8')).hexdigest()[:16]

        return SelfFeedbackResult(
            needs_refinement=needs_refinement,
            feedback_category=feedback_category,
            issues=issues,
            unsupported_claim_ids=unsupported_ids,
            insufficient_claim_ids=insufficient_ids,
            suggested_focus=suggested_focus,
            feedback_signature=feedback_signature,
            feedback_summary=feedback_summary
        )
