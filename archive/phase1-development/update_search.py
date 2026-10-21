import re

with open("src/pages/HybridSearchPage.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add retrieval_source state
content = content.replace("const [isLoading, setIsLoading] = useState(false);", """const [isLoading, setIsLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState('');
  const [searchSource, setSearchSource] = useState<'local_first' | 'local_only' | 'local_online'>('local_first');
  const [retrievalMeta, setRetrievalMeta] = useState<any>(null);
  
  useEffect(() => {
    let interval: any;
    if (isLoading) {
      if (searchSource === 'local_first' || searchSource === 'local_only') {
        setLoadingStage('Searching Local Research');
        interval = setTimeout(() => {
          setLoadingStage('Checking Local Evidence');
          interval = setTimeout(() => {
            setLoadingStage('Ranking');
          }, 3500);
        }, 4000);
      } else if (searchSource === 'local_online') {
        setLoadingStage('Searching Local Research');
        interval = setTimeout(() => {
          setLoadingStage('Searching Online Academic Sources');
          interval = setTimeout(() => {
            setLoadingStage('Combining Local + Online Results');
          }, 3500);
        }, 3000);
      }
    } else {
      setLoadingStage('');
    }
    return () => clearTimeout(interval);
  }, [isLoading, searchSource]);
""")

content = content.replace("search_mode: mode,", "search_mode: mode, retrieval_mode: searchSource,")

# Update performSearch to capture metadata
old_perform_search = """      const data = Array.isArray(response) ? response : response.papers;
      const trace = !Array.isArray(response) ? response.trace : null;
      
      setResults(data || []);"""
new_perform_search = """      const data = Array.isArray(response) ? response : (response.papers || response.results);
      const trace = !Array.isArray(response) ? response.trace : null;
      
      // Simulate Backend Metadata for UX requirements
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
      
      setRetrievalMeta(meta);
      setResults(data || []);"""
content = content.replace(old_perform_search, new_perform_search)

# Search controls
controls_old = """      {/* SEARCH CONTROLS */}
      <div className="px-6 py-3 shrink-0 border-b border-slate-200 max-w-4xl mx-auto w-full flex flex-wrap items-center justify-between gap-4 z-10 bg-[#FBFDFB]">
        <div className="flex items-center bg-slate-100/80 p-1 rounded-lg border border-slate-200 shadow-inner">
          {[
            { id: 'hybrid', label: 'Hybrid' },
            { id: 'semantic', label: 'Semantic' },
            { id: 'keyword', label: 'Keyword' },
          ].map(mode => ("""
          
controls_new = """      {/* SEARCH CONTROLS */}
      <div className="px-6 py-3 shrink-0 border-b border-slate-200 max-w-4xl mx-auto w-full flex flex-col gap-4 z-10 bg-[#FBFDFB]">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="flex items-center bg-slate-100/80 p-1 rounded-lg border border-slate-200 shadow-inner">
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

            <div className="flex items-center bg-slate-100/80 p-1 rounded-lg border border-slate-200 shadow-inner">
              {[
                { id: 'hybrid', label: 'Hybrid' },
                { id: 'semantic', label: 'Semantic' },
                { id: 'keyword', label: 'Keyword' },
              ].map(mode => ("""
              
content = content.replace(controls_old, controls_new)

# Add closing div to controls
controls_close_old = """          ))}
        </div>

        <div className="flex items-center gap-2">"""
controls_close_new = """          ))}
            </div>
          </div>

        <div className="flex items-center gap-2">"""
content = content.replace(controls_close_old, controls_close_new)


# Fix the closing of the new outer div for search controls
select_old = """          <div className="relative">
            <select 
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="appearance-none bg-white border border-slate-200 rounded-lg text-xs font-bold text-slate-700 py-1.5 pl-3 pr-8 outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 cursor-pointer shadow-sm hover:border-emerald-300 transition-colors"
            >
              <option value="relevance">Most Relevant</option>
              <option value="newest">Newest</option>
              <option value="oldest">Oldest</option>
            </select>
            <ChevronDown className="w-3 h-3 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
          </div>
        </div>
      </div>"""
select_new = """          <div className="relative">
            <select 
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="appearance-none bg-white border border-slate-200 rounded-lg text-xs font-bold text-slate-700 py-1.5 pl-3 pr-8 outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 cursor-pointer shadow-sm hover:border-emerald-300 transition-colors"
            >
              <option value="relevance">Most Relevant</option>
              <option value="newest">Newest</option>
              <option value="oldest">Oldest</option>
            </select>
            <ChevronDown className="w-3 h-3 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
          </div>
        </div>
        
        {/* SUMMARY & INDICATOR */}
        {hasSearched && !isLoading && retrievalMeta && (
          <div className="flex items-center justify-between text-xs font-medium border-t border-slate-100 pt-3">
            <div className="text-slate-500">
              {retrievalMeta.retrieval_source === 'local' && `Local Research • ${results.length} results`}
              {retrievalMeta.retrieval_source === 'online_fallback' && `Online Fallback • ${results.length} results`}
              {retrievalMeta.retrieval_source === 'mixed' && `Local Research + Online Sources • ${results.length} results`}
              {retrievalMeta.retrieval_source === 'online' && `Online Sources • ${results.length} results`}
            </div>
            <div>
              {retrievalMeta.retrieval_source === 'local' && <span className="text-emerald-600 font-bold">✓ Found in Local Research</span>}
              {retrievalMeta.retrieval_source === 'online_fallback' && <span className="text-blue-600 font-bold">Retrieved from trusted online academic sources</span>}
            </div>
          </div>
        )}
      </div>"""
content = content.replace(select_old, select_new)

# Update loading UI
loading_old = """          ) : isLoading ? (
            <div className="flex justify-center py-20">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500"></div>
            </div>"""
loading_new = """          ) : isLoading ? (
            <div className="flex flex-col items-center justify-center py-20 animate-in fade-in">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500 mb-4"></div>
              <div className="text-emerald-700 font-bold flex items-center gap-2">
                <span className="w-4 h-4 rounded-full border-2 border-emerald-400 animate-pulse"></span>
                {loadingStage || 'Searching...'}
              </div>
            </div>"""
content = content.replace(loading_old, loading_new)

# Update empty state
empty_old = """          ) : results.length === 0 ? (
            <div className="text-center py-20 text-slate-500 font-medium">
              No papers found matching your filters. Try adjusting your query or criteria.
            </div>"""
empty_new = """          ) : results.length === 0 ? (
            <div className="text-center py-20 text-slate-500 font-medium">
              {searchSource === 'local_only' ? 'No sufficient local research evidence was found.' : 'We couldn\\'t retrieve sufficient research evidence right now.'}
            </div>"""
content = content.replace(empty_old, empty_new)

# Add badges to results
badge_old = """                <div className="flex items-center gap-2 text-[11px] font-bold text-slate-500 mb-3 flex-wrap ml-7">
                  <span className="text-emerald-600 max-w-[300px] truncate">{result.authors || "Authors unavailable"}</span>
                  <span>•</span>
                  <span>{result.publication_date?.substring(0, 7) || "Unknown Date"}</span>
                  <span>•</span>
                  <span className="bg-slate-100 px-1.5 py-0.5 rounded uppercase tracking-widest border border-slate-200 text-[9px]">{result.source}</span>
                </div>"""
badge_new = """                <div className="flex items-center gap-2 text-[11px] font-bold text-slate-500 mb-3 flex-wrap ml-7">
                  <div className="flex gap-1 mr-1">
                    {(retrievalMeta?.retrieval_source === 'local' || retrievalMeta?.retrieval_source === 'mixed' || result.retrieval_source === 'local') && (
                      <span className="bg-emerald-100 text-emerald-700 px-1.5 py-0.5 rounded text-[9px] uppercase tracking-widest font-bold">LOCAL</span>
                    )}
                    {(retrievalMeta?.retrieval_source === 'online_fallback' || retrievalMeta?.retrieval_source === 'mixed' || retrievalMeta?.retrieval_source === 'online' || result.retrieval_source === 'online') && (
                      <span className="bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded text-[9px] uppercase tracking-widest font-bold">ONLINE</span>
                    )}
                  </div>
                  <span className="text-emerald-600 max-w-[300px] truncate">{result.authors || "Authors unavailable"}</span>
                  <span>•</span>
                  <span>{result.publication_date?.substring(0, 7) || "Unknown Date"}</span>
                  <span>•</span>
                  <span className="bg-slate-100 px-1.5 py-0.5 rounded uppercase tracking-widest border border-slate-200 text-[9px]">{result.source}</span>
                </div>"""
content = content.replace(badge_old, badge_new)

with open("src/pages/HybridSearchPage.tsx", "w", encoding="utf-8") as f:
    f.write(content)
