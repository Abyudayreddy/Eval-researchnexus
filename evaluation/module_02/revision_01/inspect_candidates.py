#!/usr/bin/env python3
import json

def inspect_candidates():
    with open('evaluation/module_02/raw/claims_raw.json', 'r', encoding='utf-8') as f:
        claims = json.load(f)

    for i, c in enumerate(claims, 1):
        txt = c['claim_text']
        lower = txt.lower()
        if "scaling challenges" in lower or "loss function" in lower or "contrastive" in lower:
            print(f"Index {i}: [{c['system']}|{c['query_id']}|{c['claim_id']}]")
            print(f"   {txt}\n")

if __name__ == '__main__':
    inspect_candidates()
