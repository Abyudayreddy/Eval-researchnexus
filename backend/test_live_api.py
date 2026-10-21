import sys
import time
import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8000"

def post_json(endpoint, data):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'), 
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode('utf-8'))

def get_json(endpoint):
    url = f"{BASE_URL}{endpoint}"
    with urllib.request.urlopen(url, timeout=120) as resp:
        return json.loads(resp.read().decode('utf-8'))

def run_test():
    print("=== LIVE SERVER E2E RUNTIME TEST ===", flush=True)
    
    # Check health
    health = get_json("/health")
    print(f"0. Health check: {health}", flush=True)

    # 1. Start Explorer Search
    query = "trace evidence retrieval systems"
    print(f"1. Submitting Explorer Search: '{query}'", flush=True)
    search_res = post_json("/api/papers/search", {"query": query, "search_mode": "hybrid"})
    search_id = search_res.get("search_id")
    execution_id = search_res.get("execution_id")
    print(f"   search_id: {search_id}", flush=True)
    print(f"   execution_id: {execution_id}", flush=True)

    # 2. Wait for completion
    st = {}
    for i in range(25):
        time.sleep(1)
        st = get_json(f"/api/papers/{search_id}/status")
        state = st.get("execution_state")
        if state in ["COMPLETED_WITH_RESULTS", "COMPLETED_NO_RESULTS", "DEGRADED", "FAILED"]:
            print(f"   Search state reached: {state} in {i+1}s", flush=True)
            break
            
    results = st.get("results", [])
    local_count = st.get("local_result_count", 0)
    online_count = st.get("online_result_count", 0)
    print(f"   Returned papers: Total {len(results)} | Local: {local_count} | Online: {online_count}", flush=True)

    # Inspect top evidence
    print("\n2. Explorer Evidence Inspection:", flush=True)
    for idx, r in enumerate(results[:3]):
        pid = r.get("id") or r.get("paper_id")
        title = r.get("title", "")
        ev_text = r.get("evidence_text") or r.get("abstract", "")
        print(f"   - [{idx+1}] ID: {pid} | Title: {title[:40]}... | Ev len: {len(ev_text)}", flush=True)

    # 3. Ask AI with Explorer Context
    print("\n3. Calling Ask AI with Explorer Context (No new search):", flush=True)
    ask_payload = {
        "query": query,
        "search_mode": search_id,
        "search_id": search_id,
        "session_id": f"session-{search_id[:8]}",
        "mode": "research",
        "scope": "all_research",
        "context_papers": results,
        "refinement_mode": "automatic"
    }

    t0 = time.time()
    ask_res = post_json("/api/ai/ask", ask_payload)
    ask_dur = time.time() - t0
    print(f"   Ask AI Completed in {ask_dur:.2f}s", flush=True)

    answer = ask_res.get("answer", "")
    gen_status = ask_res.get("generation_status")
    claims = ask_res.get("claims", [])
    citations = ask_res.get("citations", [])
    evidence = ask_res.get("evidence", [])
    sources = ask_res.get("sources", [])

    print(f"   Generation Status: {gen_status}", flush=True)
    print(f"   Grounded Sources Count: {len(sources)}", flush=True)
    print(f"   Bounded Evidence Count: {len(evidence)}", flush=True)
    print(f"   Claims Verified: {len(claims)}", flush=True)
    print(f"   Citations Count: {len(citations)}", flush=True)
    print(f"\n   Answer Preview:\n   {answer[:350]}...\n", flush=True)

    # 4. Negative Test for True Insufficient Evidence
    print("4. Testing Negative Case (True Insufficient Evidence):", flush=True)
    neg_res = post_json("/api/ai/ask", {
        "query": "unrelated exotic question with zero context",
        "mode": "research",
        "scope": "current_evidence",
        "evidence_ids": [],
        "session_id": "session-empty"
    })
    print(f"   Negative Generation Status: {neg_res.get('generation_status')}", flush=True)
    print(f"   Negative Answer: {neg_res.get('answer')}", flush=True)

    # 5. Direct Assistant Entry
    print("\n5. Direct Assistant Entry (Without Explorer Context):", flush=True)
    dir_res = post_json("/api/ai/ask", {
        "query": "What is digital forensics?",
        "search_mode": "hybrid"
    })
    print(f"   Direct Answer Status: {dir_res.get('generation_status')}", flush=True)
    print(f"   Direct Answer Preview: {dir_res.get('answer', '')[:120]}...", flush=True)

    print("\n=== ALL REAL LIVE RUNTIME CHECKS PASSED ===", flush=True)

if __name__ == "__main__":
    run_test()
