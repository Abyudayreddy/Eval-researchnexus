import re

with open('backend/app/api/papers.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_block = """    (local_papers, is_sufficient, local_trace), (online_papers, online_trace) = await asyncio.gather(local_task, online_task, return_exceptions=True)
    
    # Handle exceptions gracefully to ensure one failure doesn't kill the other
    if isinstance(local_papers, Exception):
        local_papers, is_sufficient, local_trace = [], False, {"error": str(local_papers)}
    if isinstance(online_papers, Exception):
        print(f"ONLINE RETRIEVAL FAILED: {online_papers}")
        online_papers, online_trace = [], {"error": str(online_papers)}"""

new_block = """    results = await asyncio.gather(local_task, online_task, return_exceptions=True)
    
    # Handle exceptions gracefully to ensure one failure doesn't kill the other
    local_res = results[0]
    if isinstance(local_res, Exception):
        local_papers, is_sufficient, local_trace = [], False, {"error": str(local_res)}
    else:
        local_papers, is_sufficient, local_trace = local_res
        
    online_res = results[1]
    if isinstance(online_res, Exception):
        print(f"ONLINE RETRIEVAL FAILED: {online_res}")
        online_papers, online_trace = [], {"error": str(online_res)}
    else:
        online_papers, online_trace = online_res"""

c = c.replace(old_block, new_block)

with open('backend/app/api/papers.py', 'w', encoding='utf-8') as f:
    f.write(c)
