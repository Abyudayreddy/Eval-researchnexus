import re
import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.paper import Paper, PaperChunk
from app.models.search_experiment import SearchExperiment
from app.services.assistant.models import ResearchTheme

class SynthesisEvidenceExtractor:
    """
    Extracts evidence and groups paper-by-paper observations into research themes.
    Performs deterministic theme deduplication and attribution preservation.
    """
    @staticmethod
    def extract_evidence_by_theme(
        db: Session,
        allowed_paper_ids: List[str],
        search_id: Optional[str] = None
    ) -> Tuple[List[ResearchTheme], Dict[str, Dict[str, Any]]]:
        """
        Returns (themes, evidence_map)
        """
        raw_chunks: List[Dict[str, Any]] = []

        # 1. Fetch chunks for allowed papers
        for pid in allowed_paper_ids:
            chunks = db.query(PaperChunk).filter(PaperChunk.paper_id == pid).all()
            if not chunks:
                paper = db.query(Paper).filter(Paper.id == pid).first()
                if paper and paper.abstract:
                    raw_chunks.append({
                        "chunk_id": f"{pid}_abstract",
                        "paper_id": pid,
                        "title": paper.title or pid,
                        "text": paper.abstract,
                        "section": "Abstract",
                        "page": "1",
                        "source_type": "local"
                    })
                continue

            for chunk in chunks:
                raw_chunks.append({
                    "chunk_id": chunk.chunk_id,
                    "paper_id": pid,
                    "title": chunk.paper_id,
                    "text": chunk.text,
                    "section": chunk.section_name or "Main",
                    "page": str(chunk.page_number) if chunk.page_number else "1",
                    "source_type": "local"
                })

        # 2. Theme Categorization & Deduplication
        theme_buckets: Dict[str, Dict[str, Any]] = {
            "Retrieval & Search": {"description": "Mechanisms for document and evidence retrieval.", "pids": set(), "eids": set(), "sources": set()},
            "Architecture & Models": {"description": "Model design, neural layers, and representation.", "pids": set(), "eids": set(), "sources": set()},
            "Verification & Grounding": {"description": "Claim verification, citation integrity, and fact checking.", "pids": set(), "eids": set(), "sources": set()},
            "Evaluation & Benchmarks": {"description": "Experimental setups, metrics, datasets, and performance.", "pids": set(), "eids": set(), "sources": set()},
            "Domain Applications": {"description": "Task-specific adaptations and real-world deployment.", "pids": set(), "eids": set(), "sources": set()}
        }

        evidence_id_map: Dict[str, Dict[str, Any]] = {}

        for chk in raw_chunks:
            eid = chk["chunk_id"]
            pid = chk["paper_id"]
            text_lower = chk["text"].lower()

            evidence_id_map[eid] = chk

            matched = False
            if any(k in text_lower for k in ["retrieval", "bm25", "dense", "chroma", "search", "rrf"]):
                theme_buckets["Retrieval & Search"]["pids"].add(pid)
                theme_buckets["Retrieval & Search"]["eids"].add(eid)
                theme_buckets["Retrieval & Search"]["sources"].add(chk["source_type"])
                matched = True

            if any(k in text_lower for k in ["model", "architecture", "bge", "transformer", "encoder", "llm"]):
                theme_buckets["Architecture & Models"]["pids"].add(pid)
                theme_buckets["Architecture & Models"]["eids"].add(eid)
                theme_buckets["Architecture & Models"]["sources"].add(chk["source_type"])
                matched = True

            if any(k in text_lower for k in ["verify", "verification", "claim", "citation", "grounding", "proof"]):
                theme_buckets["Verification & Grounding"]["pids"].add(pid)
                theme_buckets["Verification & Grounding"]["eids"].add(eid)
                theme_buckets["Verification & Grounding"]["sources"].add(chk["source_type"])
                matched = True

            if any(k in text_lower for k in ["dataset", "eval", "metric", "accuracy", "benchmark", "result", "f1"]):
                theme_buckets["Evaluation & Benchmarks"]["pids"].add(pid)
                theme_buckets["Evaluation & Benchmarks"]["eids"].add(eid)
                theme_buckets["Evaluation & Benchmarks"]["sources"].add(chk["source_type"])
                matched = True

            if not matched:
                theme_buckets["Domain Applications"]["pids"].add(pid)
                theme_buckets["Domain Applications"]["eids"].add(eid)
                theme_buckets["Domain Applications"]["sources"].add(chk["source_type"])

        # 3. Construct ResearchTheme objects
        themes: List[ResearchTheme] = []
        for t_name, data in theme_buckets.items():
            if data["eids"]:
                themes.append(ResearchTheme(
                    theme_id=f"theme_{uuid.uuid4().hex[:8]}",
                    name=t_name,
                    description=data["description"],
                    paper_ids=list(data["pids"]),
                    evidence_ids=list(data["eids"]),
                    support_status="SUPPORTED",
                    source_types=list(data["sources"]) if data["sources"] else ["LOCAL"]
                ))

        return themes, evidence_id_map
