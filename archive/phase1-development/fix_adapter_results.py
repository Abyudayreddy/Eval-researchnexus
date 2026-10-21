import re

with open('src/utils/apiAdapter.ts', 'r', encoding='utf-8') as f:
    content = f.read()

if 'results: raw.results || []' not in content:
    content = content.replace("trace: raw.trace || {}", "trace: raw.trace || {},\n    results: raw.results || raw.papers || []")
    content = content.replace("trace: { local_trace?: any; online_trace?: any; combined_trace?: any };", "trace: { local_trace?: any; online_trace?: any; combined_trace?: any };\n  results?: any[];")
    
    with open('src/utils/apiAdapter.ts', 'w', encoding='utf-8') as f:
        f.write(content)
