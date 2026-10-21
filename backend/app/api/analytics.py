from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.db.session import SessionLocal
from app.api.auth import get_current_user, get_optional_user
from app.models.user import User
from app.models.workspace import Project, Note, Bookmark, ResearchSearchEvent, PaperViewEvent
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SearchEventPayload(BaseModel):
    query: str
    search_mode: Optional[str] = "hybrid"
    domain: Optional[str] = None
    subdomain: Optional[str] = None
    result_count: Optional[int] = 0

class PaperViewPayload(BaseModel):
    paper_id: str

@router.post("/search")
def record_search_event(payload: SearchEventPayload, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_optional_user)):
    try:
        uid = current_user.id if current_user else "default_user"
        # Simple debounce / duplicate protection
        last_event = db.query(ResearchSearchEvent).filter(
            ResearchSearchEvent.user_id == uid
        ).order_by(desc(ResearchSearchEvent.searched_at)).first()
        
        if last_event and last_event.query == payload.query:
            if last_event.searched_at:
                time_diff = (datetime.utcnow() - last_event.searched_at.replace(tzinfo=None)).total_seconds()
                if time_diff < 5:
                    return {"status": "ignored_duplicate"}

        event = ResearchSearchEvent(
            user_id=uid,
            query=payload.query,
            search_mode=payload.search_mode,
            domain=payload.domain,
            subdomain=payload.subdomain,
            result_count=payload.result_count
        )
        db.add(event)
        db.commit()
        return {"status": "recorded"}
    except Exception as e:
        print(f"Analytics tracking failed: {e}")
        return {"status": "failed", "error": str(e)}

@router.post("/paper_view")
def record_paper_view(payload: PaperViewPayload, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_optional_user)):
    try:
        uid = current_user.id if current_user else "default_user"
        last_event = db.query(PaperViewEvent).filter(
            PaperViewEvent.user_id == uid,
            PaperViewEvent.paper_id == payload.paper_id
        ).order_by(desc(PaperViewEvent.viewed_at)).first()
        
        if last_event and last_event.viewed_at:
            time_diff = (datetime.utcnow() - last_event.viewed_at.replace(tzinfo=None)).total_seconds()
            if time_diff < 10:
                return {"status": "ignored_duplicate"}

        event = PaperViewEvent(
            user_id=uid,
            paper_id=payload.paper_id
        )
        db.add(event)
        db.commit()
        return {"status": "recorded"}
    except Exception as e:
        print(f"Analytics tracking failed: {e}")
        return {"status": "failed", "error": str(e)}

@router.get("/overview")
def get_analytics_overview(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    user_ids = [user_id]
    if user_id != "default_user":
        user_ids.append("default_user")
    
    searches_count = db.query(ResearchSearchEvent).filter(ResearchSearchEvent.user_id.in_(user_ids)).count()
    paper_views_count = db.query(PaperViewEvent).filter(PaperViewEvent.user_id.in_(user_ids)).count()
    bookmarks_count = db.query(Bookmark).filter(Bookmark.user_id == user_id).count()
    projects_count = db.query(Project).filter(Project.user_id == user_id).count()
    notes_count = db.query(Note).filter(Note.user_id == user_id).count()

    stats = [
        {'label': 'Research Sessions', 'value': str(searches_count)},
        {'label': 'Papers Opened', 'value': str(paper_views_count)},
        {'label': 'Papers Saved', 'value': str(bookmarks_count)},
        {'label': 'Active Projects', 'value': str(projects_count)}
    ]

    ALLOWED_DOMAINS = [
        "Artificial Intelligence", "Healthcare", "Data Science", 
        "Environmental Science", "Materials Science", 
        "Interdisciplinary Research", "Energy", "Space Science"
    ]
    domain_counts = db.query(
        ResearchSearchEvent.domain, func.count(ResearchSearchEvent.id)
    ).filter(
        ResearchSearchEvent.user_id.in_(user_ids),
        ResearchSearchEvent.domain.isnot(None)
    ).group_by(ResearchSearchEvent.domain).all()

    total_domain_searches = sum([count for d, count in domain_counts if d in ALLOWED_DOMAINS])
    domain_interest = []
    if total_domain_searches > 0:
        for domain_name, count in domain_counts:
            if domain_name in ALLOWED_DOMAINS:
                pct = int((count / total_domain_searches) * 100)
                domain_interest.append({"name": domain_name, "value": pct, "count": count})
        domain_interest.sort(key=lambda x: x["value"], reverse=True)

    timeline_events = []
    
    recent_searches = db.query(ResearchSearchEvent).filter(ResearchSearchEvent.user_id.in_(user_ids)).order_by(desc(ResearchSearchEvent.searched_at)).limit(5).all()
    for s in recent_searches:
        timeline_events.append({'action': 'Search', 'detail': f'Searched: "{s.query}"', 'time': s.searched_at})
        
    recent_views = db.query(PaperViewEvent).filter(PaperViewEvent.user_id.in_(user_ids)).order_by(desc(PaperViewEvent.viewed_at)).limit(5).all()
    for v in recent_views:
        timeline_events.append({'action': 'Paper Opened', 'detail': f'Viewed paper {v.paper_id[:8]}...', 'time': v.viewed_at})

    recent_bookmarks = db.query(Bookmark).filter(Bookmark.user_id == user_id).order_by(desc(Bookmark.created_at)).limit(5).all()
    for b in recent_bookmarks:
        timeline_events.append({'action': 'Paper Saved', 'detail': f'Saved paper {b.paper_id[:8]}...', 'time': b.created_at})
        
    recent_projects = db.query(Project).filter(Project.user_id == user_id).order_by(desc(Project.created_at)).limit(5).all()
    for p in recent_projects:
        timeline_events.append({'action': 'Project Created', 'detail': p.name, 'time': p.created_at})
        
    recent_notes = db.query(Note).filter(Note.user_id == user_id).order_by(desc(Note.created_at)).limit(5).all()
    for n in recent_notes:
        timeline_events.append({'action': 'Note Created', 'detail': (n.content[:30] + '...') if n.content else 'Empty note', 'time': n.created_at})

    timeline_events.sort(key=lambda x: x['time'].isoformat() if x['time'] else "", reverse=True)
    
    formatted_timeline = []
    for evt in timeline_events[:6]:
        formatted_timeline.append({
            'action': evt['action'],
            'detail': evt['detail'],
            'time': evt['time'].strftime("%Y-%m-%d %H:%M") if evt['time'] else "Unknown"
        })

    query_counts = db.query(
        ResearchSearchEvent.query, func.count(ResearchSearchEvent.id)
    ).filter(ResearchSearchEvent.user_id.in_(user_ids)).group_by(ResearchSearchEvent.query).order_by(desc(func.count(ResearchSearchEvent.id))).limit(5).all()
    
    insights = []
    for q, c in query_counts:
        insights.append({"name": q, "value": c})

    today = datetime.utcnow().date()
    activity = []
    
    # Always generate the last 7 days including today
    seven_days_ago = today - timedelta(days=6) # 7 days total including today
    
    date_map = {}
    for i in range(7):
        d = seven_days_ago + timedelta(days=i)
        date_map[d] = {"name": d.strftime("%a"), "Searches": 0, "Papers Opened": 0}
        
    recent_all_searches = db.query(ResearchSearchEvent.searched_at).filter(
        ResearchSearchEvent.user_id.in_(user_ids), 
        ResearchSearchEvent.searched_at >= seven_days_ago
    ).all()
    recent_all_views = db.query(PaperViewEvent.viewed_at).filter(
        PaperViewEvent.user_id.in_(user_ids), 
        PaperViewEvent.viewed_at >= seven_days_ago
    ).all()
    
    for (dt,) in recent_all_searches:
        if dt:
            d = dt.date()
            if d in date_map:
                date_map[d]["Searches"] += 1
                
    for (dt,) in recent_all_views:
        if dt:
            d = dt.date()
            if d in date_map:
                date_map[d]["Papers Opened"] += 1
                
    for d in sorted(date_map.keys()):
        activity.append(date_map[d])
            
    return {
        "stats": stats,
        "domain_interest": domain_interest,
        "timeline": formatted_timeline,
        "insights": insights,
        "activity": activity
    }
