#!/usr/bin/env python3
import json

def inspect():
    with open('evaluation/module_02/raw/claims_raw.json', 'r', encoding='utf-8') as f:
        claims_raw = json.load(f)

    for idx in range(1, 23):
        c = claims_raw[idx-1]
        print(f"{idx:02d}. [{c['system'][:5]}|{c['query_id']}|{c['claim_id']}] cit:{c['citation_ids']} -> {c['support_status']}")
        print(f"    {c['claim_text']}")

if __name__ == '__main__':
    inspect()
