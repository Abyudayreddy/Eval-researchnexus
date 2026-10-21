import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/researchnexus"
os.environ["GEMINI_API_KEY"] = "dummy"

from app.services.local_evidence import get_local_retriever

def main():
    retriever = get_local_retriever()
    query = "Stock Price Prediction Using Triple Barrier Labeling"
    
    candidates, l_bm25, l_dense, l_rrf = retriever.retrieve_hybrid_rrf(query, top_k=60)
    print("Candidates count:", len(candidates))
    for c in candidates[:5]:
        print(" ", c)
        
    evidence, metadata_only, latency = retriever.rerank_and_build_evidence(query, candidates, use_reranker=False)
    
    print("\nEvidence length:", len(evidence))
    for e in evidence:
        print(f"[{e['id']}] {e['title']} (RRF: {e.get('rrf_score')}, Rerank: {e.get('reranker_score')})")

if __name__ == "__main__":
    main()
