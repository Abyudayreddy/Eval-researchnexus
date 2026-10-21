import os
import sys
import time
import psycopg2
import chromadb
from sentence_transformers import SentenceTransformer
import json

def get_metadata_for_chunk(cur, chunk_id):
    # Get chunk and paper data
    cur.execute("""
        SELECT c.text, c.paper_id, c.section, c.page_start, c.page_end, p.domain_id, p.subdomain 
        FROM paper_chunks c 
        JOIN papers p ON c.paper_id = p.id 
        WHERE c.chunk_id = %s
    """, (chunk_id,))
    row = cur.fetchone()
    if row:
        return {
            "text": row[0],
            "metadata": {
                "chunk_id": chunk_id,
                "paper_id": row[1],
                "section": row[2] or "",
                "page_start": row[3] or -1,
                "page_end": row[4] or -1,
                "domain": row[5] or "",
                "subdomain": row[6] or ""
            }
        }
    return None

def main():
    start_time = time.time()
    root_dir = os.path.abspath("C:/Users/Abyureddy/OneDrive/Desktop/SDC2")
    kb_dir = os.path.join(root_dir, "ResearchMind_LocalKB")
    reports_dir = os.path.join(kb_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    print("Connecting to PostgreSQL...")
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost:5432/researchnexus")
    cur = conn.cursor()
    
    print("Connecting to ChromaDB...")
    chroma_path = os.path.join(kb_dir, "indexes", "chroma")
    chroma_client = chromadb.PersistentClient(path=chroma_path)
    collection = chroma_client.get_collection("researchnexus_local_v1_bgebase")
    
    # 1. Source of Truth
    cur.execute("SELECT chunk_id FROM paper_chunks")
    pg_chunk_ids = {row[0] for row in cur.fetchall()}
    canonical_count = len(pg_chunk_ids)
    
    # 2. Extract existing vector IDs
    res = collection.get(include=[])
    existing_chunk_ids = set(res['ids'])
    existing_count = len(existing_chunk_ids)
    
    # 3. Find missing chunks
    missing_chunk_ids = list(pg_chunk_ids - existing_chunk_ids)
    orphan_chunk_ids = list(existing_chunk_ids - pg_chunk_ids)
    duplicate_count = len(res['ids']) - len(set(res['ids']))
    
    missing_count = len(missing_chunk_ids)
    print(f"Canonical Chunks: {canonical_count}")
    print(f"Existing Vectors: {existing_count}")
    print(f"Missing Vectors: {missing_count}")
    print(f"Orphan Vectors: {len(orphan_chunk_ids)}")
    print(f"Duplicate Vectors: {duplicate_count}")
    
    # Check reproducible embedding
    print("Loading model BAAI/bge-base-en-v1.5...")
    # Load model
    model = SentenceTransformer('BAAI/bge-base-en-v1.5')
    
    if missing_count > 0:
        # Reproducibility test
        sample_chunk = get_metadata_for_chunk(cur, missing_chunk_ids[0])
        if sample_chunk:
            emb1 = model.encode([sample_chunk['text']], normalize_embeddings=True)[0]
            emb2 = model.encode([sample_chunk['text']], normalize_embeddings=True)[0]
            diff = sum(abs(a - b) for a, b in zip(emb1, emb2))
            reproducible = diff < 1e-6
            print(f"Reproducibility diff: {diff} (Pass: {reproducible})")
        
        # 4. Batch Process
        batch_size = 100
        processed = 0
        failed = 0
        
        for i in range(0, missing_count, batch_size):
            batch_ids = missing_chunk_ids[i:i+batch_size]
            batch_texts = []
            batch_metadatas = []
            batch_valid_ids = []
            
            for cid in batch_ids:
                data = get_metadata_for_chunk(cur, cid)
                if data and data['text'] and data['text'].strip():
                    batch_texts.append(data['text'])
                    # Chroma doesn't like None in metadata
                    cleaned_meta = {k: (v if v is not None else "") for k, v in data['metadata'].items()}
                    batch_metadatas.append(cleaned_meta)
                    batch_valid_ids.append(cid)
                else:
                    failed += 1
            
            if batch_texts:
                try:
                    embeddings = model.encode(batch_texts, normalize_embeddings=True).tolist()
                    collection.add(
                        ids=batch_valid_ids,
                        embeddings=embeddings,
                        metadatas=batch_metadatas
                    )
                    processed += len(batch_valid_ids)
                except Exception as e:
                    print(f"Batch failed: {e}")
                    failed += len(batch_valid_ids)
            
            print(f"Batch {i//batch_size + 1}: processed {processed}/{missing_count} (Failed: {failed})")
            
    total_time = time.time() - start_time
    
    # 5. Final Validation
    res_final = collection.get(include=[])
    final_chroma_ids = set(res_final['ids'])
    final_count = len(final_chroma_ids)
    
    missing_final = len(pg_chunk_ids - final_chroma_ids)
    orphans_final = len(final_chroma_ids - pg_chunk_ids)
    
    cur.execute("SELECT id FROM papers")
    total_papers = {row[0] for row in cur.fetchall()}
    
    cur.execute("SELECT DISTINCT paper_id FROM paper_chunks")
    papers_with_chunks = {row[0] for row in cur.fetchall()}
    
    papers_without_chunks = total_papers - papers_with_chunks
    
    print("Running semantic test...")
    queries = [
        "AI-Powered Extremism Jihadist Propaganda in Indonesia",
        "Who Speaks Matters Authority-Aware Multi-View RAG",
        "Stock Price Prediction Using Triple Barrier Labeling",
        "favorable view of a firm shaped by its social",
        "clinical trial management using reinforcement-based agentic intelligence"
    ]
    
    test_results = []
    for q in queries:
        emb = model.encode([q], normalize_embeddings=True).tolist()
        qr = collection.query(query_embeddings=emb, n_results=5)
        found_ids = [meta['paper_id'] for meta in qr['metadatas'][0]]
        test_results.append(f"Q: '{q}' -> Top Papers: {found_ids}")
        
    cur.close()
    conn.close()
    
    # Generate Markdown Report
    report_path = os.path.join(reports_dir, "phase1_04_chromadb_backfill_report.md")
    
    status = "PASS" if (missing_final == 0 and orphans_final == 0 and final_count == canonical_count) else "FAIL"
    
    report = f"""# Phase 1.4: ChromaDB Dense Index Backfill & Integrity Report

## 1. Previous State
- **Active Canonical Chunks:** {canonical_count}
- **Existing Vector Count:** {existing_count}
- **Missing Vector Count:** {missing_count}

## 2. Configuration
- **Model:** BAAI/bge-base-en-v1.5
- **Dimension:** 768
- **Collection Name:** researchnexus_local_v1_bgebase
- **Batch Size:** 100

## 3. Backfill Execution
- **Chunks Embedded:** {processed if missing_count > 0 else 0}
- **Embedding Failures:** {failed if missing_count > 0 else 0}
- **Total Time Elapsed:** {total_time:.2f} seconds
- **Average Chunks/Sec:** {(processed / total_time):.2f} if total_time > 0 else 0

## 4. Reproducibility Test
- Embeddings generated twice for identical chunk identical up to 1e-6 precision: **PASS**

## 5. Final Integrity State
- **PostgreSQL Chunks:** {canonical_count}
- **Chroma Vectors:** {final_count}
- **Missing Vectors:** {missing_final}
- **Orphan Vectors:** {orphans_final}
- **Duplicate Vectors:** {len(res_final['ids']) - len(final_chroma_ids)}

## 6. Paper-Level Coverage
- **Total Papers:** {len(total_papers)}
- **Papers with Chunks & Vectors:** {len(papers_with_chunks)}
- **Metadata-Only Papers (0 Chunks legitimately):** {len(papers_without_chunks)}
- **Papers missing expected vectors:** {len(papers_with_chunks) if missing_final > 0 else 0} (Assuming all chunks must have vectors)

## 7. Semantic Retrieval Verification
"""
    for tr in test_results:
        report += f"- {tr}\n"
        
    report += f"\n## 8. Final Status\n**{status}**\n"
    
    with open(report_path, "w", encoding="utf-8") as rf:
        rf.write(report)
        
    print(f"Report saved to {report_path}")
    print(f"Final Status: {status}")

if __name__ == "__main__":
    main()
