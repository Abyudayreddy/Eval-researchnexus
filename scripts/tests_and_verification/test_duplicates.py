import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/researchnexus"
os.environ["GEMINI_API_KEY"] = "dummy"

from app.services.local_evidence import get_local_retriever

def main():
    retriever = get_local_retriever()
    
    queries = [
        "How is AI being utilized to spread extremist and jihadist propaganda online in Indonesia?",
        "Can a multi-view RAG system that is aware of authority improve who speaks?",
        "Can raw OHLCV data be used with deep learning to forecast stock prices without technical indicators?",
        "Is the favorable view of a firm influenced significantly by its social initiatives?",
        "How can reinforcement-based agentic intelligence be applied to manage clinical trials efficiently?"
    ]
    
    for i, q in enumerate(queries):
        candidates, l_bm25, l_dense, l_rrf = retriever.retrieve_hybrid_rrf(q, rrf_k=60, top_k=60)
        evidence, meta, latency = retriever.rerank_and_build_evidence(q, candidates, top_k_evidence=5, use_reranker=False)
        
        print(f"--- Query {i+1} ---")
        print(f"Q: {q}")
        print("Final Evidence Paper IDs:")
        for e in evidence:
            print("  ", e['paper_id'])
            
if __name__ == "__main__":
    main()
