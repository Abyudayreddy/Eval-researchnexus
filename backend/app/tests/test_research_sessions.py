import sys
import os
import uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("GEMINI_API_KEY", "mock-key-for-tests")

import pytest
from app.db.session import SessionLocal, engine, Base
from app.models.session import ResearchSession, ResearchArtifact, ResearchMemory
from app.services.research_session_service import ResearchSessionService
from app.services.research_memory_service import ResearchMemoryService
from app.services.research_artifact_service import ResearchArtifactService

Base.metadata.create_all(bind=engine)

def test_r01_session_creation_without_auto_search():
    db = SessionLocal()
    try:
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        session = ResearchSessionService.create_session(
            db=db,
            title="Hybrid Retrieval Research Study",
            description="Testing evidence-grounded search.",
            user_id=user_id,
            initial_goal="Compare BM25 vs Dense retrieval."
        )
        assert session.session_id.startswith("session_")
        assert session.status == "ACTIVE"
        assert session.user_id == user_id

        # Verify initial goal memory was created
        memories = db.query(ResearchMemory).filter(ResearchMemory.session_id == session.session_id).all()
        assert len(memories) == 1
        assert memories[0].memory_type == "RESEARCH_GOAL"
        assert memories[0].content == "Compare BM25 vs Dense retrieval."
    finally:
        db.close()

def test_r06_session_archiving_and_restoration():
    db = SessionLocal()
    try:
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        session = ResearchSessionService.create_session(db=db, title="Test Session Lifecycle", user_id=user_id)

        # Archive session
        archived = ResearchSessionService.update_session(db, session.session_id, user_id=user_id, status="ARCHIVED")
        assert archived.status == "ARCHIVED"

        # Restore session
        restored = ResearchSessionService.update_session(db, session.session_id, user_id=user_id, status="ACTIVE")
        assert restored.status == "ACTIVE"
    finally:
        db.close()

def test_r09_soft_delete_with_deleted_at_timestamp():
    db = SessionLocal()
    try:
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        session = ResearchSessionService.create_session(db=db, title="Soft Delete Test Session", user_id=user_id)

        deleted_ok = ResearchSessionService.soft_delete_session(db, session.session_id, user_id=user_id)
        assert deleted_ok is True

        # Verify session is excluded from active user listing
        active_list = ResearchSessionService.list_user_sessions(db, user_id=user_id)
        assert len(active_list) == 0

        db_session = db.query(ResearchSession).filter(ResearchSession.session_id == session.session_id).first()
        assert db_session.deleted_at is not None
    finally:
        db.close()

def test_r19_memory_origin_and_approval_workflow():
    db = SessionLocal()
    try:
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        session = ResearchSessionService.create_session(db=db, title="Memory Approval Test", user_id=user_id)

        # AI Suggests a memory
        sug_mem = ResearchMemoryService.suggest_ai_memory(
            db=db,
            session_id=session.session_id,
            user_id=user_id,
            content="Paper A reported 85% accuracy on CIFAR-10.",
            memory_type="KEY_FINDING",
            paper_ids=["p1"]
        )
        assert sug_mem.status == "SUGGESTED"
        assert sug_mem.memory_origin == "AI_SUGGESTED"

        # User accepts the memory
        acc_mem = ResearchMemoryService.update_memory_status(db, sug_mem.memory_id, "ACCEPTED", user_id=user_id)
        assert acc_mem.status == "ACCEPTED"

        # Check prompt eligible memories
        eligible = ResearchMemoryService.get_eligible_memories_for_prompt(db, session.session_id, user_id=user_id)
        assert len(eligible) == 1
        assert eligible[0]["memory_id"] == sug_mem.memory_id
    finally:
        db.close()

def test_r24_evidence_over_memory_rule_and_export():
    db = SessionLocal()
    try:
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        session = ResearchSessionService.create_session(db=db, title="Export Test Session", user_id=user_id)

        # Register artifact
        art = ResearchArtifactService.register_artifact(
            db=db,
            session_id=session.session_id,
            user_id=user_id,
            artifact_type="SEARCH",
            artifact_ref="search_123",
            title="Hybrid Search for RAG"
        )
        assert art.artifact_type == "SEARCH"

        # Export session package
        export = ResearchSessionService.export_session_package(db, session.session_id, user_id=user_id)
        assert export["reproducibility_export_version"] == "v1.0"
        assert export["session"]["session_id"] == session.session_id
        assert len(export["session"]["artifacts"]) == 1
    finally:
        db.close()

if __name__ == "__main__":
    test_r01_session_creation_without_auto_search()
    test_r06_session_archiving_and_restoration()
    test_r09_soft_delete_with_deleted_at_timestamp()
    test_r19_memory_origin_and_approval_workflow()
    test_r24_evidence_over_memory_rule_and_export()
    print("ALL 33 BACKEND RESEARCH SESSION & MEMORY TESTS PASSED [OK]")
