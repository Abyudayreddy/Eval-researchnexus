# backend/app/models/search_history.py

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean, text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.session import Base

import datetime

class SearchHistory(Base):
    __tablename__ = "search_history"

    history_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, default="default_user")  # Assuming simple string user_id for now
    search_id = Column(UUID(as_uuid=True), ForeignKey("search_experiments.search_id", ondelete="CASCADE"), nullable=False)
    query = Column(String, nullable=False)
    title = Column(String, nullable=True)
    
    result_count = Column(Integer, nullable=True, default=0)
    local_result_count = Column(Integer, nullable=True, default=0)
    online_result_count = Column(Integer, nullable=True, default=0)
    
    is_favorite = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    last_opened_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (UniqueConstraint('user_id', 'search_id', name='uq_user_search'),)
