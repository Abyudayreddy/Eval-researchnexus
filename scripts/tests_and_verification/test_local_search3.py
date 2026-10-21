import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/researchnexus"
os.environ["GEMINI_API_KEY"] = "dummy"

from app.services.local_evidence import get_local_retriever

def main():
    retriever = get_local_retriever()
    query = "Stock Price Prediction Using Triple Barrier Labeling Raw OHLCV"
    
    candidates, l_bm25, l_dense, l_rrf = retriever.retrieve_hybrid_rrf(query, top_k=200)
    print("Candidates count:", len(candidates))
    found = False
    for c in candidates:
        if '2504.02249v2' in c['chunk_id']:
            print("FOUND IN HYBRID WITH OHLCV:", c)
            found = True
            
    if not found:
        print("Paper 2504.02249v2 NOT found in top 200 candidates WITH OHLCV!")

if __name__ == "__main__":
    main()
