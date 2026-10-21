import uuid
import json
import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.session import ResearchSession, ResearchArtifact, ResearchMemory

class ResearchSessionService:
    @staticmethod
    def create_session(
        db: Session,
        title: Optional[str] = None,
        description: Optional[str] = None,
        user_id: str = "default_user",
        initial_goal: Optional[str] = None
    ) -> ResearchSession:
        session_id = f"session_{uuid.uuid4().hex[:12]}"
        default_title = title or "New Research Session"

        session = ResearchSession(
            session_id=session_id,
            user_id=user_id,
            title=default_title,
            description=description or "Scientific investigation workspace.",
            status="ACTIVE",
            created_by="researcher"
        )
        db.add(session)
        db.commit()
        db.refresh(session)

        # If an initial goal was specified, create an initial RESEARCH_GOAL memory
        if initial_goal:
            from app.services.research_memory_service import ResearchMemoryService
            ResearchMemoryService.create_memory(
                db=db,
                session_id=session_id,
                user_id=user_id,
                memory_type="RESEARCH_GOAL",
                content=initial_goal,
                memory_origin="USER_RECORDED"
            )

        return session

    @staticmethod
    def list_user_sessions(
        db: Session,
        user_id: str = "default_user",
        include_archived: bool = True
    ) -> List[Dict[str, Any]]:
        query = db.query(ResearchSession).filter(
            ResearchSession.user_id == user_id,
            ResearchSession.deleted_at.is_(None)
        )
        if not include_archived:
            query = query.filter(ResearchSession.status != "ARCHIVED")

        sessions = query.order_by(ResearchSession.last_activity_at.desc()).all()

        results = []
        for s in sessions:
            paper_count = db.query(ResearchArtifact).filter(
                ResearchArtifact.session_id == s.session_id,
                ResearchArtifact.artifact_type == "PAPER"
            ).count()

            finding_count = db.query(ResearchMemory).filter(
                ResearchMemory.session_id == s.session_id,
                ResearchMemory.memory_type == "KEY_FINDING",
                ResearchMemory.status == "ACCEPTED"
            ).count()

            results.append({
                "session_id": s.session_id,
                "title": s.title,
                "description": s.description,
                "status": s.status,
                "paper_count": paper_count,
                "finding_count": finding_count,
                "last_activity_at": s.last_activity_at.isoformat() if s.last_activity_at else None,
                "created_at": s.created_at.isoformat() if s.created_at else None
            })

        return results

    @staticmethod
    def get_session_details(db: Session, session_id: str, user_id: str = "default_user") -> Dict[str, Any]:
        session = db.query(ResearchSession).filter(
            ResearchSession.session_id == session_id,
            ResearchSession.user_id == user_id,
            ResearchSession.deleted_at.is_(None)
        ).first()

        if not session:
            raise ValueError("SESSION_NOT_FOUND")

        artifacts = db.query(ResearchArtifact).filter(ResearchArtifact.session_id == session_id).all()
        memories = db.query(ResearchMemory).filter(
            ResearchMemory.session_id == session_id,
            ResearchMemory.status.in_(["ACCEPTED", "SUGGESTED"])
        ).all()

        paper_artifacts = [a for a in artifacts if a.artifact_type == "PAPER"]
        evidence_artifacts = [a for a in artifacts if a.artifact_type == "EVIDENCE"]
        question_artifacts = [a for a in artifacts if a.artifact_type == "QUESTION"]
        comparison_artifacts = [a for a in artifacts if a.artifact_type == "COMPARISON"]
        synthesis_artifacts = [a for a in artifacts if a.artifact_type == "SYNTHESIS"]

        return {
            "session_id": session.session_id,
            "title": session.title,
            "description": session.description,
            "status": session.status,
            "created_at": session.created_at.isoformat() if session.created_at else None,
            "last_activity_at": session.last_activity_at.isoformat() if session.last_activity_at else None,
            "stats": {
                "paper_count": len(paper_artifacts),
                "evidence_count": len(evidence_artifacts),
                "question_count": len(question_artifacts),
                "finding_count": len([m for m in memories if m.memory_type == "KEY_FINDING"]),
                "comparison_count": len(comparison_artifacts),
                "synthesis_count": len(synthesis_artifacts),
                "memory_count": len(memories)
            },
            "artifacts": [
                {
                    "artifact_id": a.artifact_id,
                    "artifact_type": a.artifact_type,
                    "artifact_ref": a.artifact_ref,
                    "title": a.title,
                    "created_at": a.created_at.isoformat() if a.created_at else None
                }
                for a in artifacts
            ],
            "memories": [
                {
                    "memory_id": m.memory_id,
                    "memory_type": m.memory_type,
                    "content": m.content,
                    "status": m.status,
                    "memory_origin": m.memory_origin,
                    "paper_ids": json.loads(m.paper_ids) if m.paper_ids else [],
                    "evidence_ids": json.loads(m.evidence_ids) if m.evidence_ids else [],
                    "created_at": m.created_at.isoformat() if m.created_at else None
                }
                for m in memories
            ]
        }

    @staticmethod
    def update_session(
        db: Session,
        session_id: str,
        user_id: str = "default_user",
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None
    ) -> ResearchSession:
        session = db.query(ResearchSession).filter(
            ResearchSession.session_id == session_id,
            ResearchSession.user_id == user_id,
            ResearchSession.deleted_at.is_(None)
        ).first()

        if not session:
            raise ValueError("SESSION_NOT_FOUND")

        if title:
            session.title = title
        if description:
            session.description = description
        if status in ["ACTIVE", "PAUSED", "COMPLETED", "ARCHIVED"]:
            session.status = status

        session.last_activity_at = datetime.datetime.utcnow()
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def soft_delete_session(db: Session, session_id: str, user_id: str = "default_user") -> bool:
        session = db.query(ResearchSession).filter(
            ResearchSession.session_id == session_id,
            ResearchSession.user_id == user_id
        ).first()

        if not session:
            return False

        session.deleted_at = datetime.datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def export_session_package(db: Session, session_id: str, user_id: str = "default_user") -> Dict[str, Any]:
        details = ResearchSessionService.get_session_details(db, session_id, user_id)
        return {
            "reproducibility_export_version": "v1.0",
            "export_timestamp": datetime.datetime.utcnow().isoformat(),
            "session": details
        }
