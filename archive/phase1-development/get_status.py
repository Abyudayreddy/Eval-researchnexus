import requests, json

try:
    search_id = '2232ae5d-5f4d-4d60-b43d-45b1f805c1f2'
    r2 = requests.get(f'http://127.0.0.1:8000/api/papers/{search_id}/status')
    with open('status_dump.json', 'w', encoding='utf-8') as f:
        json.dump(r2.json(), f, indent=2)
except Exception as e:
    print(e)
