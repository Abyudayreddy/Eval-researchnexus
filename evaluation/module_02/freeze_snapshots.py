#!/usr/bin/env python3
"""
ResearchNexus AI - Freeze Context Snapshots for Module 2 Evaluation
Freezes the exact retrieved chunks, text, ordering, and context SHA-256 hashes
for all 15 TEST queries from the canonical Module 1 B3 candidate retrieval pool.
"""

import os
import sys
import json
import hashlib

def main():
    # Load benchmark manifest
    with open('evaluation/module_01/benchmark_manifest.json', 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    test_manifest_queries = {q['query_id']: q for q in manifest['queries']}

    # Load all chunks
    all_chunks = {}
    for root, dirs, files in os.walk('ResearchMind_LocalKB'):
        for f in files:
            if f.endswith('.json'):
                p = os.path.join(root, f)
                try:
                    with open(p, encoding='utf-8') as fh:
                        data = json.load(fh)
                        if isinstance(data, list):
                            for item in data:
                                if isinstance(item, dict) and 'chunk_id' in item:
                                    all_chunks[item['chunk_id']] = item
                except Exception:
                    pass

    # Load raw queries from e03
    with open('research_artifacts/retrieval_evaluation/v11/e03_candidate_recall/e03_raw_per_query.json', 'r', encoding='utf-8') as f:
        raw_queries = json.load(f)
    b3_k20 = [q for q in raw_queries if q.get('config') == 'B3_Hybrid_RRF' and q.get('k') == 20 and q.get('split') == 'TEST']
    b3_k20.sort(key=lambda x: x['query_id'])

    os.makedirs('evaluation/module_02/context_snapshots', exist_ok=True)

    snapshots = []
    for q in b3_k20:
        qid = q['query_id']
        retrieved_chunk_ids = q.get('retrieved_chunk_ids', [])
        deduplicated_evidence = []
        seen = set()
        for rank, cid in enumerate(retrieved_chunk_ids, 1):
            if cid in seen:
                continue
            seen.add(cid)
            c_obj = all_chunks.get(cid, {})
            text = c_obj.get('text', '')
            pid = c_obj.get('paper_id', cid.split('#')[0] if '#' in cid else cid)
            title = c_obj.get('topic', c_obj.get('title', pid))
            deduplicated_evidence.append({
                'retrieval_rank': rank,
                'id': pid,
                'paper_id': pid,
                'chunk_id': cid,
                'title': title,
                'authors': c_obj.get('authors', 'ResearchNexus Corpus'),
                'evidence_text': text,
                'section': c_obj.get('section', 'General'),
                'source_type': 'local',
                'retrieval_source': 'local',
                'evidence_status': 'evidence_ready'
            })
        
        context_text = ""
        citation_map = {}
        for idx, ev in enumerate(deduplicated_evidence, 1):
            c_id = f"[{idx}]"
            context_text += (
                f"CITATION {c_id}:\n"
                f"Paper: {ev['title']}\n"
                f"Evidence: {ev['evidence_text']}\n\n"
            )
            citation_map[c_id] = ev

        chash = hashlib.sha256(context_text.encode('utf-8')).hexdigest()
        snapshot_record = {
            'query_id': qid,
            'split': 'TEST',
            'query_text': test_manifest_queries[qid]['query_text'],
            'expected_paper_ids': test_manifest_queries[qid]['expected_paper_ids'],
            'expected_evidence_ids': test_manifest_queries[qid]['expected_evidence_ids'],
            'retrieved_chunk_ids': retrieved_chunk_ids,
            'deduplicated_chunk_count': len(deduplicated_evidence),
            'context_hash': chash,
            'context_text': context_text,
            'evidence_items': deduplicated_evidence
        }
        snapshots.append(snapshot_record)
        with open(f'evaluation/module_02/context_snapshots/{qid}_snapshot.json', 'w', encoding='utf-8') as out_f:
            json.dump(snapshot_record, out_f, indent=2)

    with open('evaluation/module_02/context_snapshots/all_test_snapshots.json', 'w', encoding='utf-8') as out_f:
        json.dump(snapshots, out_f, indent=2)

    print(f'Successfully frozen {len(snapshots)} context snapshots.')

if __name__ == '__main__':
    main()
