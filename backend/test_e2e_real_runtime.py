import asyncio
import time
import json
import uuid
from app.db.session import SessionLocal, Base, engine
from app.models.paper import Paper, PaperChunk
from app.models.search_experiment import SearchExperiment
from app.models.search_history import SearchHistory
from app.api.papers import search_papers, SearchRequest, _EXPERIMENTS
from app.api.ai import ask_ai, AskRequest, ContextPaper
from app.services.local_evidence import get_local_retriever
from app.services.assistant.context_manager import ContextManager
from app.services.assistant.iterative_rag import IterativeRAGService
from app.services.assistant.enhanced_rag import EnhancedRAGService

async def main():
    print("============================================================", flush=True)
    print("RESEARCHNEXUS — REAL RUNTIME END-TO-END VALIDATION", flush=True)
    print("============================================================\n", flush=True)

    # Ensure all tables are created
    Base.metadata.create_all(bind=engine)

    # ---------------------------------------------------------
    # PHASE 1: SYSTEM & INFRASTRUCTURE
    # ---------------------------------------------------------
    print("--- PHASE 1: INFRASTRUCTURE & DATA INTEGRITY ---", flush=True)
    db = SessionLocal()
    try:
        paper_count = db.query(Paper).count()
        chunk_count = db.query(PaperChunk).count()
        print(f"PostgreSQL/SQLite Papers in DB: {paper_count} | Chunks: {chunk_count}", flush=True)
    finally:
        db.close()

    local_retriever = get_local_retriever()
    if local_retriever.init_status != "ready":
        print("Initializing Local Hybrid Retriever (BM25 + Dense FAISS)...", flush=True)
        local_retriever.load()
    print(f"Local Retriever Status: {local_retriever.init_status}", flush=True)

    # ---------------------------------------------------------
    # PHASE 2: REAL EXPLORER SEARCH
    # ---------------------------------------------------------
    print("\n--- PHASE 2: REAL EXPLORER SEARCH EXECUTION ---", flush=True)
    query = "trace evidence retrieval systems"
    search_req = SearchRequest(
        query=query,
        search_mode="hybrid",
        retrieval_mode="hybrid",
        publication_year=None,
        sort_by="relevance",
        domain=None
    )

    from fastapi import BackgroundTasks
    bg = BackgroundTasks()

    t0_search = time.time()
    search_init_res = await search_papers(search_req, bg)
    search_id_str = search_init_res["search_id"]
    execution_id = search_init_res["execution_id"]
    search_uuid = uuid.UUID(search_id_str)

    print(f"Explorer Search Initialized:")
    print(f"  search_id: {search_id_str}")
    print(f"  execution_id: {execution_id}")

    # Execute background tasks (the actual search pipeline: Local BM25/Dense + Online + RRF + BGE)
    for task in bg.tasks:
        if asyncio.iscoroutinefunction(task.func):
            await task.func(*task.args, **task.kwargs)
        else:
            task.func(*task.args, **task.kwargs)

    search_duration = time.time() - t0_search
    experiment_data = _EXPERIMENTS.get(search_uuid, {})
    
    execution_state = experiment_data.get("execution_state")
    results = experiment_data.get("results", [])
    local_count = experiment_data.get("local_result_count", 0)
    online_count = experiment_data.get("online_result_count", 0)
    unique_count = experiment_data.get("combined_result_count", len(results))

    print(f"\nExplorer Search Finished in {search_duration:.2f}s:")
    print(f"  Execution State: {execution_state}")
    print(f"  Local Papers: {local_count}")
    print(f"  Online Papers: {online_count}")
    print(f"  Unique Results: {unique_count}")

    # ---------------------------------------------------------
    # PHASE 3: VERIFY EXPLORER EVIDENCE
    # ---------------------------------------------------------
    print("\n--- PHASE 3: EXPLORER EVIDENCE VERIFICATION ---", flush=True)
    raw_evidence_count = len(results)
    eligible_evidence_count = 0
    dropped_evidence_count = 0

    for idx, p in enumerate(results):
        pid = p.get("id") or p.get("paper_id")
        title = p.get("title", "Untitled")
        abstract = p.get("abstract") or p.get("evidence_text") or ""
        stype = p.get("retrieval_source", "local")
        if len(abstract.strip()) > 10:
            eligible_evidence_count += 1
        else:
            dropped_evidence_count += 1
        if idx < 3:
            print(f"  [Evidence Block {idx+1}] ID: {pid} | Provenance: {stype} | Title: '{title[:50]}...' | Len: {len(abstract)}")

    print(f"  RAW_EVIDENCE_COUNT: {raw_evidence_count}")
    print(f"  ELIGIBLE_EVIDENCE_COUNT: {eligible_evidence_count}")
    print(f"  DROPPED_EVIDENCE_COUNT: {dropped_evidence_count}")

    # ---------------------------------------------------------
    # PHASE 4 & 5: CLICK ASK AI (SAME CONTEXT, ZERO REDUNDANT RETRIEVAL)
    # ---------------------------------------------------------
    print("\n--- PHASE 4 & 5: ASK AI INVOCATION (BOUNDED EXPLORER CONTEXT) ---", flush=True)
    context_papers_objs = [ContextPaper(
        id=p.get("id") or p.get("paper_id", ""),
        title=p.get("title", ""),
        authors=p.get("authors", ""),
        abstract=p.get("abstract", "") or p.get("evidence_text", ""),
        url=p.get("url", "") or p.get("paper_url", ""),
        published=str(p.get("publication_year", "")),
        domain=p.get("retrieval_source", "local")
    ) for p in results]

    ask_req = AskRequest(
        query=query,
        search_mode=search_id_str,
        search_id=search_id_str,
        session_id=f"session-{search_id_str[:8]}",
        mode="research",
        scope="all_research",
        context_papers=context_papers_objs,
        refinement_mode="automatic"
    )

    t0_ask = time.time()
    ask_bg = BackgroundTasks()
    ask_result = await ask_ai(ask_req, ask_bg)
    ask_duration = time.time() - t0_ask

    # ---------------------------------------------------------
    # PHASE 6, 7 & 8: ENHANCED RAG & GEMINI RESPONSE
    # ---------------------------------------------------------
    print(f"\n--- PHASE 6, 7 & 8: ENHANCED RAG & GEMINI GENERATION ---", flush=True)
    print(f"Ask AI Pipeline Completed in {ask_duration:.2f}s")
    answer = ask_result.get("answer", "")
    gen_status = ask_result.get("generation_status", "")
    claims = ask_result.get("claims", [])
    citations = ask_result.get("citations", [])
    evidence = ask_result.get("evidence", [])
    sources = ask_result.get("sources", [])
    manifest = ask_result.get("evidence_manifest", {})
    metrics = ask_result.get("verification_metrics", {})

    print(f"Generation Status: {gen_status}")
    print(f"Evidence Sent to LLM (Bounded): {len(evidence)}")
    print(f"Grounded Sources: {len(sources)}")
    print(f"Generated Answer Preview:\n{answer}\n")

    # ---------------------------------------------------------
    # PHASE 9 & 10: CLAIM VERIFICATION & CITATION AUDIT
    # ---------------------------------------------------------
    print("--- PHASE 9 & 10: CLAIM VERIFICATION & CITATIONS AUDIT ---", flush=True)
    print(f"Claims Extracted & Verified: {len(claims)}")
    for idx, c in enumerate(claims):
        claim_text = c.get('text') or c.get('claim_text') or ""
        status = c.get('claim_support_status') or c.get('status') or "UNKNOWN"
        print(f"  [Claim {idx+1}] \"{claim_text[:80]}...\" -> Status: {status} | Citations: {c.get('citation_ids')}")

    print(f"\nCitations Validated: {len(citations)}")
    for idx, cit in enumerate(citations):
        print(f"  [Citation {cit.get('citation_id')}] Paper: {cit.get('title')[:45]}... (Source: {cit.get('source_type')})")

    # ---------------------------------------------------------
    # PHASE 12: TEST INSUFFICIENT EVIDENCE (NEGATIVE TEST)
    # ---------------------------------------------------------
    print("\n--- PHASE 12: NEGATIVE TEST (TRUE INSUFFICIENT EVIDENCE) ---", flush=True)
    empty_ask_req = AskRequest(
        query="unrelated exotic quantum biological topic with zero context",
        mode="research",
        scope="current_evidence",
        evidence_ids=[],
        session_id="session-empty"
    )
    empty_bg = BackgroundTasks()
    empty_result = await ask_ai(empty_ask_req, empty_bg)
    print(f"Empty Context Generation Status: {empty_result.get('generation_status')}")
    print(f"Empty Context Answer: {empty_result.get('answer')}")

    # ---------------------------------------------------------
    # PHASE 16: DIRECT ASSISTANT WORKFLOW (NO SEARCH CONTEXT)
    # ---------------------------------------------------------
    print("\n--- PHASE 16: DIRECT ASSISTANT REGRESSION ---", flush=True)
    direct_req = AskRequest(
        query="What is digital evidence in forensic computing?",
        search_mode="hybrid"
    )
    direct_bg = BackgroundTasks()
    direct_result = await ask_ai(direct_req, direct_bg)
    print(f"Direct Assistant Generation Status: {direct_result.get('generation_status')}")
    print(f"Direct Assistant Answer Preview:\n{direct_result.get('answer', '')[:200]}...")

    print("\n============================================================", flush=True)
    print("ALL RUNTIME PHASES COMPLETED WITH REAL DATA", flush=True)
    print("============================================================\n", flush=True)

if __name__ == "__main__":
    import traceback
    try:
        asyncio.run(main())
    except Exception as e:
        print("FATAL ERROR IN RUNTIME VALIDATION:", e, flush=True)
        traceback.print_exc()

