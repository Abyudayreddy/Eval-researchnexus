import asyncio
import uuid
import json
import time
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.models.paper import Paper, PaperChunk
from app.models.search_experiment import SearchExperiment
from app.services.local_evidence import get_local_retriever
from app.services.llm_provider import LLMProviderManager

def run_full_verification():
    print("============================================================")
    print("STARTING FULL END-TO-END RUNTIME VALIDATION")
    print("============================================================\n")

    client = TestClient(app)

    # PHASE 1: Confirm DB & Local Retriever
    print("--- PHASE 1: INFRASTRUCTURE & RETRIEVAL READINESS ---")
    db = SessionLocal()
    try:
        paper_count = db.query(Paper).count()
        chunk_count = db.query(PaperChunk).count()
        print(f"PostgreSQL Connection: OK | Local Papers: {paper_count} | Chunks: {chunk_count}")
    finally:
        db.close()

    local_retriever = get_local_retriever()
    if local_retriever.init_status != "ready":
        print("Loading local retriever...")
        local_retriever.load()
    print(f"Local Retriever Status: {local_retriever.init_status}")

    # PHASE 2: REAL EXPLORER SEARCH
    print("\n--- PHASE 2: REAL EXPLORER SEARCH ---")
    query = "trace evidence retrieval systems"
    search_payload = {
        "query": query,
        "search_mode": "hybrid",
        "retrieval_mode": "hybrid",
        "publication_year": None,
        "sort_by": "relevance",
        "domain": None
    }
    
    t_search_start = time.time()
    search_res = client.post("/papers/search", json=search_payload)
    print(f"Search HTTP Status: {search_res.status_code}")
    search_data = search_res.json()
    
    search_id = search_data.get("search_id")
    execution_id = search_data.get("execution_id")
    print(f"search_id: {search_id}")
    print(f"execution_id: {execution_id}")

    # Poll status until terminal
    max_wait = 30
    elapsed = 0
    status_data = {}
    while elapsed < max_wait:
        time.sleep(1)
        elapsed += 1
        st_res = client.get(f"/papers/{search_id}/status")
        if st_res.status_code == 200:
            status_data = st_res.json()
            exec_state = status_data.get("execution_state")
            if exec_state in ["COMPLETED_WITH_RESULTS", "COMPLETED_NO_RESULTS", "DEGRADED", "FAILED"]:
                print(f"Search reached terminal state: {exec_state} in {elapsed}s")
                break

    results = status_data.get("results", [])
    local_count = status_data.get("local_result_count", 0)
    online_count = status_data.get("online_result_count", 0)
    combined_count = status_data.get("combined_result_count", len(results))
    print(f"Results summary: Total {len(results)} | Local: {local_count} | Online: {online_count}")

    # PHASE 3: VERIFY EXPLORER EVIDENCE
    print("\n--- PHASE 3: INSPECT EXPLORER EVIDENCE ---")
    raw_evidence_count = len(results)
    eligible_evidence_count = 0
    dropped_evidence_count = 0
    
    for idx, p in enumerate(results[:5]):
        pid = p.get("id") or p.get("paper_id")
        title = p.get("title", "Untitled")
        abstract = p.get("abstract") or p.get("evidence_text") or ""
        stype = p.get("retrieval_source", "local")
        if len(abstract.strip()) > 10:
            eligible_evidence_count += 1
        else:
            dropped_evidence_count += 1
        print(f"  [Evidence {idx+1}] ID: {pid} | Source: {stype} | Title: {title[:50]}... | Text Length: {len(abstract)}")

    # PHASE 4: CLICK ASK AI (SIMULATED VIA EXACT HANDOFF PAYLOAD)
    print("\n--- PHASE 4 & 5: ASK AI WITH EXPLORER CONTEXT (NO SECOND SEARCH) ---")
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

    t_ask_start = time.time()
    ask_res = client.post("/ai/ask", json=ask_payload)
    ask_latency = time.time() - t_ask_start
    print(f"Ask AI HTTP Status: {ask_res.status_code} (Latency: {ask_latency:.2f}s)")
    
    if ask_res.status_code != 200:
        print(f"Ask AI Failed: {ask_res.text}")
        return

    ask_data = ask_res.json()
    answer = ask_data.get("answer", "")
    gen_status = ask_data.get("generation_status")
    claims = ask_data.get("claims", [])
    citations = ask_data.get("citations", [])
    evidence = ask_data.get("evidence", [])
    sources = ask_data.get("sources", [])
    manifest = ask_data.get("evidence_manifest", {})

    print(f"\n--- PHASE 6, 7 & 8: ENHANCED RAG & GEMINI RESPONSE ---")
    print(f"Generation Status: {gen_status}")
    print(f"Evidence Items Sent to LLM / Bounded: {len(evidence)}")
    print(f"Grounded Sources: {len(sources)}")
    print(f"Answer Preview:\n{answer[:300]}...\n")

    # PHASE 9: CLAIM VERIFICATION
    print("--- PHASE 9: CLAIM VERIFICATION METRICS ---")
    print(f"Total Claims Extracted: {len(claims)}")
    for c in claims[:3]:
        print(f"  Claim: {c.get('claim_text')[:60]}... | Status: {c.get('status')} | Direct: {c.get('is_direct_evidence')}")

    # PHASE 10: CITATION VALIDATION
    print("\n--- PHASE 10: CITATIONS ---")
    print(f"Total Citations: {len(citations)}")
    for cit in citations[:3]:
        print(f"  Citation: {cit.get('citation_id')} -> Paper: {cit.get('title')[:40]}... (ID: {cit.get('paper_id')})")

    # PHASE 12: TEST INSUFFICIENT EVIDENCE (NEGATIVE TEST)
    print("\n--- PHASE 12: NEGATIVE TEST (INSUFFICIENT EVIDENCE CHECK) ---")
    neg_payload = {
        "query": "quantum gravity entanglement black hole horizon information paradox",
        "mode": "research",
        "scope": "current_evidence",
        "evidence_ids": [],
        "session_id": "session-empty"
    }
    neg_res = client.post("/ai/ask", json=neg_payload)
    print(f"Negative Test Status: {neg_res.status_code}")
    if neg_res.status_code == 200:
        neg_data = neg_res.json()
        print(f"Negative Test Answer: {neg_data.get('answer')}")
        print(f"Negative Test Generation Status: {neg_data.get('generation_status')}")

    # PHASE 16: DIRECT ASSISTANT WORKFLOW (NO EXPLORER CONTEXT)
    print("\n--- PHASE 16: DIRECT ASSISTANT WORKFLOW ---")
    direct_payload = {
        "query": "What is digital forensics?",
        "search_mode": "hybrid"
    }
    direct_res = client.post("/ai/ask", json=direct_payload)
    print(f"Direct Assistant HTTP Status: {direct_res.status_code}")
    if direct_res.status_code == 200:
        direct_data = direct_res.json()
        print(f"Direct Assistant Answer Preview: {direct_data.get('answer', '')[:150]}...")

    print("\n============================================================")
    print("END-TO-END VALIDATION EXECUTION COMPLETE")
    print("============================================================")

if __name__ == "__main__":
    run_full_verification()
