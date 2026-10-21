import re

with open('backend/app/api/papers.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add BackgroundTasks import
if 'BackgroundTasks' not in content:
    content = content.replace('from fastapi import APIRouter, HTTPException, Depends', 'from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks')
    content = content.replace('from fastapi import APIRouter, HTTPException', 'from fastapi import APIRouter, HTTPException, BackgroundTasks')

# Extract search_papers block
match = re.search(r'(@router\.post\("/search"\)\s*async def search_papers\(request: SearchRequest\):[\s\S]*?)@router\.get\("/\{id\}"\)', content)
if not match:
    print("Could not find search_papers block")
else:
    original_block = match.group(1)
    
    # Let's write the new background task and new endpoint
    
    body = original_block.replace('@router.post("/search")\nasync def search_papers(request: SearchRequest):', '')
    
    # Everything after _update_experiment(... stage="initialized"...) needs to be indented for background task
    init_str = '    _update_experiment(search_id, overall_status="running", stage="initialized", progress=None)\n'
    idx = body.find(init_str) + len(init_str)
    
    background_body = body[idx:]
    
    # We replace the final `return` in background_body with an update to `_EXPERIMENTS`
    
    # Original return:
    return_str = """
    return {
        "search_id": str(search_id),
        "papers": mixed_papers[:15],
        "trace": mixed_trace,
        "retrieval_source": retrieval_source_val,
        "retrieval_mode": "local_online",
        "fallback_used": False,
        "local_status": local_status,
        "online_status": online_status,
        "local_result_count": len(local_papers),
        "online_result_count": len(online_papers),
        "combined_result_count": len(mixed_papers[:15]),
    }
"""
    # Wait, the indentation might be different. Let's just use regex to replace the final return.
    
    background_task = """
async def execute_search_experiment(search_id: uuid.UUID, request: SearchRequest):
""" + background_body

    background_task = re.sub(r'\s*return\s+\{.*\}\s*$', '', background_task, flags=re.DOTALL)
    
    # Append the results to the final _update_experiment
    old_update = """    _update_experiment(
        search_id,
        stage="merged",
        progress=100,
        overall_status="complete",
        local_status=local_status,
        online_status=online_status,
        combined_trace={"local_trace": local_trace, "online_trace": online_trace},
        combined_metrics={"merged_count": len(mixed_papers)}
    )"""
    new_update = """    _update_experiment(
        search_id,
        stage="merged",
        progress=100,
        overall_status="complete",
        local_status=local_status,
        online_status=online_status,
        combined_trace={"local_trace": local_trace, "online_trace": online_trace},
        combined_metrics={"merged_count": len(mixed_papers)},
        results=mixed_papers[:15],
        local_results=local_papers,
        online_results=online_papers,
        combined_results=mixed_papers[:15],
        local_result_count=len(local_papers),
        online_result_count=len(online_papers),
        combined_result_count=len(mixed_papers[:15])
    )"""
    background_task = background_task.replace(old_update, new_update)

    new_endpoint = """
@router.post("/search")
async def search_papers(request: SearchRequest, background_tasks: BackgroundTasks):
    search_id = uuid.uuid4()
    _init_experiment(search_id, request.query)
    _update_experiment(search_id, overall_status="running", stage="initialized", progress=None)

    background_tasks.add_task(execute_search_experiment, search_id, request)

    return {
        "search_id": str(search_id),
        "overall_status": "running"
    }
"""

    content = content.replace(original_block, background_task + new_endpoint + "\n")

    with open('backend/app/api/papers.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced successfully.")
