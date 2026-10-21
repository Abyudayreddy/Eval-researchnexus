import os, sys
sys.path.insert(0, os.path.abspath('backend'))
os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@localhost:5432/researchnexus'

from app.services.local_evidence import get_local_retriever
r = get_local_retriever()
print("INIT STATUS:", r.init_status)
