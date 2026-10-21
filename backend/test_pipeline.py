import asyncio
import json
from app.services.ingestion import search_arxiv, download_paper_pdf
from app.services.document_processing import extract_text_pymupdf, process_and_chunk_document, get_embed_model
from app.services.retrieval import query_chromadb, query_bm25_all, reciprocal_rank_fusion, rerank_with_bge, generate_rag_response
from app.db.session import get_chroma_client
import logging

logging.basicConfig(level=logging.INFO)

async def run_test_pipeline():
    print("--- 1. Testing Online Repository (arXiv) ---")
    results = await search_arxiv("retrieval augmented generation", max_results=1)
    if not results:
        print("No papers found or network error.")
        return
        
    paper = results[0]
    print(f"Found Paper: {paper['title']}")
    print(f"PDF URL: {paper['url']}")
    
    print("\n--- 2. Downloading PDF ---")
    pdf_bytes = await download_paper_pdf(paper['url'])
    if not pdf_bytes:
        print("Failed to download PDF.")
        return
    print(f"Downloaded {len(pdf_bytes)} bytes.")

    print("\n--- 3. Document Processing (PyMuPDF -> LlamaIndex -> BGE Embeddings) ---")
    text = extract_text_pymupdf(pdf_bytes)
    print(f"Extracted {len(text)} characters of text.")
    
    metadata = {"id": "test_arxiv_001", "title": paper['title'], "domain": paper['domain']}
    chunks = process_and_chunk_document(text, metadata)
    print(f"Generated {len(chunks)} semantic chunks with BAAI/bge-base-en-v1.5 embeddings.")

    print("\n--- 4. Storing in ChromaDB ---")
    client = get_chroma_client()
    collection = client.get_or_create_collection("papers")
    
    if chunks:
        collection.add(
            ids=[c['chunk_id'] for c in chunks],
            documents=[c['text'] for c in chunks],
            embeddings=[c['embedding'] for c in chunks],
            metadatas=[c['metadata'] for c in chunks]
        )
        print("Successfully stored chunks in ChromaDB.")

    print("\n--- 5. Query Processing & Retrieval Pipeline ---")
    query = "How does retrieval augmented generation reduce hallucinations?"
    
    print(f"Query: {query}")
    model = get_embed_model()
    query_embedding = model.encode([query], normalize_embeddings=True)[0].tolist()

    print("a) ChromaDB Semantic Search...")
    semantic_results = query_chromadb(query_embedding, domain="Data Science / AI", n_results=5)
    print(f"   Retrieved {len(semantic_results)} semantic results.")
    
    print("b) BM25 Keyword Search...")
    bm25_results = query_bm25_all(query, domain="Data Science / AI", n_results=5)
    print(f"   Retrieved {len(bm25_results)} keyword results.")

    print("c) Reciprocal Rank Fusion (RRF)...")
    fused_results = reciprocal_rank_fusion(semantic_results, bm25_results)
    print(f"   Fused into {len(fused_results)} unique results.")

    print("d) BAAI/bge-reranker-base Reranking...")
    reranked_results = rerank_with_bge(query, fused_results, top_k=3)
    print(f"   Reranked top {len(reranked_results)} results.")

    print("\n--- 6. Gemini 2.5 Flash RAG & Explainable AI ---")
    response = generate_rag_response(query, reranked_results)
    
    print("\n=== GENERATED ANSWER ===")
    print(response["answer"])
    
    print("\n=== EXPLAINABLE AI METADATA ===")
    print(json.dumps(response["explainability"], indent=2))

if __name__ == "__main__":
    asyncio.run(run_test_pipeline())
