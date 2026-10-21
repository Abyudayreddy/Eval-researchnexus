from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.search_history import SearchHistory
from app.models.search_experiment import SearchExperiment
from pydantic import BaseModel, UUID4
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SearchHistoryResponse(BaseModel):
    history_id: UUID4
    search_id: UUID4
    query: str
    title: Optional[str] = None
    result_count: int
    local_result_count: int
    online_result_count: int
    is_favorite: bool
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

from app.api.auth import get_optional_user
from app.models.user import User

@router.get("/", response_model=List[SearchHistoryResponse])
def get_search_history(user_id: Optional[str] = None, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_optional_user)):
    target_user_id = user_id or (current_user.id if current_user else "default_user")
    history = db.query(SearchHistory).filter(
        (SearchHistory.user_id == target_user_id) | (SearchHistory.user_id == "default_user")
    ).order_by(SearchHistory.created_at.desc()).all()
    
    seen = set()
    results = []
    for h in history:
        if h.history_id not in seen:
            seen.add(h.history_id)
            results.append({
                "history_id": h.history_id,
                "search_id": h.search_id,
                "query": h.query,
                "title": h.title,
                "result_count": h.result_count or 0,
                "local_result_count": h.local_result_count or 0,
                "online_result_count": h.online_result_count or 0,
                "is_favorite": h.is_favorite,
                "created_at": h.created_at.isoformat() if h.created_at else "",
                "updated_at": h.updated_at.isoformat() if h.updated_at else ""
            })
    return results

@router.delete("/{history_id}")
def delete_history(history_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    try:
        uid = uuid.UUID(history_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid history_id")
        
    record = db.query(SearchHistory).filter(SearchHistory.history_id == uid, SearchHistory.user_id == user_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="History not found")
        
    db.delete(record)
    db.commit()
    return {"status": "success"}

@router.patch("/{history_id}")
def update_history(history_id: str, updates: dict, user_id: str = "default_user", db: Session = Depends(get_db)):
    try:
        uid = uuid.UUID(history_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid history_id")
        
    record = db.query(SearchHistory).filter(SearchHistory.history_id == uid, SearchHistory.user_id == user_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="History not found")
        
    if "title" in updates:
        record.title = updates["title"]
    if "is_favorite" in updates:
        record.is_favorite = updates["is_favorite"]
        
    db.commit()
    db.refresh(record)
    return record
