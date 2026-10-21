import re

with open("backend/app/services/local_evidence.py", "r") as f:
    code = f.read()

# Fix 1: pg_papers chunk fetching in retrieve_hybrid_rrf
fix1 = """
            pg_candidates = len(pg_papers)
            
            p_ids = [p.id for p in pg_papers]
            chunks = db.query(PaperChunk).filter(PaperChunk.paper_id.in_(p_ids)).all() if p_ids else []
            chunk_map = {}
            for chunk in chunks:
                if chunk.paper_id not in chunk_map:
                    chunk_map[chunk.paper_id] = chunk
            
            for p in pg_papers:
                chunk = chunk_map.get(p.id)
                if chunk:
"""
code = re.sub(
    r"\s*pg_candidates = len\(pg_papers\)\s*for p in pg_papers:\s*chunk = db\.query\(PaperChunk\)\.filter\(PaperChunk\.paper_id == p\.id\)\.first\(\)\s*if chunk:",
    fix1,
    code
)

# Fix 2: rerank_and_build_evidence chunk and paper batching
fix2 = """
            start = time.time()
            candidates_before_filter = len(candidates)
            
            # BATCH FETCH CHUNKS
            c_ids = [c['chunk_id'] for c in candidates]
            chunks = db.query(PaperChunk).filter(PaperChunk.chunk_id.in_(c_ids)).all() if c_ids else []
            chunk_by_id = {ch.chunk_id: ch for ch in chunks}
            
            valid_candidates = []
            for c in candidates:
                cid = c['chunk_id']
                chunk = chunk_by_id.get(cid)
                if chunk and chunk.text.strip():
                    c['chunk_data'] = chunk
                    valid_candidates.append(c)
            
            # BATCH FETCH PAPERS
            p_ids = list(set([c['chunk_data'].paper_id for c in valid_candidates]))
            papers = db.query(Paper).filter(Paper.id.in_(p_ids)).all() if p_ids else []
            paper_by_id = {p.id: p for p in papers}
"""
code = re.sub(
    r"\s*start = time\.time\(\)\s*candidates_before_filter = len\(candidates\)\s*valid_candidates = \[\]\s*for c in candidates:\s*cid = c\['chunk_id'\]\s*chunk = db\.query\(PaperChunk\)\.filter\(PaperChunk\.chunk_id == cid\)\.first\(\)\s*if chunk and chunk\.text\.strip\(\):\s*c\['chunk_data'\] = chunk\s*valid_candidates\.append\(c\)",
    fix2,
    code
)

code = re.sub(
    r"paper = db\.query\(Paper\)\.filter\(Paper\.id == chunk\.paper_id\)\.first\(\)",
    r"paper = paper_by_id.get(chunk.paper_id)",
    code
)

code = re.sub(
    r"paper = db\.query\(Paper\)\.filter\(Paper\.id == pid\)\.first\(\)",
    r"paper = paper_by_id.get(pid)",
    code
)

with open("backend/app/services/local_evidence.py", "w") as f:
    f.write(code)

print("Patched N+1 SQL queries.")
