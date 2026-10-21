from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.workspace import Bookmark
from app.models.paper import Paper
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class PaperCreate(BaseModel):
    id: str
    title: str
    authors: str
    abstract: Optional[str] = None
    url: Optional[str] = None
    published: Optional[str] = None
    domain: Optional[str] = None

class BookmarkCreate(BaseModel):
    paper: PaperCreate

@router.post("/")
async def add_bookmark(bookmark_data: BookmarkCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 1. Check if paper exists, if not create it
    paper = db.query(Paper).filter(Paper.id == bookmark_data.paper.id).first()
    if not paper:
        pub_date = None
        if bookmark_data.paper.published:
            try:
                pub_date = datetime.fromisoformat(bookmark_data.paper.published.replace('Z', '+00:00'))
            except ValueError:
                pass
                
        paper = Paper(
            id=bookmark_data.paper.id,
            title=bookmark_data.paper.title,
            authors=bookmark_data.paper.authors,
            abstract=bookmark_data.paper.abstract,
            url=bookmark_data.paper.url,
            publish_date=pub_date
        )
        db.add(paper)
        db.flush()

    # 2. Check if bookmark already exists
    existing = db.query(Bookmark).filter(Bookmark.user_id == current_user.id, Bookmark.paper_id == paper.id).first()
    if existing:
        return {"message": "Already bookmarked", "id": existing.id}

    # 3. Create bookmark
    new_bookmark = Bookmark(user_id=current_user.id, paper_id=paper.id)
    db.add(new_bookmark)
    db.commit()
    db.refresh(new_bookmark)
    
    return {"message": "Bookmark added", "id": new_bookmark.id}

@router.get("/")
async def get_bookmarks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bookmarks = db.query(Bookmark).filter(Bookmark.user_id == current_user.id).order_by(desc(Bookmark.created_at)).all()
    
    results = []
    for b in bookmarks:
        paper = db.query(Paper).filter(Paper.id == b.paper_id).first()
        if paper:
            results.append({
                "id": b.id,
                "paper_id": b.paper_id,
                "created_at": b.created_at,
                "paper": {
                    "id": paper.id,
                    "title": paper.title,
                    "authors": paper.authors,
                    "abstract": paper.abstract,
                    "url": paper.url,
                    "published": paper.publish_date.isoformat() if paper.publish_date else None
                }
            })
    return results

@router.delete("/{paper_id:path}")
async def remove_bookmark(paper_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bookmark = db.query(Bookmark).filter(Bookmark.user_id == current_user.id, Bookmark.paper_id == paper_id).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
        
    db.delete(bookmark)
    db.commit()
    return {"message": "Bookmark removed"}
