from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.research_session_service import ResearchSessionService
from app.services.research_memory_service import ResearchMemoryService
from app.services.research_artifact_service import ResearchArtifactService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CreateSessionRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    initial_goal: Optional[str] = None

class UpdateSessionRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class CreateMemoryRequest(BaseModel):
    content: str
    memory_type: str = "KEY_FINDING"
    memory_origin: str = "USER_RECORDED"
    paper_ids: Optional[List[str]] = None
    evidence_ids: Optional[List[str]] = None

class UpdateMemoryRequest(BaseModel):
    status: Optional[str] = None
    content: Optional[str] = None

@router.post("/sessions")
async def create_session(request: CreateSessionRequest, user_id: str = "default_user", db: Session = Depends(get_db)):
    session = ResearchSessionService.create_session(
        db=db,
        title=request.title,
        description=request.description,
        user_id=user_id,
        initial_goal=request.initial_goal
    )
    return {"session_id": session.session_id, "title": session.title, "status": session.status}

@router.get("/sessions")
async def list_sessions(include_archived: bool = True, user_id: str = "default_user", db: Session = Depends(get_db)):
    return ResearchSessionService.list_user_sessions(db, user_id=user_id, include_archived=include_archived)

@router.get("/sessions/{session_id}")
async def get_session(session_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    try:
        return ResearchSessionService.get_session_details(db, session_id=session_id, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/sessions/{session_id}")
async def update_session(session_id: str, request: UpdateSessionRequest, user_id: str = "default_user", db: Session = Depends(get_db)):
    try:
        session = ResearchSessionService.update_session(
            db=db,
            session_id=session_id,
            user_id=user_id,
            title=request.title,
            description=request.description,
            status=request.status
        )
        return {"session_id": session.session_id, "title": session.title, "status": session.status}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/sessions/{session_id}")
async def soft_delete_session(session_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    success = ResearchSessionService.soft_delete_session(db, session_id=session_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="SESSION_NOT_FOUND")
    return {"status": "DELETED", "session_id": session_id}

@router.post("/sessions/{session_id}/archive")
async def archive_session(session_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    try:
        session = ResearchSessionService.update_session(db, session_id, user_id, status="ARCHIVED")
        return {"session_id": session.session_id, "status": session.status}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/sessions/{session_id}/restore")
async def restore_session(session_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    try:
        session = ResearchSessionService.update_session(db, session_id, user_id, status="ACTIVE")
        return {"session_id": session.session_id, "status": session.status}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/sessions/{session_id}/activity")
async def get_session_activity(session_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    return ResearchArtifactService.get_session_activity_timeline(db, session_id, user_id)

@router.get("/sessions/{session_id}/memories")
async def get_session_memories(session_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    return ResearchMemoryService.get_eligible_memories_for_prompt(db, session_id, user_id)

@router.post("/sessions/{session_id}/memories")
async def add_session_memory(session_id: str, request: CreateMemoryRequest, user_id: str = "default_user", db: Session = Depends(get_db)):
    mem = ResearchMemoryService.create_memory(
        db=db,
        session_id=session_id,
        user_id=user_id,
        content=request.content,
        memory_type=request.memory_type,
        memory_origin=request.memory_origin,
        paper_ids=request.paper_ids,
        evidence_ids=request.evidence_ids
    )
    return {"memory_id": mem.memory_id, "memory_type": mem.memory_type, "status": mem.status}

@router.patch("/memories/{memory_id}")
async def update_memory(memory_id: str, request: UpdateMemoryRequest, user_id: str = "default_user", db: Session = Depends(get_db)):
    try:
        if request.content:
            mem = ResearchMemoryService.edit_memory_content(db, memory_id, request.content, user_id)
        elif request.status:
            mem = ResearchMemoryService.update_memory_status(db, memory_id, request.status, user_id)
        else:
            raise HTTPException(status_code=400, detail="INVALID_UPDATE_PAYLOAD")

        return {"memory_id": mem.memory_id, "status": mem.status, "content": mem.content}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/memories/{memory_id}")
async def delete_memory(memory_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    success = ResearchMemoryService.delete_memory(db, memory_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="MEMORY_NOT_FOUND")
    return {"status": "DELETED", "memory_id": memory_id}

@router.get("/sessions/{session_id}/export")
async def export_session(session_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    try:
        return ResearchSessionService.export_session_package(db, session_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
