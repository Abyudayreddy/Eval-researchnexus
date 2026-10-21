import requests
import json

search_id = "28aaf867-6088-47b4-ade6-4d3c4f88779b"
r = requests.get(f"http://localhost:8000/api/papers/{search_id}/status")
print(json.dumps(r.json(), indent=2))
