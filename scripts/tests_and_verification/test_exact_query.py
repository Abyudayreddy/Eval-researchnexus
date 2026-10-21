import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))
from app.services.local_evidence import get_local_retriever

def main():
    retriever = get_local_retriever()
    query = "Stock Price Prediction Using Triple Barrier Labeling"
    
    candidates, l_bm25, l_dense, l_rrf = retriever.retrieve_hybrid_rrf(query, top_k=5)
    print("Candidates:", candidates)
    
    evidence, metadata_only, _ = retriever.rerank_and_build_evidence(query, candidates, use_reranker=False)
    
    print("\nEvidence:")
    for e in evidence:
        print(f"[{e['id']}] {e['title']}")
        
if __name__ == "__main__":
    main()
