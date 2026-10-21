import os, sys, requests, time

url = "http://localhost:8000/api/papers/search"
payload = {
    "query": "Stock Price Prediction Using Triple Barrier Labeling",
    "search_mode": "hybrid",
    "retrieval_mode": "local_online",
    "deep_evidence": False
}
try:
    print("Sending POST /search")
    resp = requests.post(url, json=payload)
    data = resp.json()
    sid = data.get("search_id")
    print("Search ID:", sid)
    
    for _ in range(10):
        time.sleep(1)
        r2 = requests.get(f"http://localhost:8000/api/papers/{sid}/status")
        d2 = r2.json()
        print("local_status:", d2.get("local_status"))
        
        local_trace = d2.get("local_trace") or d2.get("trace", {}).get("local_trace") or {}
        combined_trace = d2.get("combined_trace") or d2.get("trace", {}).get("combined_trace") or {}
        if not local_trace and combined_trace:
            local_trace = combined_trace.get("local_trace", {})
            
        if d2.get("local_status") in ["complete", "failed", "no_results"]:
            print("LOCAL TRACE ERROR:", local_trace.get("error"))
            print("LOCAL TRACE STR:", str(local_trace)[:500])
            break
except Exception as e:
    print("Error:", e)
