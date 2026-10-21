import re

with open('backend/app/api/papers.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_dedup = """    seen_doi = set()
    seen_title = set()
    seen_ids = set()
    mixed_papers = []
    
    def add_paper(p):
        pid = p.get('id') or p.get('paper_id')
        doi = p.get('doi')
        title = p.get('title')
        norm_title = normalize_title(title)
        
        if pid and pid in seen_ids: return False
        if doi and doi in seen_doi: return False
        if norm_title and norm_title in seen_title: return False
        
        if pid: seen_ids.add(pid)
        if doi: seen_doi.add(doi)
        if norm_title: seen_title.add(norm_title)
        
        mixed_papers.append(p)
        return True"""

new_dedup = """    seen_map = {}
    mixed_papers = []
    
    def add_paper(p):
        pid = p.get('id') or p.get('paper_id')
        doi = p.get('doi')
        title = p.get('title')
        norm_title = normalize_title(title)
        
        existing_paper = None
        if pid and pid in seen_map: existing_paper = seen_map[pid]
        elif doi and doi in seen_map: existing_paper = seen_map[doi]
        elif norm_title and norm_title in seen_map: existing_paper = seen_map[norm_title]
        
        if existing_paper:
            # Found in both
            if existing_paper.get('retrieval_source') != p.get('retrieval_source'):
                existing_paper['retrieval_source'] = 'mixed'
                # Merge evidence text if needed
                if p.get('evidence_text') and not existing_paper.get('evidence_text'):
                    existing_paper['evidence_text'] = p['evidence_text']
                if p.get('chunk_id') and not existing_paper.get('chunk_id'):
                    existing_paper['chunk_id'] = p['chunk_id']
            return False
            
        if pid: seen_map[pid] = p
        if doi: seen_map[doi] = p
        if norm_title: seen_map[norm_title] = p
        
        mixed_papers.append(p)
        return True"""

c = c.replace(old_dedup, new_dedup)

with open('backend/app/api/papers.py', 'w', encoding='utf-8') as f:
    f.write(c)
