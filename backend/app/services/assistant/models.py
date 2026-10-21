from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import datetime

class PaperRef(BaseModel):
    paper_id: str
    title: str
    authors: Optional[str] = "Unknown Authors"
    publication_year: Optional[Any] = None
    url: Optional[str] = None
    source_type: Optional[str] = "local"  # local | online | mixed | uploaded
    search_id: Optional[str] = None

class EvidenceRef(BaseModel):
    paper_id: str
    chunk_id: str
    search_id: Optional[str] = None
    source_type: Optional[str] = "local"  # local | online | mixed | uploaded
    text: str
    section: Optional[Any] = None
    page: Optional[Any] = None

class DocumentRef(BaseModel):
    document_id: str
    filename: str
    source_type: str = "uploaded"

class ResearchContext(BaseModel):
    context_snapshot_id: str
    session_id: str
    search_id: Optional[str] = None
    mode: str  # research | paper | compare | evidence | upload | synthesis
    scope: str  # all_research | selected_papers | single_paper | current_evidence | uploaded_documents
    papers: List[PaperRef] = Field(default_factory=list)
    evidence: List[EvidenceRef] = Field(default_factory=list)
    uploaded_documents: List[DocumentRef] = Field(default_factory=list)
    provenance: str  # LOCAL | ONLINE | UPLOADED | MIXED
    snapshot_created_at: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    snapshot_version: int = 1
    context_hash: str

class ResolvedContext(BaseModel):
    allowed_paper_ids: List[str] = Field(default_factory=list)
    allowed_evidence_ids: List[str] = Field(default_factory=list)
    allowed_document_ids: List[str] = Field(default_factory=list)
    allowed_source_types: List[str] = Field(default_factory=list)
    search_id: Optional[str] = None
    mode: str
    scope: str
    context_snapshot_id: str
    context_hash: str
    evidence_items: List[Dict[str, Any]] = Field(default_factory=list)


# --- Phase 3.6 Multi-Paper Comparison Models ---

class MetricCompatibility(BaseModel):
    metric_name: Optional[str] = None
    dataset: Optional[str] = None
    split: Optional[str] = None
    evaluation_protocol: Optional[str] = None
    unit: Optional[str] = None
    is_comparable: bool = False
    comparison_note: str = "Not directly comparable."

class ComparisonCell(BaseModel):
    paper_id: str
    dimension_id: str
    dimension_name: str
    status: str = "EVIDENCE_BACKED"  # EVIDENCE_BACKED | NOT_REPORTED | EXTRACTION_FAILED
    value: str
    evidence_id: Optional[str] = None
    evidence_text: Optional[str] = None
    page_number: Optional[Any] = None
    chunk_id: Optional[str] = None
    source_id: Optional[str] = None
    confidence: Optional[float] = None
    dimension: Optional[str] = None
    value_type: str = "synthesized_summary"  # extracted_fact | synthesized_summary | unavailable
    evidence_ids: List[str] = Field(default_factory=list)
    evidence_refs: List[EvidenceRef] = Field(default_factory=list)
    support_status: str = "SUPPORTED"  # SUPPORTED | PARTIALLY_SUPPORTED | INSUFFICIENT_EVIDENCE | UNSUPPORTED | VERIFICATION_UNAVAILABLE
    provenance: str = "LOCAL"  # LOCAL | ONLINE | UPLOADED | MIXED
    is_available: bool = True

class ComparisonRow(BaseModel):
    dimension: str
    cells: List[ComparisonCell] = Field(default_factory=list)
    comparison_claims: List[str] = Field(default_factory=list)
    metric_compatibility: Optional[MetricCompatibility] = None

class ComparisonMatrix(BaseModel):
    dimensions: List[str] = Field(default_factory=list)
    paper_ids: List[str] = Field(default_factory=list)
    rows: List[ComparisonRow] = Field(default_factory=list)

class ComparisonSummary(BaseModel):
    similarities: List[str] = Field(default_factory=list)
    differences: List[str] = Field(default_factory=list)
    evidence_backed_findings: List[str] = Field(default_factory=list)
    potential_conflicts: List[str] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)

class ComparisonResult(BaseModel):
    comparison_id: str
    session_id: str
    context_snapshot_id: str
    context_hash: str
    paper_ids: List[str]
    dimensions: List[str]
    matrix: ComparisonMatrix
    summary: ComparisonSummary
    claims: List[Any] = Field(default_factory=list)
    verification_metrics: Dict[str, Any] = Field(default_factory=dict)
    latencies: Dict[str, float] = Field(default_factory=dict)
    reproducibility_export: Dict[str, Any] = Field(default_factory=dict)

# --- Phase 3.7 Synthesis, Contradiction & Research Gap Models ---

class ResearchTheme(BaseModel):
    theme_id: str
    name: str
    description: str
    paper_ids: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    support_status: str = "SUPPORTED"
    source_types: List[str] = Field(default_factory=list)

class LiteratureFinding(BaseModel):
    finding_id: str
    text: str
    type: str  # COMMON_FINDING | DIFFERENT_FINDING | LIMITATION | OPEN_QUESTION | POTENTIAL_GAP
    paper_ids: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    claim_status: str = "SUPPORTED"

class ContradictionCandidate(BaseModel):
    conflict_id: str
    conflict_type: str  # DIRECT_CONTRADICTION | NUMERICAL_CONTRADICTION | METHODOLOGICAL_TENSION | CONDITIONAL_DISAGREEMENT | APPARENT_CONFLICT
    paper_a_id: str
    paper_b_id: str
    claim_a: str
    claim_b: str
    evidence_a_ids: List[str] = Field(default_factory=list)
    evidence_b_ids: List[str] = Field(default_factory=list)
    conflict_basis: str
    support_status: str = "PARTIALLY_SUPPORTED"

class ResearchGapCandidate(BaseModel):
    gap_id: str
    category: str  # METHOD_GAP | DATASET_GAP | EVALUATION_GAP | DOMAIN_GAP | TASK_GAP | GENERALIZATION_GAP | INTEGRATION_GAP | SCALABILITY_GAP | REPRODUCIBILITY_GAP | THEORETICAL_GAP
    title: str
    observed_coverage: str
    missing_dimension: str
    reason: str
    evidence_strength: str  # STRONG_EVIDENCE | MODERATE_EVIDENCE | LIMITED_EVIDENCE
    paper_ids: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    support_status: str = "SUPPORTED"

class SynthesisResult(BaseModel):
    synthesis_id: str
    session_id: str
    context_snapshot_id: str
    context_hash: str
    mode: str
    scope: str
    analysis_scope: str = "Selected literature context"
    coverage_statement: str = "Findings reflect the selected literature only."
    themes: List[ResearchTheme] = Field(default_factory=list)
    findings: List[LiteratureFinding] = Field(default_factory=list)
    agreements: List[str] = Field(default_factory=list)
    differences: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    potential_conflicts: List[ContradictionCandidate] = Field(default_factory=list)
    gap_candidates: List[ResearchGapCandidate] = Field(default_factory=list)
    claims: List[Any] = Field(default_factory=list)
    citations: List[Any] = Field(default_factory=list)
    evidence: List[EvidenceRef] = Field(default_factory=list)
    verification_metrics: Dict[str, Any] = Field(default_factory=dict)
    latencies: Dict[str, float] = Field(default_factory=dict)
    reproducibility_export: Dict[str, Any] = Field(default_factory=dict)
