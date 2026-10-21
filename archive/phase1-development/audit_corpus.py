import os
import json
import psycopg2
import chromadb
import pickle

def main():
    root_dir = os.path.abspath("C:/Users/Abyureddy/OneDrive/Desktop/SDC2")
    kb_dir = os.path.join(root_dir, "ResearchMind_LocalKB")
    
    # 1. Reconcile Canonical Paper Count
    # Let's find canonical_papers.json
    canonical_json_path = os.path.join(kb_dir, "canonical_papers.json")
    canonical_json_ids = set()
    if os.path.exists(canonical_json_path):
        with open(canonical_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # data might be list or dict
            if isinstance(data, list):
                canonical_json_ids = {p.get('id') for p in data if p.get('id')}
            elif isinstance(data, dict):
                canonical_json_ids = set(data.keys())
    else:
        # Check if there is another json file in indexes or metadata
        metadata_dir = os.path.join(kb_dir, "metadata")
        if os.path.exists(metadata_dir):
            for f in os.listdir(metadata_dir):
                if f.endswith('.json'):
                    try:
                        with open(os.path.join(metadata_dir, f), 'r', encoding='utf-8') as mf:
                            mdata = json.load(mf)
                            canonical_json_ids.add(mdata.get('id') or mdata.get('paper_id'))
                    except:
                        pass
                        
    # Postgres Papers
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost:5432/researchnexus")
    cur = conn.cursor()
    cur.execute("SELECT id FROM papers")
    pg_paper_ids = {row[0] for row in cur.fetchall()}
    
    print("--- PAPER COUNT RECONCILIATION ---")
    print(f"JSON IDs found: {len(canonical_json_ids)}")
    print(f"PG IDs found: {len(pg_paper_ids)}")
    
    added = pg_paper_ids - canonical_json_ids
    removed = canonical_json_ids - pg_paper_ids
    print(f"Added (in PG but not JSON): {len(added)}")
    print(f"Removed (in JSON but not PG): {len(removed)}")
    
    # 2. Reconcile Chunk Count
    cur.execute("SELECT chunk_id FROM paper_chunks")
    pg_chunk_ids = {row[0] for row in cur.fetchall()}
    print(f"\n--- CHUNK COUNT RECONCILIATION ---")
    print(f"PG Chunks: {len(pg_chunk_ids)}")
    
    # 3. BM25 Coverage
    bm25_path = os.path.join(kb_dir, "indexes", "bm25_index.pkl")
    mapping_path = os.path.join(kb_dir, "indexes", "bm25_mapping.json")
    bm25_chunk_ids = set()
    if os.path.exists(mapping_path):
        with open(mapping_path, 'r', encoding='utf-8') as f:
            bm25_mapping = json.load(f)
            bm25_chunk_ids = {m['chunk_id'] for m in bm25_mapping}
    print(f"\n--- BM25 COVERAGE ---")
    print(f"BM25 Mapping entries: {len(bm25_chunk_ids)}")
    
    # 4. ChromaDB
    chroma_path = os.path.join(kb_dir, "indexes", "chroma")
    chroma_client = chromadb.PersistentClient(path=chroma_path)
    collection = chroma_client.get_collection("researchnexus_local_v1_bgebase")
    chroma_count = collection.count()
    print(f"\n--- CHROMADB COVERAGE ---")
    print(f"Chroma Records: {chroma_count}")
    
    # To get actual missing chunks, we would need to page through chroma IDs, 
    # but we can get them all since it's local.
    res = collection.get(include=[])
    chroma_chunk_ids = set(res['ids'])
    
    missing_from_chroma = pg_chunk_ids - chroma_chunk_ids
    orphans_in_chroma = chroma_chunk_ids - pg_chunk_ids
    
    print(f"Vectors present: {len(chroma_chunk_ids)}")
    print(f"Vectors missing (in PG but not Chroma): {len(missing_from_chroma)}")
    print(f"Orphan vectors (in Chroma but not PG): {len(orphans_in_chroma)}")
    
    if len(missing_from_chroma) > 0:
        print(f"Sample missing chunk IDs: {list(missing_from_chroma)[:5]}")
        # check which paper these belong to
        missing_sample = list(missing_from_chroma)[0]
        cur.execute("SELECT paper_id FROM paper_chunks WHERE chunk_id = %s", (missing_sample,))
        row = cur.fetchone()
        if row:
            print(f"Missing chunk {missing_sample} belongs to paper: {row[0]}")
            
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
