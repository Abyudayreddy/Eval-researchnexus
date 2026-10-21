import uuid
import json
import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.session import ResearchArtifact, ResearchSession

VALID_ARTIFACT_TYPES = [
    "SEARCH",
    "XAI",
    "QUESTION",
    "ANSWER",
    "PAPER",
    "EVIDENCE",
    "COMPARISON",
    "SYNTHESIS",
    "GAP",
    "FINDING",
    "NOTE",
    "DOCUMENT"
]

class ResearchArtifactService:
    @staticmethod
    def register_artifact(
        db: Session,
        session_id: str,
        artifact_type: str,
        artifact_ref: str,
        title: str,
        user_id: str = "default_user",
        metadata: Optional[Dict[str, Any]] = None
    ) -> ResearchArtifact:
        if artifact_type not in VALID_ARTIFACT_TYPES:
            artifact_type = "NOTE"

        artifact_id = f"art_{uuid.uuid4().hex[:12]}"
        art = ResearchArtifact(
            artifact_id=artifact_id,
            session_id=session_id,
            user_id=user_id,
            artifact_type=artifact_type,
            artifact_ref=artifact_ref,
            title=title,
            metadata_json=json.dumps(metadata) if metadata else None
        )
        db.add(art)

        # Update last activity timestamp on session
        session = db.query(ResearchSession).filter(ResearchSession.session_id == session_id).first()
        if session:
            session.last_activity_at = datetime.datetime.utcnow()

        db.commit()
        db.refresh(art)
        return art

    @staticmethod
    def get_session_activity_timeline(db: Session, session_id: str, user_id: str = "default_user", limit: int = 30) -> List[Dict[str, Any]]:
        artifacts = db.query(ResearchArtifact).filter(
            ResearchArtifact.session_id == session_id,
            ResearchArtifact.user_id == user_id
        ).order_by(ResearchArtifact.created_at.desc()).limit(limit).all()

        return [
            {
                "artifact_id": a.artifact_id,
                "artifact_type": a.artifact_type,
                "artifact_ref": a.artifact_ref,
                "title": a.title,
                "created_at": a.created_at.isoformat() if a.created_at else None,
                "metadata": json.loads(a.metadata_json) if a.metadata_json else {}
            }
            for a in artifacts
        ]
