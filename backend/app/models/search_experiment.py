# backend/app/models/search_experiment.py

from sqlalchemy import Column, String, DateTime, JSON, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.session import Base

class SearchExperiment(Base):
    __tablename__ = "search_experiments"

    search_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query = Column(String, nullable=False)
    overall_status = Column(String, nullable=True)
    # Existing columns follow
    local_metrics = Column(JSON, nullable=True)
    online_status = Column(String, nullable=True)
    online_metrics = Column(JSON, nullable=True)
    combined_metrics = Column(JSON, nullable=True)
    local_trace = Column(JSON, nullable=True)
    online_trace = Column(JSON, nullable=True)
    combined_trace = Column(JSON, nullable=True)
    results = Column(JSON, nullable=True)
