from sqlalchemy import text
from app.db.session import SessionLocal, engine

db = SessionLocal()
try:
    cols = [
        "keywords TEXT",
        "subdomain VARCHAR",
        "publication_year VARCHAR",
        "publication_date VARCHAR",
        "journal VARCHAR",
        "conference VARCHAR",
        "publisher VARCHAR",
        "doi VARCHAR",
        "source_repository VARCHAR",
        "source_id VARCHAR",
        "paper_url VARCHAR",
        "pdf_path VARCHAR",
        "read_source VARCHAR",
        "metadata_source VARCHAR"
    ]
    for col in cols:
        try:
            db.execute(text(f"ALTER TABLE papers ADD COLUMN {col};"))
            db.commit()
            print(f"Added {col}")
        except Exception as e:
            db.rollback()
            print(f"Skipped {col}: {e}")
            
    # Also recreate paper_chunks if needed, but create_all handles missing tables
except Exception as e:
    print(e)
finally:
    db.close()
