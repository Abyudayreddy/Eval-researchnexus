import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ClaimObject(BaseModel):
    claim_id: str
    text: str
    claim_text: Optional[str] = None
    claim_type: str  # factual | methodological | numerical | comparative | causal | synthesis
    citation_ids: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    supporting_passages: List[str] = Field(default_factory=list)
    supporting_passage: str = ""
    source_paper_title: str = ""
    source_paper_id: str = ""
    paper_ids: List[str] = Field(default_factory=list)
    provenance: str = "LOCAL"
    claim_support_status: str = "UNSUPPORTED"  # SUPPORTED | PARTIALLY_SUPPORTED | INSUFFICIENT_EVIDENCE | UNSUPPORTED | VERIFICATION_UNAVAILABLE
    verification_status: str = "UNSUPPORTED"
    support_level: str = "UNSUPPORTED"
    confidence_score: float = 0.5
    entailment_score: float = 0.5
    citation_text: str = ""
    stage_a_status: str = "VALID_CITATION_MAPPING"
    stage_b_status: str = "ENTAILMENT_VERIFIED"
    verification_method: str = "none"
    verification_reason: str = ""
    citation_repaired: bool = False

class ClaimExtractor:
    @staticmethod
    def extract_claims(raw_text: str, citation_mapping: Dict[str, Any]) -> List[ClaimObject]:
        """
        Splits response into atomic research claims, identifies explicit citation markers,
        and classifies claim types.
        """
        if not raw_text or not raw_text.strip():
            return []

        # Split text into paragraphs/sentences while preserving citations
        raw_sentences = re.split(r'(?<=[.!?])\s+', raw_text.strip())
        claims: List[ClaimObject] = []
        claim_counter = 1

        for sentence in raw_sentences:
            s_clean = sentence.strip()
            if not s_clean or len(s_clean) < 15:
                continue

            # Skip header or structural titles
            if s_clean.startswith('#') or s_clean.endswith(':'):
                continue

            # Extract numeric citations like [1], [2]
            cited_markers = re.findall(r'\[(\d+)\]', s_clean)
            citation_ids = [f"[{m}]" for m in cited_markers]
            
            # Map citation markers to evidence IDs
            evidence_ids = []
            for marker in citation_ids:
                if marker in citation_mapping:
                    ev_info = citation_mapping[marker]
                    eid = ev_info.get("chunk_id") if isinstance(ev_info, dict) else str(ev_info)
                    if eid and eid not in evidence_ids:
                        evidence_ids.append(eid)

            # Classify claim type conservatively
            claim_type = ClaimExtractor._classify_claim_type(s_clean)

            # Clean citation tags from claim text for analysis
            clean_text = re.sub(r'\[\d+\]', '', s_clean).strip()

            claims.append(ClaimObject(
                claim_id=f"claim_{claim_counter:02d}",
                text=clean_text,
                claim_type=claim_type,
                citation_ids=citation_ids,
                evidence_ids=evidence_ids
            ))
            claim_counter += 1

        return claims

    @staticmethod
    def _classify_claim_type(text: str) -> str:
        text_lower = text.lower()
        
        # Numerical
        if re.search(r'\b\d+(?:\.\d+)?%|\b\d+\.\d+|\bfrom \d+ to \d+\b', text_lower):
            return "numerical"
        
        # Comparative
        if any(w in text_lower for w in ["outperform", "better than", "compared to", "higher than", "lower than", "superior", "versus"]):
            return "comparative"
            
        # Causal
        if any(w in text_lower for w in ["causes", "leads to", "resulted in", "due to", "because of", "driven by"]):
            return "causal"
            
        # Synthesis
        if any(w in text_lower for w in ["generally agree", "literature suggests", "across studies", "broadly", "collectively"]):
            return "synthesis"
            
        # Methodological
        if any(w in text_lower for w in ["method", "algorithm", "architecture", "dataset", "framework", "model"]):
            return "methodological"
            
        return "factual"
