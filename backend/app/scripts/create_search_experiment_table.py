# Migration script to create search_experiments table

import sqlalchemy as sa
from sqlalchemy import text
from app.db.session import engine

# Define table creation SQL – id UUID primary key, timestamps, JSON columns for metrics
create_sql = """
CREATE TABLE IF NOT EXISTS search_experiments (
    search_id UUID PRIMARY KEY,
    query TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    local_status TEXT,
    local_metrics JSONB,
    online_status TEXT,
    online_metrics JSONB,
    combined_metrics JSONB,
    local_trace JSONB,
    online_trace JSONB,
    combined_trace JSONB
);
"""

with engine.begin() as conn:
    conn.execute(text(create_sql))
    conn.commit()
