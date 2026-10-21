import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class ResearchSession(Base):
    __tablename__ = "research_sessions"

    session_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False, default="default_user")
    title = Column(String, nullable=False, default="New Research Session")
    description = Column(Text, nullable=True)
    
    # Lifecycle: ACTIVE | PAUSED | COMPLETED | ARCHIVED
    status = Column(String, default="ACTIVE", index=True)
    deleted_at = Column(DateTime, nullable=True, index=True)  # Soft delete timestamp
    
    created_by = Column(String, default="researcher")
    metadata_json = Column(Text, nullable=True)  # Structured JSON string for extra settings
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    last_activity_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    artifacts = relationship("ResearchArtifact", back_populates="session", cascade="all, delete-orphan")
    memories = relationship("ResearchMemory", back_populates="session", cascade="all, delete-orphan")

class ResearchArtifact(Base):
    __tablename__ = "research_artifacts"

    artifact_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("research_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String, index=True, nullable=False, default="default_user")
    
    # Type: SEARCH | XAI | QUESTION | ANSWER | PAPER | EVIDENCE | COMPARISON | SYNTHESIS | GAP | FINDING | NOTE | DOCUMENT
    artifact_type = Column(String, nullable=False, index=True)
    artifact_ref = Column(String, nullable=False, index=True)  # Identifier of target object (search_id, paper_id, etc.)
    title = Column(String, nullable=False)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    session = relationship("ResearchSession", back_populates="artifacts")

class ResearchMemory(Base):
    __tablename__ = "research_memories"

    memory_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("research_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String, index=True, nullable=False, default="default_user")
    
    # Type: RESEARCH_GOAL | RESEARCH_CONSTRAINT | SELECTED_PAPER | KEY_FINDING | EVIDENCE_REFERENCE | RESEARCH_DECISION | OPEN_QUESTION | POTENTIAL_GAP | RESEARCH_NOTE
    memory_type = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    
    # Status: SUGGESTED | ACCEPTED | REJECTED | EDITED
    status = Column(String, default="ACCEPTED", index=True)
    
    # Origin: USER_RECORDED | EVIDENCE_DERIVED | AI_SUGGESTED
    memory_origin = Column(String, default="USER_RECORDED", index=True)
    
    # Provenance structured JSON arrays
    source_artifact_ids = Column(Text, nullable=True)  # JSON string array
    paper_ids = Column(Text, nullable=True)  # JSON string array
    evidence_ids = Column(Text, nullable=True)  # JSON string array
    
    version = Column(Integer, default=1)
    created_by = Column(String, default="user")
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    session = relationship("ResearchSession", back_populates="memories")
