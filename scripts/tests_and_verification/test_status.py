import urllib.request
import urllib.parse
import json
import time

API_URL = "http://localhost:8000/api"

def test_search(query: str, desc: str):
    print(f"\n--- Testing: {desc} ---")
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
                    print(f"Overall Status: {overall}")
                    print(f"Local Status: {status_data.get('local_status')}")
                    print(f"Online Status: {status_data.get('online_status')}")
                    
                    local_count = status_data.get('local_result_count', 0)
                    online_count = status_data.get('online_result_count', 0)
                    print(f"Local Count: {local_count}, Online Count: {online_count}")
                    break
        except Exception as e:
            print("Poll error:", e)
            
        time.sleep(1.0)

def main():
    # 1. Known local topic (should have results)
    test_search("attention", "Query A: Known local topic")
    
    # 2. Unlikely local topic (0 results)
    test_search("ancient roman agriculture methods", "Query B: Unlikely local topic")

if __name__ == "__main__":
    main()
