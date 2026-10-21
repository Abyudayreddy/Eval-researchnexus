from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.services.assistant.models import ResolvedContext

class ContextEligibility(BaseModel):
    can_use_local: bool
    can_use_online: bool
    can_use_uploads: bool
    should_retrieve: bool  # False for current_evidence
    allowed_paper_ids: List[str] = Field(default_factory=list)
    allowed_evidence_ids: List[str] = Field(default_factory=list)
    allowed_document_ids: List[str] = Field(default_factory=list)
    allowed_source_types: List[str] = Field(default_factory=list)
    scope: str
    mode: str

class ContextEligibilityEngine:
    @staticmethod
    def evaluate(resolved_ctx: ResolvedContext) -> ContextEligibility:
        scope = resolved_ctx.scope
        mode = resolved_ctx.mode
        
        # Rule 3: current_evidence = zero retrieval
        if scope == "current_evidence":
            return ContextEligibility(
                can_use_local=False,
                can_use_online=False,
                can_use_uploads=False,
                should_retrieve=False,
                allowed_paper_ids=resolved_ctx.allowed_paper_ids,
                allowed_evidence_ids=resolved_ctx.allowed_evidence_ids,
                allowed_document_ids=[],
                allowed_source_types=resolved_ctx.allowed_source_types,
                scope=scope,
                mode=mode
            )
            
        # Rule 6: uploaded_documents = only authorized uploaded documents
        if scope == "uploaded_documents":
            return ContextEligibility(
                can_use_local=False,
                can_use_online=False,
                can_use_uploads=True,
                should_retrieve=True,
                allowed_paper_ids=[],
                allowed_evidence_ids=[],
                allowed_document_ids=resolved_ctx.allowed_document_ids,
                allowed_source_types=["uploaded"],
                scope=scope,
                mode=mode
            )
            
        # Rule 4 & 5: single_paper / selected_papers
        if scope in ["single_paper", "selected_papers"]:
            sources = resolved_ctx.allowed_source_types or ["local", "online"]
            can_local = any(s in ["local", "mixed"] for s in sources)
            can_online = any(s in ["online", "mixed"] for s in sources)
            
            # Default to local/online if source_types list is empty (fallback)
            if not sources:
                can_local = True
                can_online = True

            return ContextEligibility(
                can_use_local=can_local,
                can_use_online=can_online,
                can_use_uploads=False,
                should_retrieve=True,
                allowed_paper_ids=resolved_ctx.allowed_paper_ids,
                allowed_evidence_ids=[],
                allowed_document_ids=[],
                allowed_source_types=sources,
                scope=scope,
                mode=mode
            )

        # Rule 7: all_research = configured Local + Online sources
        return ContextEligibility(
            can_use_local=True,
            can_use_online=True,
            can_use_uploads=False,
            should_retrieve=True,
            allowed_paper_ids=[],
            allowed_evidence_ids=[],
            allowed_document_ids=[],
            allowed_source_types=["local", "online", "mixed"],
            scope=scope,
            mode=mode
        )
