import os, sys, asyncio
sys.path.insert(0, os.path.abspath('backend'))
os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@localhost:5432/researchnexus'
os.environ['GEMINI_API_KEY'] = 'dummy'

from app.api.papers import run_local_search
query2 = "Can raw OHLCV data with deep learning predict stock prices without technical indicators?"
res = run_local_search(query2, deep_evidence=False)
print("QUERY 2 LOCAL RESULT COUNT:", len(res[0]))
print("QUERY 2 STATUS:", res[1])
print("QUERY 2 TRACE:", res[2])
