import os, sys, asyncio
sys.path.insert(0, os.path.abspath('backend'))
os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@localhost:5432/researchnexus'
os.environ['GEMINI_API_KEY'] = 'dummy'

from app.api.papers import run_local_search
query = "Stock Price Prediction Using Triple Barrier Labeling"
res = run_local_search(query, deep_evidence=True)
print("DEEP EVIDENCE COUNT:", len(res[0]))
