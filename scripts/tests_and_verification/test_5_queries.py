import urllib.request
import urllib.parse
import json
import time

API_URL = "http://localhost:8000/api"

queries = [
    {
        "q": "AI-Powered Extremism Jihadist Propaganda in Indonesia",
        "expected_id": "10.1355/9789815361513-003",
        "desc": "Query 1: Distinctive title phrase"
    },
    {
        "q": "Who Speaks Matters Authority-Aware Multi-View RAG Mirko Tritella",
        "expected_id": "2608.13410v1",
        "desc": "Query 2: Title + Author"
    },
    {
        "q": "favorable view of a firm shaped by its social",
        "expected_id": "2507.05782v1",
        "desc": "Query 3: Distinctive abstract phrase"
    },
    {
        "q": "Stock Price Prediction Using Triple Barrier Labeling Raw OHLCV",
        "expected_id": "2504.02249v2",
        "desc": "Query 4: Domain + distinctive concept"
    },
    {
        "q": "clinical trial management using reinforcement-based agentic intelligence",
        "expected_id": "10.2196/preprints.78741",
        "desc": "Query 5: Semantic paraphrase"
    }
]

def test_search(query_info):
    print(f"\n==========================================")
    print(f"--- Testing: {query_info['desc']} ---")
    print(f"Query: {query_info['q']}")
    print(f"Expected ID: {query_info['expected_id']}")
    
    # 1. Start search
    data = json.dumps({
        "query": query_info['q'],
        "search_mode": "hybrid",
        "retrieval_mode": "local_online"  # We still use local_online but we will check local_results specifically
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
                    local_status = status_data.get('local_status')
                    print(f"Local Status: {local_status}")
                    
                    # Dump local trace and results
                    local_trace = status_data.get('trace', {}).get('local_trace', {})
                    if not local_trace:
                        local_trace = status_data.get('local', {}).get('trace', {})
                    
                    local_results = status_data.get('local_results', [])
                    if not local_results:
                        local_results = [r for r in status_data.get('results', []) if r.get('retrieval_source') == 'local']
                    
                    found = False
                    for r in local_results:
                        pid = r.get("id") or r.get("paper_id")
                        if pid == query_info['expected_id']:
                            found = True
                            print("EXPECTED PAPER FOUND IN FINAL LOCAL RESULTS!")
                            print("Title:", r.get("title"))
                            print("Retrieval Source:", r.get("retrieval_source"))
                            break
                    if not found:
                        print("EXPECTED PAPER NOT FOUND IN FINAL LOCAL RESULTS.")
                    
                    print(f"Local Trace: {json.dumps(local_trace, indent=2)}")
                    break
        except Exception as e:
            print("Poll error:", e)
            
        time.sleep(1.0)

def main():
    for q in queries:
        test_search(q)
        time.sleep(1)

if __name__ == "__main__":
    main()
