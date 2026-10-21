import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))
from app.services.local_evidence import get_local_retriever

def main():
    retriever = get_local_retriever()
    retriever.load()
    query = "Stock Price Prediction Using Triple Barrier Labeling"
    bm25_res, _ = retriever.retrieve_bm25(query, top_k=50)
    
    found = False
    for i, r in enumerate(bm25_res):
        if r['paper_id'] == '2504.02249v2':
            print(f"FOUND at rank {r['rank']} with score {r['score']}")
            found = True
            
    if not found:
        print("Paper 2504.02249v2 NOT found in top 50 of BM25!")
        
if __name__ == "__main__":
    main()
