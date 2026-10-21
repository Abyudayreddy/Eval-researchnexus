import requests

try:
    res = requests.post('http://127.0.0.1:8000/api/papers/search', json={'query': 'retrieval augmented generation', 'search_mode': 'hybrid'})
    data = res.json()
    search_id = data.get('search_id')
    print("Search ID:", search_id)
    
    import time
    for i in range(15):
        time.sleep(1)
        r2 = requests.get(f'http://127.0.0.1:8000/api/papers/{search_id}/status')
        d2 = r2.json()
        if d2.get('overall_status') in ['complete', 'failed']:
            import json
            print(json.dumps(d2.get('trace', {}).get('local_trace', {}), indent=2))
            break
except Exception as e:
    print(e)
