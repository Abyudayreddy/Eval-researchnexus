import os, sys
sys.path.insert(0, os.path.abspath('backend'))
os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@localhost:5432/researchnexus'

from app.services.local_evidence import get_local_retriever
retriever = get_local_retriever()

q = "Stock Price Prediction Using Triple Barrier Labeling"
b_res, b_lat = retriever.retrieve_bm25(q, top_k=50)
d_res, d_lat = retriever.retrieve_dense(q, top_k=50)

print(f"BM25 found {len(b_res)} candidates")
for b in b_res[:5]:
    print(" ", b)

print(f"Dense found {len(d_res)} candidates")
for d in d_res[:5]:
    print(" ", d)
