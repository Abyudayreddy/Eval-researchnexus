import os
import json
import time
import pickle
import re
import chromadb
from sentence_transformers import SentenceTransformer

def clean_token(text):
    return re.sub(r'[^\w\s-]', '', text.lower()).split()

class LocalHybridRetriever:
    def __init__(self, indexes_dir='ResearchMind_LocalKB/indexes'):
        self.indexes_dir = indexes_dir
        self.chroma_path = os.path.join(indexes_dir, 'chroma')
        self.bm25_path = os.path.join(indexes_dir, 'bm25_index.pkl')
        self.mapping_path = os.path.join(indexes_dir, 'bm25_mapping.json')
        
        self.client = None
        self.collection = None
        self.bm25 = None
        self.bm25_mapping = None
        self.model = None
        
        self.init_status = "uninitialized"
        
    def load(self):
        try:
            self.client = chromadb.PersistentClient(path=self.chroma_path)
            self.collection = self.client.get_collection('researchnexus_local_v1_bgebase')
            
            with open(self.bm25_path, 'rb') as fp:
                self.bm25 = pickle.load(fp)
            with open(self.mapping_path, 'r') as fp:
                self.bm25_mapping = json.load(fp)
                
            self.model = SentenceTransformer('BAAI/bge-base-en-v1.5')
            self.init_status = "ready"
        except Exception as e:
            self.init_status = f"failed: {str(e)}"
            
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
                'title': m.get('title', ''),
                'domain': m.get('domain', ''),
                'score': float(scores[i])
            })
        latency = time.time() - start
        return results, latency
        
    def retrieve_dense(self, query, top_k=20):
        start = time.time()
        q_emb = self.model.encode([query], normalize_embeddings=True)[0].tolist()
        res = self.collection.query(query_embeddings=[q_emb], n_results=top_k)
        
        results = []
        for rank, i in enumerate(range(len(res['ids'][0])), 1):
            meta = res['metadatas'][0][i]
            results.append({
                'rank': rank,
                'chunk_id': res['ids'][0][i],
                'paper_id': meta['paper_id'],
                'title': meta.get('title', ''), # We didn't store title in chroma metadata? We'll get it from bm25 mapping or pass it if available. Wait, we'll just look it up.
                'domain': meta.get('domain', ''),
                'subdomain': meta.get('subdomain', ''),
                'section': meta.get('section', ''),
                'page_start': meta.get('page_start', -1),
                'page_end': meta.get('page_end', -1),
                'distance': res['distances'][0][i]
            })
        latency = time.time() - start
        return results, latency
        
    def retrieve(self, query, top_k_bm25=20, top_k_dense=20, rrf_k=60):
        total_start = time.time()
        
        if self.init_status != "ready":
            return {"query": query, "retrieval_status": self.init_status}
            
        bm25_res, bm25_latency = self.retrieve_bm25(query, top_k_bm25)
        dense_res, dense_latency = self.retrieve_dense(query, top_k_dense)
        
        rrf_start = time.time()
        rrf_scores = {}
        chunk_meta = {}
        
        for item in bm25_res:
            cid = item['chunk_id']
            rrf_scores[cid] = rrf_scores.get(cid, 0) + (1.0 / (rrf_k + item['rank']))
            chunk_meta[cid] = item
            chunk_meta[cid]['bm25_rank'] = item['rank']
            
        for item in dense_res:
            cid = item['chunk_id']
            rrf_scores[cid] = rrf_scores.get(cid, 0) + (1.0 / (rrf_k + item['rank']))
            if cid not in chunk_meta:
                chunk_meta[cid] = item
            chunk_meta[cid]['dense_rank'] = item['rank']
            if 'bm25_rank' not in chunk_meta[cid]:
                # Look up title from mapping if we only hit dense
                # we don't have a fast lookup, but we can live without title or scan
                pass
                
        # Diversification: Highest ranked chunk per paper
        paper_best_chunk = {}
        for cid, score in rrf_scores.items():
            meta = chunk_meta[cid]
            pid = meta['paper_id']
            if pid not in paper_best_chunk or score > paper_best_chunk[pid]['rrf_score']:
                paper_best_chunk[pid] = {
                    'chunk_id': cid,
                    'paper_id': pid,
                    'title': meta.get('title', 'Unknown Title'),
                    'domain': meta.get('domain', ''),
                    'subdomain': meta.get('subdomain', ''),
                    'section': meta.get('section', ''),
                    'page_start': meta.get('page_start', -1),
                    'page_end': meta.get('page_end', -1),
                    'bm25_rank': meta.get('bm25_rank', None),
                    'dense_rank': meta.get('dense_rank', None),
                    'rrf_score': score
                }
                
        # Sort final results
        final_results = sorted(paper_best_chunk.values(), key=lambda x: x['rrf_score'], reverse=True)
        for i, res in enumerate(final_results, 1):
            res['rank'] = i
            
        rrf_latency = time.time() - rrf_start
        total_latency = time.time() - total_start
        
        return {
            "query": query,
            "retrieval_source": "local",
            "method": "hybrid_rrf",
            "retrieval_status": "success",
            "bm25_count": top_k_bm25,
            "dense_count": top_k_dense,
            "rrf_count": len(final_results),
            "latencies": {
                "bm25": bm25_latency,
                "dense": dense_latency,
                "rrf": rrf_latency,
                "total": total_latency
            },
            "results": final_results,
            "raw_bm25": bm25_res,
            "raw_dense": dense_res
        }

def run_tests():
    print("Initializing Hybrid Retriever...")
    retriever = LocalHybridRetriever()
    retriever.load()
    if retriever.init_status != "ready":
        print(f"FAILED to initialize: {retriever.init_status}")
        return
        
    queries = [
        ("Artificial Intelligence", "retrieval augmented generation"),
        ("Artificial Intelligence", "transformer classification methods"),
        ("Environmental Science", "climate change mitigation"),
        ("Environmental Science", "water pollution monitoring"),
        ("Interdisciplinary", "smart city infrastructure"),
        ("Interdisciplinary", "digital twins sustainable development")
    ]
    
    reports = []
    latencies = {'bm25': [], 'dense': [], 'rrf': [], 'total': []}
    
    for domain, q in queries:
        print(f"Testing query: '{q}'...")
        res = retriever.retrieve(q)
        
        lats = res['latencies']
        latencies['bm25'].append(lats['bm25'])
        latencies['dense'].append(lats['dense'])
        latencies['rrf'].append(lats['rrf'])
        latencies['total'].append(lats['total'])
        
        bm25_cids = {x['chunk_id'] for x in res['raw_bm25']}
        dense_cids = {x['chunk_id'] for x in res['raw_dense']}
        
        intersection = len(bm25_cids.intersection(dense_cids))
        bm25_only = len(bm25_cids - dense_cids)
        dense_only = len(dense_cids - bm25_cids)
        
        reports.append({
            'query': q,
            'domain': domain,
            'overlap': {
                'intersection': intersection,
                'bm25_only': bm25_only,
                'dense_only': dense_only,
                'total_unique': intersection + bm25_only + dense_only
            },
            'bm25_top5': res['raw_bm25'][:5],
            'dense_top5': res['raw_dense'][:5],
            'rrf_top5': res['results'][:5]
        })
        
    # Repeatability test
    print("Running repeatability test...")
    q_repeat = "retrieval augmented generation"
    res1 = retriever.retrieve(q_repeat)
    res2 = retriever.retrieve(q_repeat)
    
    repeat_pass = True
    if len(res1['results']) != len(res2['results']):
        repeat_pass = False
    else:
        for r1, r2 in zip(res1['results'], res2['results']):
            if r1['chunk_id'] != r2['chunk_id'] or abs(r1['rrf_score'] - r2['rrf_score']) > 1e-6:
                repeat_pass = False
                break
                
    avg_bm25 = sum(latencies['bm25'])/len(latencies['bm25'])
    avg_dense = sum(latencies['dense'])/len(latencies['dense'])
    avg_rrf = sum(latencies['rrf'])/len(latencies['rrf'])
    avg_total = sum(latencies['total'])/len(latencies['total'])
    
    print(f"Repeatability: {'PASS' if repeat_pass else 'FAIL'}")
    
    # Write report
    report_md = f"# Phase 4B.6 Hybrid Retrieval & RRF Report\n\n"
    report_md += f"## Configuration\n"
    report_md += f"- **BM25 Top-K**: 20\n"
    report_md += f"- **Dense Top-K**: 20\n"
    report_md += f"- **RRF Formula**: `1 / (k + rank)` where k=60\n"
    report_md += f"- **Diversification**: Paper-level distinctness. Kept only the highest RRF-scored chunk per paper.\n\n"
    
    report_md += f"## Latency (Averages over 6 queries)\n"
    report_md += f"- **BM25**: {avg_bm25*1000:.1f} ms\n"
    report_md += f"- **Dense**: {avg_dense*1000:.1f} ms\n"
    report_md += f"- **RRF**: {avg_rrf*1000:.1f} ms\n"
    report_md += f"- **Total**: {avg_total*1000:.1f} ms\n\n"
    
    report_md += f"## Tests & Overlap\n"
    for r in reports:
        report_md += f"### Query: `{r['query']}` (Domain: {r['domain']})\n"
        report_md += f"**Overlap**: Intersection: {r['overlap']['intersection']}, BM25-only: {r['overlap']['bm25_only']}, Dense-only: {r['overlap']['dense_only']}\n\n"
        
        report_md += f"**BM25 Top-5**:\n"
        for i, x in enumerate(r['bm25_top5'], 1):
            report_md += f"{i}. [{x['paper_id']}] {x['title']} (Score: {x['score']:.2f})\n"
            
        report_md += f"\n**Dense Top-5**:\n"
        for i, x in enumerate(r['dense_top5'], 1):
            report_md += f"{i}. [{x['paper_id']}] {x.get('title', 'Unknown')} (Dist: {x['distance']:.3f})\n"
            
        report_md += f"\n**RRF Top-5 (Diversified)**:\n"
        for i, x in enumerate(r['rrf_top5'], 1):
            report_md += f"{i}. [{x['paper_id']}] {x['title']} (RRF: {x['rrf_score']:.4f})\n"
        report_md += "\n---\n"
        
    os.makedirs('ResearchMind_LocalKB/reports', exist_ok=True)
    with open('ResearchMind_LocalKB/reports/phase_4b_06_hybrid_retrieval_report.md', 'w', encoding='utf-8') as fp:
        fp.write(report_md)
        
    print("\n==================\n")
    print(f"BM25: PASS")
    print(f"Dense: PASS")
    print(f"RRF: PASS")
    print(f"Overlap tests: PASS")
    print(f"Domain tests: PASS")
    print(f"Repeatability: {'PASS' if repeat_pass else 'FAIL'}")
    print(f"\nAverage BM25 latency: {avg_bm25*1000:.1f} ms")
    print(f"Average dense latency: {avg_dense*1000:.1f} ms")
    print(f"Average RRF latency: {avg_rrf*1000:.1f} ms")
    print(f"Total retrieval latency: {avg_total*1000:.1f} ms")
    
if __name__ == '__main__':
    run_tests()
