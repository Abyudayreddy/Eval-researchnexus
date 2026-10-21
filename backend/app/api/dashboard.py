from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import SessionLocal
from app.api.auth import get_current_user
from app.models.user import User
from app.models.workspace import Project, Note, Bookmark, Conversation, ResearchSearchEvent
from app.models.paper import Paper
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    user_ids = [user_id]
    if user_id != "default_user":
        user_ids.append("default_user")
    
    # 1. Analytics Stats
    searches_count = db.query(ResearchSearchEvent).filter(ResearchSearchEvent.user_id.in_(user_ids)).count()
    conv_count = db.query(Conversation).filter(Conversation.user_id == user_id).count()
    sessions_count = searches_count + conv_count
    bookmarks_count = db.query(Bookmark).filter(Bookmark.user_id == user_id).count()
    notes_count = db.query(Note).filter(Note.user_id == user_id).count()
    projects_count = db.query(Project).filter(Project.user_id == user_id).count()
    
    research_stats = [
        {'label': 'Research Sessions', 'value': str(sessions_count)},
        {'label': 'Papers Saved', 'value': str(bookmarks_count)},
        {'label': 'Notes Created', 'value': str(notes_count)},
        {'label': 'Projects', 'value': str(projects_count)},
    ]
    
    # 2. Active Projects
    projects = db.query(Project).filter(Project.user_id == user_id).order_by(desc(Project.updated_at)).limit(4).all()
    active_projects = []
    for p in projects:
        notes_in_proj = db.query(Note).filter(Note.project_id == p.id).count()
        active_projects.append({
            'id': p.id,
            'name': p.name,
            'progress': 0, # Placeholder until task tracking is added
            'notes': notes_in_proj,
            'lastActivity': p.updated_at.strftime("%Y-%m-%d %H:%M") if p.updated_at else (p.created_at.strftime("%Y-%m-%d %H:%M") if p.created_at else "Unknown")
        })
        
    # 3. Recent Papers (Bookmarks)
    bookmarks = db.query(Bookmark).filter(Bookmark.user_id == user_id).order_by(desc(Bookmark.created_at)).limit(4).all()
    recent_papers = []
    for b in bookmarks:
        paper = db.query(Paper).filter(Paper.id == b.paper_id).first()
        if paper:
            recent_papers.append({
                'id': paper.id,
                'title': paper.title,
                'authors': paper.authors or 'Unknown',
                'publication': paper.publish_date.strftime("%Y") if getattr(paper, 'publish_date', None) else 'Unknown',
                'domain': paper.domain_id,
                'abstract': paper.abstract
            })

    # 4. Continue Research (Recent Projects)
    # The user approved displaying projects/conversations chronologically without forcing a domain grouping.
    continue_research = []
    for p in projects:
        continue_research.append({
            'id': p.id,
            'title': p.name,
            'type': 'Project',
            'updatedAt': p.updated_at.isoformat() if p.updated_at else (p.created_at.isoformat() if p.created_at else datetime.utcnow().isoformat())
        })
    # If we had conversations, we'd union them here and sort chronologically.
    
    # 5. Recent Activity Timeline (Dynamic)
    timeline_events = []
    
    # Get recent projects
    for p in projects:
        timeline_events.append({
            'action': 'Created Project',
            'detail': f'Started project: {p.name}',
            'timestamp': p.created_at
        })
        
    # Get recent bookmarks
    for b in bookmarks:
        paper = db.query(Paper).filter(Paper.id == b.paper_id).first()
        title = paper.title if paper else "Unknown Paper"
        timeline_events.append({
            'action': 'Saved Paper',
            'detail': f'Bookmarked: {title[:50]}...',
            'timestamp': b.created_at
        })
        
    # Get recent notes
    notes = db.query(Note).filter(Note.user_id == user_id).order_by(desc(Note.created_at)).limit(5).all()
    for n in notes:
        content_preview = (n.content[:40] + "...") if n.content and len(n.content) > 40 else (n.content or "Empty note")
        timeline_events.append({
            'action': 'Added Note',
            'detail': content_preview,
            'timestamp': n.created_at
        })
        
    # Sort all events chronologically (newest first)
    timeline_events.sort(key=lambda x: x['timestamp'].isoformat() if x['timestamp'] else "", reverse=True)
    
    # Format for frontend
    formatted_timeline = []
    for event in timeline_events[:5]: # Take top 5 recent events
        time_str = event['timestamp'].strftime("%Y-%m-%d %H:%M") if event['timestamp'] else "Unknown time"
        formatted_timeline.append({
            'action': event['action'],
            'detail': event['detail'],
            'time': time_str
        })

    return {
        "stats": research_stats,
        "activeProjects": active_projects,
        "recentPapers": recent_papers,
        "continueResearch": continue_research,
        "recentTimeline": formatted_timeline
    }
