with open("src/pages/HybridSearchPage.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the simulated metadata logic with direct response mapping
old_meta = """      // Simulate Backend Metadata for UX requirements
      const meta = response.retrieval_source ? {
        retrieval_source: response.retrieval_source,
        retrieval_mode: response.retrieval_mode || searchSource,
        fallback_used: response.fallback_used || false,
        local_status: response.local_status || 'success',
        online_status: response.online_status || 'not_requested'
      } : {
        retrieval_source: searchSource === 'local_online' ? 'mixed' : (searchSource === 'local_only' ? 'local' : 'local'),
        retrieval_mode: searchSource,
        fallback_used: false,
        local_status: 'success',
        online_status: searchSource === 'local_online' ? 'success' : 'not_requested'
      };
      
      // Apply fallback logic based on mock
      if (searchSource === 'local_first' && (!data || data.length === 0)) {
         meta.retrieval_source = 'online_fallback';
         meta.fallback_used = true;
         meta.local_status = 'insufficient';
         meta.online_status = 'success';
      }
      
      setRetrievalMeta(meta);"""
      
new_meta = """      // Use actual backend metadata as single source of truth
      setRetrievalMeta({
        retrieval_source: response.retrieval_source,
        retrieval_mode: response.retrieval_mode,
        fallback_used: response.fallback_used,
        local_status: response.local_status,
        online_status: response.online_status
      });"""
      
content = content.replace(old_meta, new_meta)

with open("src/pages/HybridSearchPage.tsx", "w", encoding="utf-8") as f:
    f.write(content)
