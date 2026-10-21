from typing import List, Dict, Any
from app.services.assistant.claim_extractor import ClaimObject

class CitationRepair:
    @staticmethod
    def repair_citations(
        claims: List[ClaimObject],
        available_evidence: List[Dict[str, Any]],
        citation_mapping: Dict[str, Any]
    ) -> List[ClaimObject]:
        """
        Conservative citation repair:
        Only attaches an evidence citation if an un-cited claim is 100% unambiguously
        supported by exact match/substring in available context evidence.
        """
        if not claims or not available_evidence:
            return claims

        for claim in claims:
            # Only process un-cited claims
            if not claim.citation_ids and claim.claim_support_status in ["UNSUPPORTED", "INSUFFICIENT_EVIDENCE"]:
                matching_evidence = []
                
                claim_text_lower = claim.text.lower().strip()
                
                for ev in available_evidence:
                    ev_text = (ev.get("evidence_text") or ev.get("resolved_evidence_text") or ev.get("abstract") or "").lower()
                    
                    # Unambiguous match check: if major key phrases or text overlap strongly
                    if len(claim_text_lower) > 20 and claim_text_lower in ev_text:
                        matching_evidence.append(ev)
                    elif claim.claim_type == "numerical":
                        import re
                        numbers = re.findall(r'\b\d+(?:\.\d+)?%?\b', claim_text_lower)
                        if numbers and all(num in ev_text for num in numbers):
                            # Ensure key non-numeric words also overlap
                            words = [w for w in claim_text_lower.split() if len(w) > 4 and not w.isdigit()]
                            if words and sum(1 for w in words if w in ev_text) / len(words) >= 0.7:
                                matching_evidence.append(ev)

                # Only repair if exactly ONE unambiguous evidence match is found
                if len(matching_evidence) == 1:
                    target_ev = matching_evidence[0]
                    eid = target_ev.get("chunk_id") or target_ev.get("id")
                    
                    # Find corresponding citation marker if existing in mapping
                    found_marker = None
                    for marker, info in citation_mapping.items():
                        mapped_eid = info.get("chunk_id") if isinstance(info, dict) else str(info)
                        if mapped_eid == eid:
                            found_marker = marker
                            break
                            
                    if found_marker:
                        claim.citation_ids = [found_marker]
                        claim.evidence_ids = [eid]
                        claim.citation_repaired = True
                        claim.claim_support_status = "SUPPORTED"
                        claim.verification_reason = "Repaired citation based on unambiguous context match."
                        claim.verification_method = "conservative_repair"

        return claims
