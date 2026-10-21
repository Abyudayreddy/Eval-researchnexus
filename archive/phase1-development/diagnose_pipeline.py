import urllib.request
import urllib.parse
import json
import time

API_URL = "http://localhost:8000/api"

def main():
    query = "Stock Price Prediction Using Triple Barrier Labeling"
    print(f"--- Diagnosing End-to-End Search Pipeline ---")
    print(f"Query: {query}")
    
    # 1. Start search
    data = json.dumps({
        "query": query,
        "search_mode": "hybrid",
        "retrieval_mode": "local_online"
    }).encode('utf-8')
    
    req = urllib.request.Request(f"{API_URL}/papers/search", data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=30.0) as resp:
            resp_data = json.loads(resp.read().decode('utf-8'))
            search_id = resp_data.get("search_id")
            print(f"Started search_id: {search_id}")
            print("Initial Search Response:")
            print(json.dumps(resp_data, indent=2))
    except Exception as e:
        print("Failed to start search:", e)
        return
        
    # 2. Poll until complete
    while True:
        try:
            req = urllib.request.Request(f"{API_URL}/papers/{search_id}/status")
            with urllib.request.urlopen(req, timeout=10.0) as resp:
                status_data = json.loads(resp.read().decode('utf-8'))
                overall = status_data.get("overall_status")
                
                if overall in ["complete", "failed", "partial"]:
                    print("\n--- FINAL STATUS DATA ---")
                    # Save status data to file for inspection
                    with open("debug_status.json", "w", encoding='utf-8') as f:
                        json.dump(status_data, f, indent=2)
                        
                    print(f"Overall Status: {overall}")
                    print(f"Local Status: {status_data.get('local_status')}")
                    print(f"Online Status: {status_data.get('online_status')}")
                    
                    # Inspect what results are returned
                    local_results = status_data.get('local_results', [])
                    online_results = status_data.get('online_results', [])
                    combined_results = status_data.get('combined_results', status_data.get('results', []))
                    
                    print(f"\nLocal Results count in payload: {len(local_results)}")
                    for r in local_results:
                        print(f"  - [{r.get('id', r.get('paper_id'))}] {r.get('title')[:60]}... (source: {r.get('retrieval_source')})")
                        
                    print(f"\nOnline Results count in payload: {len(online_results)}")
                    for r in online_results:
                        print(f"  - [{r.get('id', r.get('paper_id'))}] {r.get('title')[:60]}... (source: {r.get('retrieval_source')})")
                        
                    print(f"\nCombined Results count in payload: {len(combined_results)}")
                    for r in combined_results:
                        print(f"  - [{r.get('id', r.get('paper_id'))}] {r.get('title')[:60]}... (source: {r.get('retrieval_source')})")
                        
                    break
        except Exception as e:
            print("Poll error:", e)
            
        time.sleep(1.0)

if __name__ == "__main__":
    main()
