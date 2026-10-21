from fastapi import APIRouter
from app.api import auth, dashboard, papers, ai, projects, notes, bookmarks, knowledge_base, analytics, goals, literature_review, search_history, documents, research, evaluation, toolkit

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(papers.router, prefix="/papers", tags=["papers"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(bookmarks.router, prefix="/bookmarks", tags=["bookmarks"])
api_router.include_router(knowledge_base.router, prefix="/knowledge-base", tags=["knowledge_base"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
api_router.include_router(literature_review.router, prefix="/literature-review", tags=["literature-review"])
api_router.include_router(search_history.router, prefix="/history", tags=["history"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(research.router, prefix="/research", tags=["research"])
api_router.include_router(evaluation.router, prefix="/evaluation", tags=["evaluation"])
api_router.include_router(toolkit.router, prefix="/toolkit", tags=["toolkit"])
