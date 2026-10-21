import os, sys
sys.path.insert(0, os.path.abspath('backend'))
os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@localhost:5432/researchnexus'
os.environ['GEMINI_API_KEY'] = 'dummy'

from app.services.local_evidence import get_local_retriever
retriever = get_local_retriever()
q = "Stock Price Prediction Using Triple Barrier Labeling"
evidence, is_sufficient, trace = retriever.retrieve(q, deep_evidence=False)
print("EVIDENCE COUNT:", len(evidence))
print("TRACE:", trace)
