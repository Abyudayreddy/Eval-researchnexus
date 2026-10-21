import requests

r = requests.post("http://localhost:8000/api/papers/search", json={
    "query": "clinical trial management",
    "search_mode": "hybrid",
    "retrieval_mode": "local_online"
})
print(r.json())
