import re

content = """
import os
import json
import time
import pickle
import re
from functools import lru_cache
import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder

from app.db.session import SessionLocal
from app.models.paper import Paper, PaperChunk

def clean_token(text):
    return re.sub(r'[^\\w\\s-]', '', text.lower()).split()

class LocalEvidenceRetriever:
    def __init__(self, indexes_dir='ResearchMind_LocalKB/indexes'):
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
        self.indexes_dir = os.path.join(root_dir, indexes_dir)
        self.chroma_path = os.path.join(self.indexes_dir, 'chroma')
        self.bm25_path = os.path.join(self.indexes_dir, 'bm25_index.pkl')
        self.mapping_path = os.path.join(self.indexes_dir, 'bm25_mapping.json')
        
        self.client = None
        self.collection = None
        self.bm25 = None
        self.bm25_mapping = None
        self.embed_model = None
        self.rerank_model = None
        
        self.init_status = "uninitialized"
        
    def load(self):
        try:
            self.client = chromadb.PersistentClient(path=self.chroma_path)
            self.collection = self.client.get_collection('researchnexus_local_v1_bgebase')
            
            with open(self.bm25_path, 'rb') as fp:
                self.bm25 = pickle.load(fp)
            with open(self.mapping_path, 'r') as fp:
                self.bm25_mapping = json.load(fp)
                
            self.embed_model = SentenceTransformer('BAAI/bge-base-en-v1.5')
            self.rerank_model = CrossEncoder('BAAI/bge-reranker-base')
            
            self.init_status = "ready"
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self.init_status = f"failed: {str(e)}\\nTraceback:\\n{tb}"
            
    @lru_cache(maxsize=128)
    def _get_query_embedding(self, query):
        return self.embed_model.encode([query], normalize_embeddings=True)[0].tolist()
            
    def retrieve_bm25(self, query, top_k=20):
        start = time.time()
        tokens = clean_token(query)
        scores = self.bm25.get_scores(tokens)
        top_n = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        
        results = []
        for rank, i in enumerate(top_n, 1):
            m = self.bm25_mapping[i]
            results.append({
                'rank': rank,
                'chunk_id': m['chunk_id'],
                'paper_id': m['paper_id'],
                'score': float(scores[i])
            })
        latency = time.time() - start
        return results, latency
        
    def retrieve_dense(self, query, top_k=20):
        start = time.time()
        q_emb = self._get_query_embedding(query)
        res = self.collection.query(query_embeddings=[q_emb], n_results=top_k)
        
        results = []
        if res and res['ids'] and len(res['ids']) > 0:
            for rank, i in enumerate(range(len(res['ids'][0])), 1):
                meta = res['metadatas'][0][i]
                results.append({
                    'rank': rank,
                    'chunk_id': res['ids'][0][i],
                    'paper_id': meta['paper_id'],
                    'distance': res['distances'][0][i]
                })
        latency = time.time() - start
        return results, latency
        
    def retrieve_hybrid_rrf(self, query, rrf_k=60, top_k=20):
        bm25_res, bm25_latency = self.retrieve_bm25(query, top_k)
        dense_res, dense_latency = self.retrieve_dense(query, top_k)
        
        start = time.time()
        rrf_scores = {}
        bm25_ranks = {}
        dense_ranks = {}
        
        for item in bm25_res:
            cid = item['chunk_id']
            rrf_scores[cid] = rrf_scores.get(cid, 0) + (1.0 / (rrf_k + item['rank']))
            bm25_ranks[cid] = item['rank']
            
        for item in dense_res:
            cid = item['chunk_id']
            rrf_scores[cid] = rrf_scores.get(cid, 0) + (1.0 / (rrf_k + item['rank']))
            dense_ranks[cid] = item['rank']
            
        pg_candidates = 0
        pg_latency = 0
        pg_start = time.time()
        db = SessionLocal()
        try:
            kw = f"%{query}%"
            pg_papers = db.query(Paper).filter((Paper.title.ilike(kw)) | (Paper.abstract.ilike(kw))).limit(top_k).all()
            pg_candidates = len(pg_papers)
            for p in pg_papers:
                chunk = db.query(PaperChunk).filter(PaperChunk.paper_id == p.id).first()
                if chunk:
                    cid = chunk.chunk_id
                    rrf_scores[cid] = rrf_scores.get(cid, 0) + 1.0
        finally:
            db.close()
        pg_latency = time.time() - pg_start
            
        final = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        rrf_latency = time.time() - start
        
        candidates = []
        for rank, (cid, score) in enumerate(final, 1):
            candidates.append({
                'rank': rank,
                'chunk_id': cid,
                'rrf_score': score,
                'bm25_rank': bm25_ranks.get(cid),
                'dense_rank': dense_ranks.get(cid)
            })
            
        trace_data = {
            "bm25_candidates": len(bm25_res),
            "dense_candidates": len(dense_res),
            "pg_candidates": pg_candidates,
            "fused_candidates": len(candidates),
            "rrf_k": rrf_k,
            "pg_latency": pg_latency,
            "bm25_latency": bm25_latency,
            "dense_latency": dense_latency,
            "rrf_latency": rrf_latency
        }
            
        return candidates, trace_data
        
    def rerank_and_build_evidence(self, query, candidates, top_k_evidence=5, use_reranker=True):
        start = time.time()
        
        db = SessionLocal()
        try:
            valid_candidates = []
            q_tokens = set(clean_token(query))
            
            for c in candidates:
                cid = c['chunk_id']
                chunk = db.query(PaperChunk).filter(PaperChunk.chunk_id == cid).first()
                if chunk and chunk.text.strip():
                    c['chunk_data'] = chunk
                    valid_candidates.append(c)
                        
            filter_start = time.time()
            if not valid_candidates:
                return [], [], time.time() - start, {"rejected_count": 0, "filter_latency": 0, "diversification_latency": 0, "rerank_latency": 0}
                
            candidates_before_filter = len(valid_candidates)
            rejected_count = 0
                
            if use_reranker:
                inputs = [(query, c['chunk_data'].text) for c in valid_candidates]
                rerank_start = time.time()
                scores = self.rerank_model.predict(inputs)
                rerank_latency = time.time() - rerank_start
                for c, score in zip(valid_candidates, scores):
                    c['reranker_score'] = float(score)
                valid_candidates.sort(key=lambda x: x['reranker_score'], reverse=True)
                filtered_candidates = [c for c in valid_candidates if c['reranker_score'] > 0.0]
                rejected_count = len(valid_candidates) - len(filtered_candidates)
                valid_candidates = filtered_candidates
                filter_latency = time.time() - filter_start - rerank_latency
            else:
                rerank_latency = 0
                gated_candidates = []
                for c in valid_candidates:
                    chunk = c['chunk_data']
                    text_lower = chunk.text.lower()
                    paper = db.query(Paper).filter(Paper.id == chunk.paper_id).first()
                    title_lower = (paper.title or '').lower() if paper else ''
                    abstract_lower = (paper.abstract or '').lower() if paper else ''
                    
                    overlap = sum(1 for t in q_tokens if t in text_lower or t in title_lower or t in abstract_lower)
                    overlap_ratio = overlap / max(1, len(q_tokens))
                    
                    if overlap_ratio > 0.15 or c['rrf_score'] > 0.01:
                        c['filter_decision'] = 'Accepted'
                        gated_candidates.append(c)
                    else:
                        c['filter_decision'] = 'Rejected (low overlap)'
                        
                rejected_count = len(valid_candidates) - len(gated_candidates)
                valid_candidates = sorted(gated_candidates, key=lambda x: x['rrf_score'], reverse=True)
                filter_latency = time.time() - filter_start
            
            div_start = time.time()
            paper_seen = set()
            evidence_list = []
            metadata_only = []
            
            for c in valid_candidates:
                chunk = c['chunk_data']
                pid = chunk.paper_id
                
                if pid in paper_seen:
                    continue
                
                paper_seen.add(pid)
                paper = db.query(Paper).filter(Paper.id == pid).first()
                if not paper:
                    continue
                
                ev_status = "evidence_ready" if chunk.text.strip() else "metadata_only"
                
                evidence = {
                    'id': pid,
                    'paper_id': pid,
                    'chunk_id': c['chunk_id'],
                    'title': paper.title,
                    'authors': paper.authors,
                    'abstract': paper.abstract,
                    'keywords': paper.keywords.split(', ') if paper.keywords else [],
                    'evidence_text': chunk.text,
                    'section': chunk.section if hasattr(chunk, 'section') else None,
                    'page': chunk.page_start if hasattr(chunk, 'page_start') else None,
                    'domain': paper.domain_id,
                    'subdomain': paper.subdomain,
                    'publication_year': paper.publication_year,
                    'publication_date': paper.publication_date,
                    'doi': paper.doi,
                    'source_repository': paper.source_repository,
                    'paper_url': paper.paper_url,
                    'pdf_url': paper.pdf_path,
                    'pdf_path': paper.pdf_path,
                    'read_source': paper.read_source,
                    'retrieval_source': 'local',
                    'bm25_rank': c.get('bm25_rank'),
                    'dense_rank': c.get('dense_rank'),
                    'rrf_rank': c['rank'],
                    'rrf_score': c['rrf_score'],
                    'reranker_score': c.get('reranker_score'),
                    'filter_decision': c.get('filter_decision', 'Accepted'),
                    'evidence_status': ev_status
                }
                
                evidence['url'] = evidence['paper_url']
                
                if ev_status == "evidence_ready":
                    evidence_list.append(evidence)
                else:
                    metadata_only.append(evidence)
                    
                if len(evidence_list) >= top_k_evidence:
                    break
                    
            div_latency = time.time() - div_start
            latency = time.time() - start
            
            trace_data = {
                "candidates_before": candidates_before_filter,
                "rejected_count": rejected_count,
                "candidates_after": len(valid_candidates),
                "unique_papers": len(evidence_list) + len(metadata_only),
                "filter_latency": filter_latency,
                "diversification_latency": div_latency,
                "rerank_latency": rerank_latency
            }
            return evidence_list, metadata_only, latency, trace_data
            
        finally:
            db.close()
            
    def retrieve(self, query, rrf_candidates=10, top_k_evidence=5, deep_evidence=False):
        overall_start = time.time()
        
        # Query Understanding Trace
        query_analysis_start = time.time()
        tokens = clean_token(query)
        query_analysis_latency = time.time() - query_analysis_start
        
        candidates, trace_hybrid = self.retrieve_hybrid_rrf(query, top_k=rrf_candidates)
        
        evidence, metadata_only, l_build, trace_build = self.rerank_and_build_evidence(
            query, 
            candidates, 
            top_k_evidence, 
            use_reranker=deep_evidence
        )
        
        # Final ranking
        for idx, ev in enumerate(evidence):
            ev['rank'] = idx + 1
            if deep_evidence:
                ev['bge_rank'] = idx + 1
                ev['bge_score'] = ev.get('reranker_score')
        
        is_sufficient = len(evidence) > 0 and (evidence[0].get('reranker_score', 0) > 0.01 or not deep_evidence)
        
        stages = ["Local Retrieval", "BM25", "Dense", "RRF", "Relevance Filtering"]
        if deep_evidence:
            stages.append("BGE Reranking")
            
        total_latency = time.time() - overall_start
            
        trace = {
            "stages": stages,
            "query": query,
            "search_query": query,
            "keywords": tokens,
            "key_phrases": [query],
            "candidates": trace_hybrid["fused_candidates"],
            "evidence_ready": len(evidence),
            "latencies": {
                "query_analysis": query_analysis_latency,
                "postgres": trace_hybrid["pg_latency"],
                "bm25": trace_hybrid["bm25_latency"],
                "dense": trace_hybrid["dense_latency"],
                "rrf": trace_hybrid["rrf_latency"],
                "build": trace_build["filter_latency"],
                "diversification": trace_build["diversification_latency"],
                "rerank_build": trace_build["rerank_latency"]
            },
            "total_latency": total_latency,
            "deep_evidence": deep_evidence,
            "rrf_k": trace_hybrid["rrf_k"],
            "bm25_candidates": trace_hybrid["bm25_candidates"],
            "dense_candidates": trace_hybrid["dense_candidates"],
            "pg_candidates": trace_hybrid["pg_candidates"],
            "candidates_before_filter": trace_build["candidates_before"],
            "rejected_count": trace_build["rejected_count"],
            "candidates_after_filter": trace_build["candidates_after"],
            "unique_papers": trace_build["unique_papers"]
        }
        
        return evidence, is_sufficient, trace

local_retriever_instance = LocalEvidenceRetriever()

def get_local_retriever():
    if local_retriever_instance.init_status == "uninitialized":
        local_retriever_instance.load()
    return local_retriever_instance
"""

with open('backend/app/services/local_evidence.py', 'w', encoding='utf-8') as f:
    f.write(content)

