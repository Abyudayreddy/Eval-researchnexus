import chromadb

paths = ['backend/chroma_db', 'chroma_db', 'ResearchMind_LocalKB', 'ResearchMind_LocalKB/indexes/chroma']
for p in paths:
    try:
        client = chromadb.PersistentClient(path=p)
        cols = client.list_collections()
        print(f"Path: {p} -> {len(cols)} collections")
        for c in cols:
            cnt = c.count()
            print(f"  Collection: {c.name}, Count: {cnt}")
            if cnt > 0:
                item = c.get(limit=1, include=['embeddings', 'metadatas'])
                embs = item.get('embeddings')
                dim = len(embs[0]) if embs is not None and len(embs) > 0 else 'None'
                meta = item['metadatas'][0] if item.get('metadatas') else {}
                print(f"    Embedding dim: {dim}, Sample meta: {meta}")
    except Exception as e:
        print(f"Path: {p} -> Error: {e}")
