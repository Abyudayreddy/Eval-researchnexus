import os, sys, requests

url = "http://localhost:8000/api/papers/search"
payload = {
    "query": "Stock Price Prediction Using Triple Barrier Labeling",
    "search_mode": "hybrid",
    "retrieval_mode": "local_online",
    "deep_evidence": False
}
try:
    resp = requests.post(url, json=payload, timeout=5)
    data = resp.json()
    sid = data.get("search_id")
    print("Search ID:", sid)
    
    import time
    for _ in range(5):
        time.sleep(1)
        r2 = requests.get(f"http://localhost:8000/api/papers/{sid}/status")
        d2 = r2.json()
        print(d2.get("local"))
        if d2.get("local", {}).get("status") in ["complete", "failed", "no_results"]:
            print("TRACE:", d2.get("trace", {}).get("local_trace"))
            break
except Exception as e:
    print("Error:", e)
