#!/usr/bin/env python3
import json

def inspect():
    with open('evaluation/module_02/raw/claims_raw.json', 'r', encoding='utf-8') as f:
        claims = json.load(f)
    print(f"Total claims: {len(claims)}")
    for i, c in enumerate(claims, 1):
        txt = c['claim_text'].replace('\n', ' ')
        print(f"{i:02d}. [{c['system'][:5]}|{c['query_id']}|{c['claim_id']}] {txt}")

if __name__ == '__main__':
    inspect()
