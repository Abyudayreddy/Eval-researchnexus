with open("src/pages/HybridSearchPage.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace loading UI
loading_old = """          ) : isLoading ? (
            <div className="flex flex-col items-center justify-center py-20 animate-in fade-in">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500 mb-4"></div>
              <div className="text-emerald-700 font-bold flex flex-col items-center gap-2">
                <span className="animate-pulse">Searching Local Research...</span>
                <span className="text-[10px] text-emerald-500/70 uppercase tracking-widest">Checking Local Evidence • Ranking</span>
              </div>
            </div>"""

loading_new = """          ) : isLoading ? (
            <div className="flex flex-col items-center justify-center py-20 animate-in fade-in">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500 mb-4"></div>
              <div className="text-emerald-700 font-bold flex items-center gap-2">
                <span className="animate-pulse">
                  {searchSource === 'local_only' ? 'Searching Local Research...' : (searchSource === 'local_online' ? 'Searching ResearchNexus + Academic Sources...' : 'Searching ResearchNexus...')}
                </span>
              </div>
            </div>"""

content = content.replace(loading_old, loading_new)

# Replace summary indicator
summary_old = """        {/* SUMMARY & INDICATOR */}
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
              {retrievalMeta.retrieval_source === 'online_fallback' && <span className="text-blue-600 font-bold">Local evidence was insufficient. Searching trusted online academic sources...</span>}
            </div>
          </div>
        )}"""

summary_new = """        {/* SUMMARY & INDICATOR */}
        {hasSearched && !isLoading && retrievalMeta && (
          <div className="flex items-center justify-between text-xs font-medium border-t border-slate-100 pt-3">
            <div className="text-slate-500">
              {retrievalMeta.retrieval_source === 'local' && (retrievalMeta.local_status === 'insufficient' ? 'No sufficient local research evidence was found.' : `Local Research • ${results.length} results`)}
              {retrievalMeta.retrieval_source === 'online_fallback' && `Online Fallback • ${results.length} results`}
              {retrievalMeta.retrieval_source === 'mixed' && `Local Research + Online Sources • ${results.length} results`}
              {retrievalMeta.retrieval_source === 'online' && `Online Sources • ${results.length} results`}
            </div>
            <div>
              {retrievalMeta.retrieval_source === 'local' && retrievalMeta.local_status !== 'insufficient' && <span className="text-emerald-600 font-bold">✓ Found in Local Research</span>}
              {retrievalMeta.retrieval_source === 'online_fallback' && <span className="text-blue-600 font-bold">Local evidence insufficient. ✓ Retrieved from Online Academic Sources</span>}
              {retrievalMeta.retrieval_source === 'mixed' && <span className="text-emerald-600 font-bold">✓ Local + Online Results</span>}
            </div>
          </div>
        )}"""

content = content.replace(summary_old, summary_new)

with open("src/pages/HybridSearchPage.tsx", "w", encoding="utf-8") as f:
    f.write(content)
