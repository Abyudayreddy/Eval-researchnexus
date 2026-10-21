import os
import psycopg2
import chromadb

def main():
    print("--- Local Corpus Integrity ---")
    
    # Postgres
    try:
        conn = psycopg2.connect("postgresql://postgres:postgres@localhost:5432/researchnexus")
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM papers")
        papers_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM paper_chunks")
        chunks_count = cur.fetchone()[0]
        cur.close()
        conn.close()
        print(f"Papers (canonical): {papers_count}")
        print(f"Chunks (canonical): {chunks_count}")
    except Exception as e:
        print("Postgres Error:", e)
        
    # Chroma
    try:
        chroma_client = chromadb.PersistentClient(path=os.path.abspath("C:/Users/Abyureddy/OneDrive/Desktop/SDC2/ResearchMind_LocalKB/indexes/chroma"))
        collection = chroma_client.get_collection("researchnexus_local_v1_bgebase")
        chroma_count = collection.count()
        print(f"Chroma Records: {chroma_count}")
    except Exception as e:
        print("Chroma Error:", e)
        
    # BM25
    try:
        import pickle
        bm25_path = "C:/Users/Abyureddy/OneDrive/Desktop/SDC2/ResearchMind_LocalKB/indexes/bm25_index.pkl"
        if os.path.exists(bm25_path):
            with open(bm25_path, "rb") as f:
                index = pickle.load(f)
                print(f"BM25 Records: {index.corpus_size if hasattr(index, 'corpus_size') else len(index.doc_freqs)}")
        else:
            print("BM25 index not found at", bm25_path)
    except Exception as e:
        print("BM25 Error:", e)

if __name__ == "__main__":
    main()
