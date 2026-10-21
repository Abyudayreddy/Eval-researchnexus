#!/usr/bin/env python3
import json

def inspect_first_18():
    with open('evaluation/module_02/raw/claims_raw.json', 'r', encoding='utf-8') as f:
        claims = json.load(f)
    for i in range(1, 19):
        c = claims[i-1]
        txt = c['claim_text'].replace('\n', ' ')
        print(f"{i:02d}. [{c['system'][:5]}|{c['query_id']}|{c['claim_id']}] {txt}")

if __name__ == '__main__':
    inspect_first_18()
