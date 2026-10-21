import uuid
import json
import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.session import ResearchMemory, ResearchSession

VALID_MEMORY_TYPES = [
    "RESEARCH_GOAL",
    "RESEARCH_CONSTRAINT",
    "SELECTED_PAPER",
    "KEY_FINDING",
    "EVIDENCE_REFERENCE",
    "RESEARCH_DECISION",
    "OPEN_QUESTION",
    "POTENTIAL_GAP",
    "RESEARCH_NOTE"
]

class ResearchMemoryService:
    @staticmethod
    def create_memory(
        db: Session,
        session_id: str,
        content: str,
        memory_type: str = "KEY_FINDING",
        user_id: str = "default_user",
        memory_origin: str = "USER_RECORDED",
        status: str = "ACCEPTED",
        paper_ids: Optional[List[str]] = None,
        evidence_ids: Optional[List[str]] = None,
        source_artifact_ids: Optional[List[str]] = None
    ) -> ResearchMemory:
        if memory_type not in VALID_MEMORY_TYPES:
            memory_type = "KEY_FINDING"

        memory_id = f"mem_{uuid.uuid4().hex[:12]}"
        mem = ResearchMemory(
            memory_id=memory_id,
            session_id=session_id,
            user_id=user_id,
            memory_type=memory_type,
            content=content,
            status=status,
            memory_origin=memory_origin,
            paper_ids=json.dumps(paper_ids) if paper_ids else None,
            evidence_ids=json.dumps(evidence_ids) if evidence_ids else None,
            source_artifact_ids=json.dumps(source_artifact_ids) if source_artifact_ids else None,
            version=1,
            created_by=user_id
        )
        db.add(mem)

        # Touch last_activity_at on session
        session = db.query(ResearchSession).filter(ResearchSession.session_id == session_id).first()
        if session:
            session.last_activity_at = datetime.datetime.utcnow()

        db.commit()
        db.refresh(mem)
        return mem

    @staticmethod
    def suggest_ai_memory(
        db: Session,
        session_id: str,
        content: str,
        memory_type: str = "KEY_FINDING",
        user_id: str = "default_user",
        paper_ids: Optional[List[str]] = None,
        evidence_ids: Optional[List[str]] = None
    ) -> ResearchMemory:
        """
        Creates an AI-suggested memory in SUGGESTED status.
        Requires explicit user approval (accept_memory) before becoming persistent research memory.
        """
        return ResearchMemoryService.create_memory(
            db=db,
            session_id=session_id,
            user_id=user_id,
            content=content,
            memory_type=memory_type,
            memory_origin="AI_SUGGESTED",
            status="SUGGESTED",
            paper_ids=paper_ids,
            evidence_ids=evidence_ids
        )

    @staticmethod
    def update_memory_status(db: Session, memory_id: str, status: str, user_id: str = "default_user") -> ResearchMemory:
        mem = db.query(ResearchMemory).filter(
            ResearchMemory.memory_id == memory_id,
            ResearchMemory.user_id == user_id
        ).first()

        if not mem:
            raise ValueError("MEMORY_NOT_FOUND")

        if status in ["ACCEPTED", "REJECTED", "SUGGESTED"]:
            mem.status = status
            mem.updated_at = datetime.datetime.utcnow()
            db.commit()
            db.refresh(mem)

        return mem

    @staticmethod
    def edit_memory_content(db: Session, memory_id: str, new_content: str, user_id: str = "default_user") -> ResearchMemory:
        mem = db.query(ResearchMemory).filter(
            ResearchMemory.memory_id == memory_id,
            ResearchMemory.user_id == user_id
        ).first()

        if not mem:
            raise ValueError("MEMORY_NOT_FOUND")

        mem.content = new_content
        mem.status = "ACCEPTED"
        mem.version += 1
        mem.updated_at = datetime.datetime.utcnow()
        db.commit()
        db.refresh(mem)
        return mem

    @staticmethod
    def delete_memory(db: Session, memory_id: str, user_id: str = "default_user") -> bool:
        mem = db.query(ResearchMemory).filter(
            ResearchMemory.memory_id == memory_id,
            ResearchMemory.user_id == user_id
        ).first()

        if not mem:
            return False

        db.delete(mem)
        db.commit()
        return True

    @staticmethod
    def get_eligible_memories_for_prompt(db: Session, session_id: str, user_id: str = "default_user") -> List[Dict[str, Any]]:
        """
        Returns active, accepted, session-scoped memories eligible for Assistant prompt injection.
        Enforces evidence > memory rule: memories are context references only.
        """
        memories = db.query(ResearchMemory).filter(
            ResearchMemory.session_id == session_id,
            ResearchMemory.user_id == user_id,
            ResearchMemory.status == "ACCEPTED"
        ).order_by(ResearchMemory.created_at.desc()).limit(15).all()

        return [
            {
                "memory_id": m.memory_id,
                "memory_type": m.memory_type,
                "content": m.content,
                "memory_origin": m.memory_origin,
                "paper_ids": json.loads(m.paper_ids) if m.paper_ids else []
            }
            for m in memories
        ]
