from sqlalchemy import Column, String, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.user import generate_uuid

class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    notes = relationship("Note", back_populates="project")
    papers = relationship("ProjectPaper", back_populates="project")

class Note(Base):
    __tablename__ = "notes"
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    paper_id = Column(String, ForeignKey("papers.id"), nullable=True)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    project = relationship("Project", back_populates="notes")


class ProjectPaper(Base):
    __tablename__ = "project_papers"
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    paper_id = Column(String, ForeignKey("papers.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint('project_id', 'paper_id', name='uq_project_paper'),
    )
    
    project = relationship("Project", back_populates="papers")
    paper = relationship("Paper")

class Bookmark(Base):
    __tablename__ = "bookmarks"
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    paper_id = Column(String, ForeignKey("papers.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    session_id = Column(String, index=True) # Link to frontend session if needed
    message_log = Column(Text) # JSON string of the chat history
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ResearchGoal(Base):
    __tablename__ = "research_goals"
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    due_date = Column(String)
    priority = Column(String, default="medium") # low, medium, high
    status = Column(String, default="not_started") # not_started, in_progress, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

from sqlalchemy import Integer

class ResearchSearchEvent(Base):
    __tablename__ = "research_search_events"
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    query = Column(String, nullable=False)
    search_mode = Column(String)
    domain = Column(String)
    subdomain = Column(String)
    result_count = Column(Integer, default=0)
    searched_at = Column(DateTime(timezone=True), server_default=func.now())

class PaperViewEvent(Base):
    __tablename__ = "paper_view_events"
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    paper_id = Column(String, nullable=False)
    viewed_at = Column(DateTime(timezone=True), server_default=func.now())
