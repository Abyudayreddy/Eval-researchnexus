from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.api.auth import get_current_user
from app.models.user import User
from app.models.workspace import Project, Note
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

@router.get("/")
def get_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = db.query(Project).filter(Project.user_id == current_user.id).all()
    return projects

@router.post("/")
def create_project(project_in: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_project = Project(
        user_id=current_user.id,
        name=project_in.name,
        description=project_in.description
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.put("/{project_id}")
def update_project(project_id: str, project_in: ProjectUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not authorized")
    
    if project_in.name is not None:
        project.name = project_in.name
    if project_in.description is not None:
        project.description = project_in.description
        
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}")
def delete_project(project_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not authorized")
    
    # Optional: Delete associated notes safely (if CASCADE is not configured)
    db.query(Note).filter(Note.project_id == project_id).delete()
    
    db.delete(project)
    db.commit()
    return {"status": "success", "message": "Project deleted"}

from app.models.workspace import ProjectPaper
from app.models.paper import Paper
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

@router.post("/{project_id}/papers")
def add_paper_to_project(project_id: str, payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 1. Verify project ownership
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not authorized")
        
    paper_id = payload.get("paper_id")
    if not paper_id:
        raise HTTPException(status_code=400, detail="paper_id is required")
        
    # 2. Check if paper exists, if not create it from metadata
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        paper = Paper(
            id=paper_id,
            title=payload.get("title", "Unknown Title"),
            authors=payload.get("authors", ""),
            abstract=payload.get("abstract", ""),
            url=payload.get("url", ""),
            # publish_date might need parsing if it exists, skipping for simplicity unless required
        )
        db.add(paper)
        db.flush()
        
    # 3. Create relationship
    try:
        proj_paper = ProjectPaper(project_id=project_id, paper_id=paper_id)
        db.add(proj_paper)
        db.commit()
    except IntegrityError:
        db.rollback()
        # Already exists
        return {"status": "success", "message": "Paper already in project"}
        
    return {"status": "success", "message": "Paper added to project"}

@router.delete("/{project_id}/papers/{paper_id:path}")
def remove_paper_from_project(project_id: str, paper_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not authorized")
        
    proj_paper = db.query(ProjectPaper).filter(ProjectPaper.project_id == project_id, ProjectPaper.paper_id == paper_id).first()
    if not proj_paper:
        raise HTTPException(status_code=404, detail="Paper not found in project")
        
    db.delete(proj_paper)
    db.commit()
    return {"status": "success", "message": "Paper removed from project"}

@router.get("/{project_id}/papers")
def get_project_papers(project_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not authorized")
        
    proj_papers = db.query(ProjectPaper).filter(ProjectPaper.project_id == project_id).order_by(desc(ProjectPaper.created_at)).all()
    results = []
    for pp in proj_papers:
        paper = db.query(Paper).filter(Paper.id == pp.paper_id).first()
        if paper:
            results.append({
                "id": pp.id,
                "project_id": pp.project_id,
                "paper_id": pp.paper_id,
                "created_at": pp.created_at,
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

@router.get("/{project_id}/notes")
def get_project_notes(project_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not authorized")
        
    notes = db.query(Note).filter(Note.project_id == project_id, Note.user_id == current_user.id).order_by(desc(Note.updated_at)).all()
    return notes
