from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.workspace import Note
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

class NoteCreate(BaseModel):
    content: str
    project_id: Optional[str] = None
    paper_id: Optional[str] = None

class NoteUpdate(BaseModel):
    content: Optional[str] = None

@router.get("/")
def get_notes(project_id: Optional[str] = None, paper_id: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Note).filter(Note.user_id == current_user.id)
    if project_id:
        query = query.filter(Note.project_id == project_id)
    if paper_id:
        query = query.filter(Note.paper_id == paper_id)
        
    notes = query.order_by(desc(Note.updated_at)).all()
    return notes

from app.models.workspace import Project
from app.models.paper import Paper

@router.post("/")
def create_note(note_in: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if note_in.project_id:
        project = db.query(Project).filter(Project.id == note_in.project_id, Project.user_id == current_user.id).first()
        if not project:
            raise HTTPException(status_code=403, detail="Project not found or not authorized")
            
    if note_in.paper_id:
        paper = db.query(Paper).filter(Paper.id == note_in.paper_id).first()
        if not paper:
            paper = Paper(
                id=note_in.paper_id,
                title=f"Paper {note_in.paper_id[:16]}",
                authors="Unknown Authors",
                abstract=""
            )
            db.add(paper)
            db.flush()

    new_note = Note(
        user_id=current_user.id,
        content=note_in.content,
        project_id=note_in.project_id,
        paper_id=note_in.paper_id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.put("/{note_id}")
def update_note(note_id: str, note_in: NoteUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if note_in.content is not None:
        note.content = note_in.content
        
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}")
def delete_note(note_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    db.delete(note)
    db.commit()
    return {"status": "success", "message": "Note deleted"}
