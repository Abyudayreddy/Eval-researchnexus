import re

with open("src/pages/HybridSearchPage.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove searchSource state
state_old = "  const [searchSource, setSearchSource] = useState<'local_first' | 'local_only' | 'local_online'>('local_first');"
content = content.replace(state_old, "")

# 2. Update search mode in performSearch
perform_old = """      const response = await api.papers.search({
        query: searchQuery,
        search_mode: mode,
        retrieval_mode: searchSource,
        publication_year: year,
        sort_by: sort
      });"""
perform_new = """      const response = await api.papers.search({
        query: searchQuery,
        search_mode: mode,
        retrieval_mode: "local_online",
        publication_year: year,
        sort_by: sort
      });"""
content = content.replace(perform_old, perform_new)

# 3. Remove source selector UI completely (the 3 buttons)
selector_old = """            <div className="flex items-center bg-slate-100/80 p-1 rounded-lg border border-slate-200 shadow-inner">
              {[
                { id: 'local_first', label: 'LOCAL FIRST' },
                { id: 'local_only', label: 'LOCAL ONLY' },
                { id: 'local_online', label: 'LOCAL + ONLINE' },
              ].map(src => (
                <button
                  key={src.id}
                  onClick={() => setSearchSource(src.id as any)}
                  className={cn(
                    "px-3 py-1.5 rounded-md text-[10px] font-bold uppercase tracking-wider transition-all",
                    searchSource === src.id
                      ? "bg-white text-emerald-700 shadow-sm border border-slate-200"
                      : "text-slate-500 hover:text-slate-700"
                  )}
                  title={src.id === 'local_first' ? 'Search local first, fallback to online.' : src.id === 'local_only' ? 'Search only local ResearchNexus.' : 'Search both.'}
                >
                  {src.label}
                </button>
              ))}
            </div>

            <div className="flex items-center bg-slate-100/80 p-1 rounded-lg border border-slate-200 shadow-inner">"""

selector_new = """            <div className="flex items-center bg-slate-100/80 p-1 rounded-lg border border-slate-200 shadow-inner">"""
content = content.replace(selector_old, selector_new)

# 4. Simplify loading UI string
loading_old = """                <span className="animate-pulse">
                  {searchSource === 'local_only' ? 'Searching Local Research...' : (searchSource === 'local_online' ? 'Searching ResearchNexus + Academic Sources...' : 'Searching ResearchNexus...')}
                </span>"""
loading_new = """                <span className="animate-pulse">
                  Searching ResearchNexus...
                </span>"""
content = content.replace(loading_old, loading_new)

# 5. Simplify empty state string
empty_old = """              {searchSource === 'local_only' ? 'No sufficient local research evidence was found.' : 'We couldn\\'t retrieve sufficient research evidence right now.'}"""
empty_new = """              We couldn't retrieve sufficient research evidence right now."""
content = content.replace(empty_old, empty_new)

# 6. Simplify summary indicator to show Local + Online Research correctly
summary_old = """            <div>
              {retrievalMeta.retrieval_source === 'local' && retrievalMeta.local_status !== 'insufficient' && <span className="text-emerald-600 font-bold">✓ Found in Local Research</span>}
              {retrievalMeta.retrieval_source === 'online_fallback' && <span className="text-blue-600 font-bold">Local evidence insufficient. ✓ Retrieved from Online Academic Sources</span>}
              {retrievalMeta.retrieval_source === 'mixed' && <span className="text-emerald-600 font-bold">✓ Local + Online Results</span>}
            </div>"""
summary_new = """            <div>
              {retrievalMeta.retrieval_source === 'local' && <span className="text-emerald-600 font-bold">✓ Local Research</span>}
              {retrievalMeta.retrieval_source === 'online' && <span className="text-blue-600 font-bold">✓ Online Academic Research</span>}
              {retrievalMeta.retrieval_source === 'mixed' && <span className="text-emerald-600 font-bold">✓ Local + Online Research</span>}
            </div>"""
content = content.replace(summary_old, summary_new)

# 7. Paper link opening logic
# Search for: <a href={selectedPaper.url}
link_old = """              <a 
                href={selectedPaper.url} 
                target="_blank" 
                rel="noreferrer"
                className="w-full py-2.5 bg-slate-900 hover:bg-emerald-600 text-white rounded-lg text-sm font-bold transition-colors flex items-center justify-center gap-2"
              >
                <Maximize className="w-4 h-4" /> Open Source
              </a>"""

# Note: In Vite, we'll just construct the local endpoint for local papers
link_new = """              {selectedPaper.retrieval_source === 'local' ? (
                <a 
                  href={`http://localhost:8000/api/papers/${selectedPaper.id}/pdf`} 
                  target="_blank" 
                  rel="noreferrer"
                  className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-sm font-bold transition-colors flex items-center justify-center gap-2"
                >
                  <Maximize className="w-4 h-4" /> Open PDF
                </a>
              ) : selectedPaper.url ? (
                <a 
                  href={selectedPaper.url} 
                  target="_blank" 
                  rel="noreferrer"
                  className="w-full py-2.5 bg-slate-900 hover:bg-emerald-600 text-white rounded-lg text-sm font-bold transition-colors flex items-center justify-center gap-2"
                >
                  <Maximize className="w-4 h-4" /> Open Source
                </a>
              ) : (
                <button disabled className="w-full py-2.5 bg-slate-100 text-slate-400 rounded-lg text-sm font-bold flex items-center justify-center gap-2 cursor-not-allowed">
                  <Maximize className="w-4 h-4" /> Not Available
                </button>
              )}"""
content = content.replace(link_old, link_new)

with open("src/pages/HybridSearchPage.tsx", "w", encoding="utf-8") as f:
    f.write(content)
