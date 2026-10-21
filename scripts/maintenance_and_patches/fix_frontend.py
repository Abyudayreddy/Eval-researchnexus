import re

with open('src/pages/HybridSearchPage.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the initial performSearch
old_perform_search = """
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
content = content.replace(old_perform_search, "")

# Fix the polling update
old_poll = """
            setRetrievalMeta({
              retrieval_source: rawStatus.retrieval_source || 'mixed',
              local_status: st.local.status,
              online_status: st.online.status,
              local_count: st.metrics?.local_metrics?.result_count || 0,
              online_count: st.metrics?.online_metrics?.result_count || 0,
              combined_count: st.metrics?.combined_metrics?.result_count || 0
            });
            
            // Fix: Do not overwrite with empty array if status endpoint omits results
            if (rawStatus.results || rawStatus.papers) {
              setResults(rawStatus.results || rawStatus.papers);
            }
"""

new_poll = """
            setRetrievalMeta({
              retrieval_source: rawStatus.retrieval_source || 'mixed',
              local_status: st.local.status,
              online_status: st.online.status,
              local_count: rawStatus.local_result_count || st.metrics?.local_metrics?.result_count || 0,
              online_count: rawStatus.online_result_count || st.metrics?.online_metrics?.result_count || 0,
              combined_count: rawStatus.combined_result_count || st.metrics?.combined_metrics?.result_count || 0
            });
            
            if (rawStatus.results || rawStatus.papers) {
              setResults(rawStatus.results || rawStatus.papers);
            }
"""
content = content.replace(old_poll, new_poll)

with open('src/pages/HybridSearchPage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
