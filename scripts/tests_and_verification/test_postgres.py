import os, sys
sys.path.insert(0, os.path.abspath('backend'))
os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@localhost:5432/researchnexus'
os.environ['GEMINI_API_KEY'] = 'dummy'

from app.db.session import SessionLocal
from app.models.paper import Paper

db = SessionLocal()
papers = db.query(Paper).filter(Paper.title.ilike('%Triple Barrier%')).all()
for p in papers:
    print(p.id, p.title)

papers2 = db.query(Paper).filter(Paper.title.ilike('%OHLCV%')).all()
for p in papers2:
    print(p.id, p.title)

db.close()
