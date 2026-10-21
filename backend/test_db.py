from app.db.session import SessionLocal
from app.models.paper import Paper, PaperChunk

db = SessionLocal()
try:
    print(f"Papers count: {db.query(Paper).count()}")
    print(f"Chunks count: {db.query(PaperChunk).count()}")
finally:
    db.close()
