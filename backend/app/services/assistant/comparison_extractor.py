import re
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.paper import Paper, PaperChunk
from app.models.search_experiment import SearchExperiment
from app.models.document import ResearchDocument, DocumentChunk

# The exact 10 canonical research comparison dimensions requested by the specification
COMPARISON_DIMENSIONS = [
    "Research Goal / Problem",
    "Core Methodology & Architecture",
    "Datasets & Experimental Setup",
    "Primary Performance Metrics",
    "Computational Efficiency / Latency",
    "Limitations & Edge Cases",
    "Theoretical Assumptions",
    "Hardware / Deployment Bounds",
    "Novel Contribution Claim",
    "Reproducibility & Open Artifacts"
]

DIMENSION_KEYWORDS = {
    "Research Goal / Problem": [
        "problem", "objective", "goal", "aim", "purpose", "intend", "research question",
        "motivation", "challenge", "address", "gap in literature", "focus"
    ],
    "Core Methodology & Architecture": [
        "architecture", "methodology", "model", "algorithm", "pipeline", "framework",
        "technique", "approach", "network", "transformer", "encoder", "decoder",
        "convolution", "module", "layer", "dual-stream", "transport", "attention"
    ],
    "Datasets & Experimental Setup": [
        "dataset", "benchmark", "samples", "corpus", "experimental setup", "data collection",
        "train", "test split", "validation", "subset", "baseline setup", "experimental protocol"
    ],
    "Primary Performance Metrics": [
        "metric", "accuracy", "f1", "iou", "map", "precision", "recall", "auc",
        "bleu", "rouge", "ndcg", "mrr", "error rate", "loss", "score", "performance"
    ],
    "Computational Efficiency / Latency": [
        "latency", "runtime", "execution time", "throughput", "flops", "parameters",
        "param count", "memory footprint", "vram", "ram", "efficiency", "inference speed", "fps"
    ],
    "Limitations & Edge Cases": [
        "limitation", "failure mode", "edge case", "weakness", "drawback", "constraint",
        "restricted to", "negative result", "bottleneck", "trade-off"
    ],
    "Theoretical Assumptions": [
        "assumption", "assume", "theoretical condition", "formal constraint", "under the assumption",
        "proof", "theorem", "lemma", "bounded by", "postulate"
    ],
    "Hardware / Deployment Bounds": [
        "hardware", "gpu", "cpu", "tpu", "nvidia", "rtx", "a100", "v100", "cuda",
        "edge device", "mobile", "ram", "server", "cluster", "deployment"
    ],
    "Novel Contribution Claim": [
        "contribution", "novel", "novelty", "we propose", "in this paper, we", "main contribution",
        "to the best of our knowledge", "first to", "key innovation"
    ],
    "Reproducibility & Open Artifacts": [
        "code", "github", "repository", "open source", "weights", "checkpoint",
        "reproducibility", "supplementary", "artifact", "dataset available at", "release"
    ]
}

class ComparisonEvidenceExtractor:
    """
    Extracts paper-specific, dimension-categorized evidence for selected research papers.
    Strictly preserves paper attribution: NO cross-paper borrowing, NO universal fallback.
    """
    @staticmethod
    def extract_evidence_for_papers(
        db: Session,
        allowed_paper_ids: List[str],
        search_id: Optional[str] = None
    ) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        paper_evidence_map: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
            pid: {dim: [] for dim in COMPARISON_DIMENSIONS} for pid in allowed_paper_ids
        }

        for pid in allowed_paper_ids:
            # 1. Check local Paper & PaperChunk
            chunks = db.query(PaperChunk).filter(PaperChunk.paper_id == pid).all()
            if chunks:
                for chunk in chunks:
                    chunk_dict = {
                        "chunk_id": chunk.chunk_id,
                        "paper_id": pid,
                        "text": chunk.text,
                        "section": getattr(chunk, "section", None) or getattr(chunk, "section_name", None) or "Main",
                        "page": str(getattr(chunk, "page_start", None) or getattr(chunk, "page_number", None) or "1"),
                        "source_type": "local"
                    }
                    ComparisonEvidenceExtractor._categorize_chunk_into_dimensions(chunk_dict, paper_evidence_map[pid])
            else:
                # 2. Check if it's an uploaded user document in DocumentChunk
                doc_chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == pid).all()
                if doc_chunks:
                    for chunk in doc_chunks:
                        chunk_dict = {
                            "chunk_id": chunk.chunk_id,
                            "paper_id": pid,
                            "text": chunk.text,
                            "section": chunk.section_name or "Main",
                            "page": str(chunk.page_number) if chunk.page_number else "1",
                            "source_type": "user_document"
                        }
                        ComparisonEvidenceExtractor._categorize_chunk_into_dimensions(chunk_dict, paper_evidence_map[pid])
                else:
                    # 3. Check Paper abstract/title fallback
                    paper = db.query(Paper).filter(Paper.id == pid).first()
                    if paper and paper.abstract:
                        fake_chunk = {
                            "chunk_id": f"{pid}_abstract",
                            "paper_id": pid,
                            "text": paper.abstract,
                            "section": "Abstract",
                            "page": "1",
                            "source_type": "local"
                        }
                        ComparisonEvidenceExtractor._categorize_chunk_into_dimensions(fake_chunk, paper_evidence_map[pid])

        # 4. Check if search_id provides additional search result abstracts for allowed papers
        if search_id:
            try:
                import uuid
                search_uuid = uuid.UUID(search_id)
                experiment = db.query(SearchExperiment).filter(SearchExperiment.search_id == search_uuid).first()
                if experiment and experiment.results:
                    for res in experiment.results:
                        r_pid = res.get("id") or res.get("paper_id")
                        if r_pid in allowed_paper_ids:
                            evidence_text = res.get("evidence_text") or res.get("abstract")
                            if evidence_text:
                                ext_chunk = {
                                    "chunk_id": f"{r_pid}_online_ref",
                                    "paper_id": r_pid,
                                    "text": evidence_text,
                                    "section": "Evidence Summary",
                                    "page": "1",
                                    "source_type": res.get("retrieval_source", "online")
                                }
                                ComparisonEvidenceExtractor._categorize_chunk_into_dimensions(ext_chunk, paper_evidence_map[r_pid])
            except Exception:
                pass

        return paper_evidence_map

    @staticmethod
    def _categorize_chunk_into_dimensions(chunk_dict: Dict[str, Any], dim_map: Dict[str, List[Dict[str, Any]]]):
        text_lower = chunk_dict["text"].lower()
        section_lower = (chunk_dict.get("section") or "").lower()

        for dim, keywords in DIMENSION_KEYWORDS.items():
            dim_lower = dim.lower()
            # Match section header keywords
            if any(part in section_lower for part in dim_lower.split(" / ")):
                dim_map[dim].append(chunk_dict)
                continue

            # Match keyword presence in chunk text
            for kw in keywords:
                if kw in text_lower:
                    dim_map[dim].append(chunk_dict)
                    break
