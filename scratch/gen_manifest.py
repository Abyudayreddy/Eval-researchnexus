import json

path = 'research_artifacts/benchmark_v11/benchmark_items.json'
with open(path, 'r', encoding='utf-8') as f:
    items = json.load(f)

test_items = [it for it in items if it.get('split') == 'TEST']

manifest = {
    'benchmark_version': 'ds_nexus_v11',
    'split': 'TEST',
    'number_of_queries': len(test_items),
    'number_with_paper_gold': sum(1 for it in test_items if len(it.get('expected_paper_ids', [])) > 0),
    'number_with_evidence_gold': sum(1 for it in test_items if len(it.get('expected_evidence_ids', [])) > 0),
    'average_gold_papers': sum(len(it.get('expected_paper_ids', [])) for it in test_items) / float(len(test_items)),
    'average_gold_evidence': sum(len(it.get('expected_evidence_ids', [])) for it in test_items) / float(len(test_items)),
    'queries': []
}

for it in test_items:
    manifest['queries'].append({
        'query_id': it['item_id'],
        'query_text': it['question'],
        'domain': it.get('domain', 'Artificial Intelligence'),
        'question_type': it.get('type', 'FACTUAL'),
        'difficulty': it.get('difficulty', 'MEDIUM'),
        'expected_paper_ids': it.get('expected_paper_ids', []),
        'expected_evidence_ids': it.get('expected_evidence_ids', []),
        'split': it['split'],
        'benchmark_version': 'ds_nexus_v11'
    })

with open('evaluation/module_01/benchmark_manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)

print("Benchmark manifest created successfully!")
print("Queries count:", manifest['number_of_queries'])
print("Avg gold papers:", manifest['average_gold_papers'])
print("Avg gold evidence:", manifest['average_gold_evidence'])
