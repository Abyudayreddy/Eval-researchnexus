import re

with open('src/pages/HybridSearchPage.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the retrievalMeta logic in performSearch
new_logic = """
      if (response.papers || response.results) {
        setResults(response.papers || response.results || []);
      }
      
      setRetrievalMeta({
        retrieval_source: response.retrieval_source || 'mixed',
        local_status: response.local_status || 'success',
        online_status: response.online_status || 'success',
        local_count: response.local_result_count || 0,
        online_count: response.online_result_count || 0,
        combined_count: response.combined_result_count || 0
      });
"""
content = content.replace("""
      if (response.papers || response.results) {
        setResults(response.papers || response.results || []);
      }
""", new_logic)

with open('src/pages/HybridSearchPage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
