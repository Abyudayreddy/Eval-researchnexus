import re

with open('backend/app/services/local_evidence.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_func = """    def rerank_and_build_evidence(self, query, candidates, top_k_evidence=5, use_reranker=True):
        start = time.time()
        
        valid_candidates = []
        for c in candidates:
            cid = c['chunk_id']
            if cid in self.chunk_cache:
                chunk_data = self.chunk_cache[cid]
                text = chunk_data.get('text', '')
                if text.strip():
                    c['chunk_data'] = chunk_data
                    valid_candidates.append(c)
                    
        if not valid_candidates:
            return [], [], time.time() - start
            
        if use_reranker:
            inputs = [(query, c['chunk_data'].get('text', '')) for c in valid_candidates]
            scores = self.rerank_model.predict(inputs)
            for c, score in zip(valid_candidates, scores):
                c['reranker_score'] = float(score)
            # Sort by reranker
            valid_candidates.sort(key=lambda x: x['reranker_score'], reverse=True)
        else:
            # Fallback to RRF score
            for c in valid_candidates:
                c['reranker_score'] = c['rrf_score']
            valid_candidates.sort(key=lambda x: x['rrf_score'], reverse=True)"""

new_func = """    def rerank_and_build_evidence(self, query, candidates, top_k_evidence=5, use_reranker=True):
        start = time.time()
        
        valid_candidates = []
        q_tokens = set(clean_token(query))
        
        for c in candidates:
            cid = c['chunk_id']
            if cid in self.chunk_cache:
                chunk_data = self.chunk_cache[cid]
                text = chunk_data.get('text', '')
                if text.strip():
                    c['chunk_data'] = chunk_data
                    valid_candidates.append(c)
                    
        if not valid_candidates:
            return [], [], time.time() - start
            
        if use_reranker:
            inputs = [(query, c['chunk_data'].get('text', '')) for c in valid_candidates]
            scores = self.rerank_model.predict(inputs)
            for c, score in zip(valid_candidates, scores):
                c['reranker_score'] = float(score)
            valid_candidates.sort(key=lambda x: x['reranker_score'], reverse=True)
            # Filter loosely
            valid_candidates = [c for c in valid_candidates if c['reranker_score'] > 0.0]
        else:
            # Lightweight relevance gate
            gated_candidates = []
            for c in valid_candidates:
                text_lower = c['chunk_data'].get('text', '').lower()
                pid = c['chunk_data'].get('paper_id')
                canonical = self.metadata_cache.get(pid, {})
                title_lower = (canonical.get('title') or '').lower()
                abstract_lower = (canonical.get('abstract') or '').lower()
                
                # Check term overlap
                overlap = sum(1 for t in q_tokens if t in text_lower or t in title_lower or t in abstract_lower)
                overlap_ratio = overlap / max(1, len(q_tokens))
                
                # Baseline gate: Must match at least some ratio or have high RRF
                if overlap_ratio > 0.25 or c['rrf_score'] > 0.03:
                    c['reranker_score'] = c['rrf_score']
                    gated_candidates.append(c)
                    
            valid_candidates = sorted(gated_candidates, key=lambda x: x['rrf_score'], reverse=True)"""

c = c.replace(old_func, new_func)

with open('backend/app/services/local_evidence.py', 'w', encoding='utf-8') as f:
    f.write(c)
