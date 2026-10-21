from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import json

from app.db.session import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.paper import Paper
from app.models.workspace import Bookmark, ProjectPaper, Project
from app.services.llm_provider import LLMProviderManager

router = APIRouter()

class SynthesizeRequest(BaseModel):
    paper_ids: List[str]

@router.post("/synthesize")
async def synthesize_literature_review(
    req: SynthesizeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not req.paper_ids:
        raise HTTPException(status_code=400, detail="No paper IDs provided")

    # Deduplicate
    unique_ids = list(dict.fromkeys(req.paper_ids))
    
    # Authorize papers (must be in user's bookmarks or projects)
    # Get user's bookmarks
    user_bookmarks = db.query(Bookmark.paper_id).filter(Bookmark.user_id == current_user.id).all()
    bookmarked_ids = {b[0] for b in user_bookmarks}
    
    # Get user's project papers
    user_projects = db.query(Project.id).filter(Project.user_id == current_user.id).all()
    project_ids = [p[0] for p in user_projects]
    project_papers = db.query(ProjectPaper.paper_id).filter(ProjectPaper.project_id.in_(project_ids)).all()
    project_paper_ids = {p[0] for p in project_papers}
    
    accessible_ids = bookmarked_ids.union(project_paper_ids)
    
    # Filter for accessible and requested
    valid_ids = [pid for pid in unique_ids if pid in accessible_ids]
    if not valid_ids:
        raise HTTPException(status_code=403, detail="None of the selected papers are accessible")

    # Load papers
    papers = db.query(Paper).filter(Paper.id.in_(valid_ids)).all()
    
    evidence_ready_papers = []
    metadata_only_papers = []
    
    # Organize evidence
    for p in papers:
        # Check if abstract exists and is meaningful
        if p.abstract and len(p.abstract.strip()) > 50:
            evidence_ready_papers.append(p)
        else:
            metadata_only_papers.append(p)
            
    sources = []
    # 1-indexed for citations
    for i, p in enumerate(evidence_ready_papers, 1):
        sources.append({
            "paper_id": p.id,
            "title": p.title,
            "evidence_status": "evidence_ready",
            "citation_index": i
        })
        
    for p in metadata_only_papers:
        sources.append({
            "paper_id": p.id,
            "title": p.title,
            "evidence_status": "metadata_only",
            "citation_index": None
        })

    if not evidence_ready_papers:
        return {
            "review": "",
            "sources": sources,
            "evidence_trace": {
                "selected_count": len(papers),
                "evidence_ready_count": 0,
                "metadata_only_count": len(metadata_only_papers),
                "papers_sent_to_llm": 0,
                "provider": None,
                "model": None,
                "generation_status": "insufficient_evidence"
            },
            "generation_status": "insufficient_evidence"
        }

    # Build context (max 6000 chars per abstract)
    context_chunks = []
    for i, p in enumerate(evidence_ready_papers, 1):
        abs_text = p.abstract.strip()
        if len(abs_text) > 6000:
            abs_text = abs_text[:6000] + "..."
            
        chunk = f"[{i}] {p.title}\nAuthors: {p.authors or 'Unknown'}\nPublication Date: {str(p.publish_date)[:10] if p.publish_date else 'Unknown'}\nAbstract:\n{abs_text}\n"
        context_chunks.append(chunk)
        
    evidence_context = "\n".join(context_chunks)

    query_instructions = (
        "You are generating a structured literature review strictly from the supplied research evidence.\n\n"
        "Use ONLY the provided papers and their supplied text. Do not add facts from pretrained/general knowledge. "
        "Do not invent citations. Do not claim a paper supports a statement unless the supplied evidence supports it. "
        "When evidence is insufficient, explicitly say so.\n\n"
        "Generate a structured review with these exact sections (omit a section or state 'Insufficient evidence' if not supported):\n"
        "### Overview\n"
        "### Key Findings\n"
        "### Methods\n"
        "### Common Themes\n"
        "### Differences\n"
        "### Research Gaps\n"
        "### Conclusion\n\n"
        "Cite your sources using the [index] numbers provided. Example: '... [1][3]'"
    )

    llm_result = await LLMProviderManager.generate(query=query_instructions, evidence_context=evidence_context)

    return {
        "review": llm_result["text"],
        "sources": sources,
        "evidence_trace": {
            "selected_count": len(papers),
            "evidence_ready_count": len(evidence_ready_papers),
            "metadata_only_count": len(metadata_only_papers),
            "papers_sent_to_llm": len(evidence_ready_papers),
            "provider": llm_result["provider"],
            "model": llm_result["model"],
            "generation_status": llm_result["generation_status"]
        },
        "generation_status": llm_result["generation_status"]
    }
